from rest_framework import permissions

from .models import Meeting


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):

        print(view.kwargs)
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            meeting = Meeting.objects.get(
                pk=view.kwargs['pk'])
            return meeting.created_by == request.user
