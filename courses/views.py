from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from courses.models import Category, Course, Lesson, Assignment, AssignmentSubmission, LessonProgress
from courses.serializers import (
    CategorySerializer,
    CourseSerializer,
    LessonSerializer,
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    LessonProgressSerializer,
)
from utils.permissions import IsInstructor, IsAdmin, IsInstructorOrOwner, IsStudentOwner
from rest_framework.exceptions import PermissionDenied


# Category CRUD (Admin only)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdmin]


# Course CRUD (Instructor creates, Admin can manage)
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsInstructor()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


# Lesson CRUD (Instructor only)
class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsInstructor()]

    def perform_create(self, serializer):
        # The course must belong to the instructor
        course = serializer.validated_data.get("course")
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only add lessons to your own courses")
        serializer.save()


class AssignmentViewSet(ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsInstructor()]

    def perform_create(self, serializer):
        course = serializer.validated_data.get("course")

        if course.instructor != self.request.user:
            raise PermissionDenied(
                "You can only create assignments for your own courses."
            )

        serializer.save(instructor=self.request.user)


class AssignmentSubmissionViewSet(ModelViewSet):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated, IsInstructorOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'instructor':
            # Instructor sees submissions only for their assignments
            return AssignmentSubmission.objects.filter(assignment__instructor=user)
        elif user.role == 'student':
            # Student sees only their own submissions
            return AssignmentSubmission.objects.filter(student=user)
        return AssignmentSubmission.objects.none()

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied("Only students can submit assignments.")

        serializer.save(student=self.request.user)


class LessonProgressViewSet(ModelViewSet):
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated, IsStudentOwner]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'student':
            return LessonProgress.objects.filter(student=user)

        if user.role == 'instructor':
            return LessonProgress.objects.filter(
                lesson__course__instructor=user
            )

        return LessonProgress.objects.all()

    def perform_create(self, serializer):
        if self.request.user.role != 'student':
            raise PermissionDenied("Only students can track progress.")

        serializer.save(student=self.request.user)
