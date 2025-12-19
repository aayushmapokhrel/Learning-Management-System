from rest_framework import serializers
from courses.models import Category, Course, Lesson


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    instructor = serializers.StringRelatedField(
        read_only=True
    )
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
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )

    class Meta:
        model = Lesson
        fields = ["id", "title", "course", "video", "material", "created_at"]

    def validate_video(self, value):
        if value:
            if not value.name.endswith(('.mp4', '.avi', '.mov')):
                raise serializers.ValidationError("Unsupported video format.")
        return value

    def validate_material(self, value):
        if value:
            if not value.name.endswith(('.pdf', '.docx', '.pptx')):
                raise serializers.ValidationError("Unsupported material format.")
        return value
