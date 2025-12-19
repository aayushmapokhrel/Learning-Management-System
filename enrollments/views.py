from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from enrollments.models import Enrollment
from enrollments.serializers import EnrollmentSerializer
from utils.permissions import IsStudent


class EnrollmentViewSet(ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    def perform_create(self, serializer):
        course = serializer.validated_data.get('course')

        # Prevent duplicate enrollment
        if Enrollment.objects.filter(
            student=self.request.user,
            course=course
        ).exists():
            raise ValidationError(
                detail="You are already enrolled in this course."
            )

        serializer.save(student=self.request.user)
