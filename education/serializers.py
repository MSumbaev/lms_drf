from rest_framework import serializers

from education.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.all.count')

    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'
