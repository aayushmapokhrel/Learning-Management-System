from rest_framework import serializers
from courses.models import Category, Course, Lesson, Assignment, AssignmentSubmission, LessonProgress
from django.utils import timezone


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description"
        ]

class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)
    lessons_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "description",
            "category",
            "instructor",
            "lessons_count",
            "created_at",
            "updated_at",
        ]
    def get_lessons_count(self, obj):
        return obj.lessons.count()



class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "video", "material", "created_at"]

    def validate_video(self, value):
        if value:
            if not value.name.endswith((".mp4", ".avi", ".mov")):
                raise serializers.ValidationError("Unsupported video format.")
        return value

    def validate_material(self, value):
        if value:
            if not value.name.endswith((".pdf", ".docx", ".pptx")):
                raise serializers.ValidationError("Unsupported material format.")
        return value


class AssignmentSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(read_only=True)
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Assignment
        fields = [
            "id",
            "course",
            "course_title",
            "title",
            "description",
            "attachment",
            "due_date",
            "instructor",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["instructor", "created_at", "updated_at"]

    def validate_due_date(self, value):
        """
        Ensure the due date is in the future.
        """
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value

    def validate_attachment(self, value):
        if value:
            if not value.name.endswith((".pdf", ".docx", ".pptx")):
                raise serializers.ValidationError("Unsupported attachment format.")
        return value


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.full_name", read_only=True)
    assignment_title = serializers.CharField(source="assignment.title", read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = [
            "id",
            "assignment",
            "assignment_title",
            "student",
            "student_name",
            "file",
            "submitted_at",
            "grade",
            "feedback",
        ]
        read_only_fields = ["submitted_at", "student_name", "assignment_title"]

    def validate(self, attrs):
        assignment = attrs.get("assignment")
        if assignment.due_date < timezone.now():
            raise serializers.ValidationError(
                "Cannot submit: the assignment due date has passed."
            )
        return attrs


class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source="lesson.title", read_only=True)
    course = serializers.IntegerField(source="lesson.course.id", read_only=True)

    class Meta:
        model = LessonProgress
        fields = ["id", "lesson", "lesson_title", "course", "completed", "completed_at"]
        read_only_fields = ["completed_at"]

    def update(self, instance, validated_data):
        if validated_data.get("completed") and not instance.completed:
            instance.completed_at = timezone.now()
        return super().update(instance, validated_data)
    
