"""Contains views for the workouts application. These are mostly class-based views.
"""
from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.parsers import (
    JSONParser,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q
from rest_framework import filters
from workouts.parsers import MultipartJsonParser
from workouts.permissions import (
    IsOwner,
    IsCoachAndVisibleToCoach,
    IsOwnerOfWorkout,
    IsCoachOfWorkoutAndVisibleToCoach,
    IsReadOnly,
    IsPublic,
    IsWorkoutPublic,
    IsOwnerOrParticipantOfWorkoutInvitation,
    IsInvitedToWorkout,
    IsParticipantToWorkout,
    IsOwnerOfExercise,
)
from workouts.mixins import CreateListModelMixin
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile, WorkoutInvitation, ExerciseFile
from workouts.serializers import WorkoutSerializer, ExerciseSerializer, WorkoutInvitationSerializer
from workouts.serializers import ExerciseInstanceSerializer, WorkoutFileSerializer, ExerciseFileSerializer
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import json
from collections import namedtuple
import base64, pickle
from django.core.signing import Signer
from rest_framework.parsers import MultiPartParser, FormParser


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "workouts": reverse("workout-list", request=request, format=format),
            "exercises": reverse("exercise-list", request=request, format=format),
            "exercise-instances": reverse(
                "exercise-instance-list", request=request, format=format
            ),
            "workout-files": reverse(
                "workout-file-list", request=request, format=format
            ),
            "exercise-files": reverse(
                "exercise-file-list", request=request, format=format
            ),
            "comments": reverse("comment-list", request=request, format=format),
            "likes": reverse("like-list", request=request, format=format),
        }
    )


class WorkoutList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """Class defining the web response for the creation of a Workout, or displaying a list
    of Workouts

    HTTP methods: GET, POST
    """

    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]  # User must be authenticated to create/view workouts
    parser_classes = [
        MultipartJsonParser,
        JSONParser,
    ]  # For parsing JSON and Multi-part requests
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "date", "owner__username"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        query_set = Workout.objects.none()
        if self.request.user:
            # A workout should be visible to the requesting user if any of the following hold:
            # - The workout has public visibility
            # - The owner of the workout is the requesting user
            # - The workout has coach visibility and the requesting user is the owner's coach
            query_set = Workout.objects.filter(
                Q(visibility="PU")
                | (Q(visibility="CO") & Q(owner__coach=self.request.user))
                | Q(owner=self.request.user) # BUG FIX -> This allow user to see it own workouts
                | Q(participants=self.request.user)
            ).distinct()

        return query_set


class WorkoutDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the details of an individual Workout.

    HTTP methods: GET, PUT, DELETE
    """

    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & ((IsOwner | IsInvitedToWorkout | IsParticipantToWorkout) | (IsReadOnly & (IsCoachAndVisibleToCoach | IsPublic)))
    ]
    parser_classes = [MultipartJsonParser, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExerciseList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    """Class defining the web response for the creation of an Exercise, or
    a list of Exercises.

    HTTP methods: GET, POST
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    parser_classes = [
        MultipartJsonParser,
        FormParser
    ]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ExerciseDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the details of an individual Exercise.

    HTTP methods: GET, PUT, PATCH, DELETE
    """

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    parser_classes = [
        MultipartJsonParser,
        JSONParser
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ExerciseFileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = ExerciseFile.objects.all()
    serializer_class = ExerciseFileSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfExercise]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExerciseInstanceList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):
    """Class defining the web response for the creation"""

    serializer_class = ExerciseInstanceSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        query_set = ExerciseInstance.objects.none()
        if self.request.user:
            query_set = ExerciseInstance.objects.filter(
                Q(workout__owner=self.request.user)
                | (
                    (Q(workout__visibility="CO") | Q(workout__visibility="PU"))
                    & Q(workout__owner__coach=self.request.user)
                )
            ).distinct()

        return query_set


class ExerciseInstanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ExerciseInstanceSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (
            IsOwnerOfWorkout
            | (IsReadOnly & (IsCoachOfWorkoutAndVisibleToCoach | IsWorkoutPublic))
        )
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WorkoutFileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]
    parser_classes = [MultipartJsonParser, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        query_set = WorkoutFile.objects.none()
        if self.request.user:
            query_set = WorkoutFile.objects.filter(
                Q(owner=self.request.user)
                | Q(workout__owner=self.request.user)
                | (
                    Q(workout__visibility="CO")
                    & Q(workout__owner__coach=self.request.user)
                )
                | Q(workout__visibility="PU") # BUG FIX -> to allow users to see pulic workout files
            ).distinct()

        return query_set


class WorkoutInvitationList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutInvitation.objects.all()
    serializer_class = WorkoutInvitationSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOfWorkout]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs): # Permission ok
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
            )

    def get_queryset(self):
        query_set = WorkoutInvitation.objects.none()
        if self.request.user:
            query_set = WorkoutInvitation.objects.filter(
                Q(participant=self.request.user)
            ).distinct()

        return query_set

class WorkoutInvitationDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutInvitation.objects.all()
    serializer_class = WorkoutInvitationSerializer
    permission_classes = [
        permissions.IsAuthenticated & IsOwnerOrParticipantOfWorkoutInvitation# TODO is owner or participant
    ]

    def delete(self, request, *args, **kwargs): # TODO is owner or participant
        return self.destroy(request, *args, **kwargs)

class WorkoutFileDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (
            IsOwner
            | IsOwnerOfWorkout
            | (IsReadOnly & (IsCoachOfWorkoutAndVisibleToCoach | IsWorkoutPublic))
        )
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
