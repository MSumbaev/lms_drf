from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import CourseViewSet

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [

] + router.urls
