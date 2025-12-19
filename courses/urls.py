from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, LessonViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('courses', CourseViewSet, basename='courses')
router.register('lessons', LessonViewSet, basename='lessons')

urlpatterns = router.urls
