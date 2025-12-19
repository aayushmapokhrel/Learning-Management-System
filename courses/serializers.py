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
