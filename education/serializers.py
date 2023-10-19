from rest_framework import serializers

from education.models import Course, Lesson, Payments
from education.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count')
    lessons = LessonSerializer(source='lesson_set.all', many=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'
        validators = [LinkValidator(field='description')]


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'
