import django
from rest_framework import mixins, generics
from workouts.mixins import CreateListModelMixin
from rest_framework import permissions
from users.serializers import (
    UserSerializer,
    OfferSerializer,
    AthleteFileSerializer,
    UserPutSerializer,
    UserGetSerializer,
)
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from users.models import Offer, AthleteFile
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from users.permissions import IsCurrentUser, IsAthlete, IsCoach
from workouts.permissions import IsOwner, IsReadOnly
from users.serializers import RememberMeSerializer
from rest_framework.response import Response
from django.core.signing import Signer
import base64, pickle


# Create your views here.
class UserList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = UserSerializer
    users = []
    admins = []

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserGetSerializer
        return self.list(request, *args, **kwargs)
        

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        query_set = get_user_model().objects.all()

        if self.request.user:
            # Return the currently logged in user
            status = self.request.query_params.get("user", None)
            if status and status == "current":
                query_set = get_user_model().objects.filter(pk=self.request.user.pk)
            
            # Search for user by username starts with
            search_string = self.request.query_params.get("search", None)
            if search_string:
                query_set = get_user_model().objects.filter(username__startswith=search_string)[:3]

        return query_set


class UserDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    lookup_field_options = ["pk", "username"]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated & (IsCurrentUser | IsReadOnly)]

    def get_object(self):
        for field in self.lookup_field_options:
            if field in self.kwargs:
                self.lookup_field = field
                break

        return super().get_object()

    def get(self, request, *args, **kwargs):
        self.serializer_class = UserGetSerializer
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        self.serializer_class = UserPutSerializer
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class OfferList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        result = Offer.objects.none()

        if self.request.user:
            query_set = Offer.objects.filter(
                Q(owner=self.request.user) | Q(recipient=self.request.user)
            ).distinct()
            query_params = self.request.query_params
            user = self.request.user

            # filtering by status (if provided)
            status = query_params.get("status", None)
            if status is not None and self.request is not None:
                query_set = query_set.filter(status=status)
                if query_params.get("status", None) is None:
                    query_set = Offer.objects.filter(Q(owner=user)).distinct()

            # filtering by category (sent or received)
            category = query_params.get("category", None)
            if category is not None and query_params is not None:
                if category == "sent":
                    query_set = query_set.filter(owner=user)
                elif category == "received":
                    query_set = query_set.filter(recipient=user)
            return query_set
        else:
            return result


class OfferDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class AthleteFileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):
    queryset = AthleteFile.objects.all()
    serializer_class = AthleteFileSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAthlete | IsCoach)]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        query_set = AthleteFile.objects.none()

        if self.request.user:
            query_set = AthleteFile.objects.filter(
                Q(athlete=self.request.user) | Q(owner=self.request.user)
            ).distinct()

        return query_set


class AthleteFileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = AthleteFile.objects.all()
    serializer_class = AthleteFileSerializer
    permission_classes = [permissions.IsAuthenticated & (IsAthlete | IsOwner)]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# Allow users to save a persistent session in their browser
class RememberMe(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    serializer_class = RememberMeSerializer

    def get(self, request):
        if request.user.is_authenticated == False:
            raise PermissionDenied
        else:
            return Response({"remember_me": self.rememberme()})

    def post(self, request):
        cookie_object = namedtuple("Cookies", request.COOKIES.keys())(
            *request.COOKIES.values()
        )
        user = self.get_user(cookie_object)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

    def get_user(self, cookie_object):
        decode = base64.b64decode(cookie_object.remember_me)
        user, sign = pickle.loads(decode)

        # Validate signature
        if sign == self.sign_user(user):
            return user

    def rememberme(self):
        creds = [self.request.user, self.sign_user(str(self.request.user))]
        return base64.b64encode(pickle.dumps(creds))

    def sign_user(self, username):
        signer = Signer()
        signed_user = signer.sign(username)
        return signed_user