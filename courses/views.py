from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from courses.models import Category, Course, Lesson
from courses.serializers import (
    CategorySerializer,
    CourseSerializer,
    LessonSerializer
)
from utils.permissions import IsInstructor, IsAdmin
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
        return [IsAuthenticated(), IsInstructor()]

    def perform_create(self, serializer):
        serializer.save(instructor=self.request.user)


# Lesson CRUD (Instructor only)
class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [IsAuthenticated()]
        return [IsAuthenticated(), IsInstructor()]

    def perform_create(self, serializer):
        # The course must belong to the instructor
        course = serializer.validated_data.get("course")
        if course.instructor != self.request.user:
            raise PermissionDenied("You can only add lessons to your own courses")
        serializer.save()
