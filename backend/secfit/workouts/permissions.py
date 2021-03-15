"""Contains custom DRF permissions classes for the workouts app
"""
from rest_framework import permissions
from workouts.models import Workout, WorkoutInvitation, Exercise
from django.contrib.auth import get_user_model


class IsOwner(permissions.BasePermission):
    """Checks whether the requesting user is also the owner of the existing object"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfWorkout(permissions.BasePermission):
    """Checks whether the requesting user is also the owner of the new or existing object"""

    def has_permission(self, request, view):
        if request.method == "POST":
            if hasattr(request, 'data') and request.data.get("workout"):
                workout_id = request.data["workout"].split("/")[-2]
                workout = Workout.objects.get(pk=workout_id)
                if workout:
                    return workout.owner == request.user
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.workout.owner == request.user

class IsOwnerOfExercise(permissions.BasePermission):
    """Checks whether the requesting user is also the owner of the new or existing object"""

    def has_permission(self, request, view):
        if request.method == "POST":
            if hasattr(request, 'data') and request.data.get("exercise"):
                exercise_id = request.data["exercise"].split("/")[-2]
                exercise = Exercise.objects.get(pk=exercise_id)
                if exercise:
                    return exercise.owner == request.user
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.exercise.owner == request.user

class IsCoachAndVisibleToCoach(permissions.BasePermission):
    """Checks whether the requesting user is the existing object's owner's coach
    and whether the object (workout) has a visibility of Public or Coach.
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner.coach == request.user


class IsCoachOfWorkoutAndVisibleToCoach(permissions.BasePermission):
    """Checks whether the requesting user is the existing workout's owner's coach
    and whether the object has a visibility of Public or Coach.
    """

    def has_object_permission(self, request, view, obj):
        return obj.workout.owner.coach == request.user


class IsPublic(permissions.BasePermission):
    """Checks whether the object (workout) has visibility of Public."""

    def has_object_permission(self, request, view, obj):
        return obj.visibility == "PU"


class IsWorkoutPublic(permissions.BasePermission):
    """Checks whether the object's workout has visibility of Public."""

    def has_object_permission(self, request, view, obj):
        return obj.workout.visibility == "PU"


class IsReadOnly(permissions.BasePermission):
    """Checks whether the HTTP request verb is only for retrieving data (GET, HEAD, OPTIONS)"""

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS

class IsOwnerOrParticipantOfWorkoutInvitation(permissions.BasePermission):
    """Checks whether the user is allowed to delete a workout invitation"""

    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE":
            invitation_pk = view.kwargs["pk"]
            invitation = WorkoutInvitation.objects.filter(pk=invitation_pk).first()
            if(request.user == invitation.owner or request.user == invitation.participant):
                return True

        return False

class IsInvitedToWorkout(permissions.BasePermission):
    """Checks whether the user is allowed to edit or get the workout. For invited participants to be able to add itself to the workout."""
    def has_object_permission(self, request, view, obj):
        if request.method == "PUT" or request.method == "GET":
            workout_pk = view.kwargs["pk"]
            workout = Workout.objects.get(pk=workout_pk)
            invitation = WorkoutInvitation.objects.filter(workout=workout, participant=request.user).first()
            if invitation is None:
                return False
            if(request.user == workout.owner or request.user == invitation.participant):
                return True

        return False

class IsParticipantToWorkout(permissions.BasePermission):
    """Checks whether the user is allowed to edit or get the workout. For participants to be able se the workout."""
    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            workout_pk = view.kwargs["pk"]
            workout = Workout.objects.get(pk=workout_pk)
            users = get_user_model().objects.filter(pk__in=workout.participants.all().values_list('id', flat=True))
            if request.user in users:
                return True

        return False