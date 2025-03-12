from rest_framework.serializers import ModelSerializer

from courses.models import Category, Course, Lesson, Tag
from rest_framework import serializers


class CategorySerialier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CourseSerialier(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'subject', 'description','created_date', 'category_id']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'created_date', 'course_id']


