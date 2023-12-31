from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import *

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lesson_create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_get'),
    path('lesson_update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson_delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments_create/', PaymentsCreateAPIView.as_view(), name='payments_create'),
    path('payments_list/', PaymentsListAPIView.as_view(), name='payments_list'),

    path('subscribe/<int:pk>/', SubscriptionCreateAPIView.as_view(), name='subscribe'),
    path('unsubscribe/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='unsubscribe'),
] + router.urls
