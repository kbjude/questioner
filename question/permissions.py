# from rest_framework import permissions


# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Custom permission class to allow only question owners update them.
#     """

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    @classmethod
    def has_object_permission(cls, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner
        return obj.created_by == request.user
=======
=======
>>>>>>> parent of 8b363b8... Update permissions.py
=======
>>>>>>> parent of 8b363b8... Update permissions.py
=======
>>>>>>> parent of 8b363b8... Update permissions.py
#     def has_object_permission(self, request, view, obj):
#         # Read permissions are allowed to any request
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # Write permissions are only allowed to the owner
#         return obj.created_by == request.user
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> parent of 8b363b8... Update permissions.py
=======
>>>>>>> parent of 8b363b8... Update permissions.py
=======
>>>>>>> parent of 8b363b8... Update permissions.py
=======
>>>>>>> parent of 8b363b8... Update permissions.py
