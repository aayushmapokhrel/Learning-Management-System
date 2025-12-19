from rest_framework import serializers
from enrollments.models import Enrollment


class EnrollmentSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    course_title = serializers.CharField(
        source='course.title',
        read_only=True
    )

    class Meta:
        model = Enrollment
        fields = [
            'id',
            'student',
            'course',
            'course_title',
            'progress',
            'enrolled_at'
        ]
        read_only_fields = ['progress']
