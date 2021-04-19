from rest_framework import permissions


class IsCommentVisibleToUser(permissions.BasePermission):
    """
    Custom permission to only allow a comment to be viewed
    if one of the following holds:
    - The comment is on a public visibility workout
    - The comment was written by the user
    - The comment is on a coach visibility workout and the user is the workout owner's coach
    - The comment is on a workout owned by the user
    """

    def has_object_permission(self, request, view, comment):
        # Write permissions are only allowed to the owner.
        return (
            comment.workout.visibility == "PU"
            or comment.owner == request.user
            or (comment.workout.visibility == "CO" and comment.owner.coach == request.user)
            or comment.workout.owner == request.user
        )
