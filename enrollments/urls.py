from rest_framework.routers import DefaultRouter
from enrollments.views import EnrollmentViewSet

router = DefaultRouter()
router.register('enrollments', EnrollmentViewSet, basename='enrollments')

urlpatterns = router.urls
