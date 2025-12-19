from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "instructor"


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"


class IsInstructorOrOwner(BasePermission):
    """
    Instructor can view submissions for their assignments.
    Student can view only their own submissions.
    """

    def has_object_permission(self, request, view, obj):
        if request.user.role == "instructor":
            return obj.assignment.instructor == request.user
        elif request.user.role == "student":
            return obj.student == request.user
        return False
