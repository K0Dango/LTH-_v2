from django.utils.timezone import activate
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, Tag
from courses import seriallzers, paginators
from rest_framework import viewsets, generics, status


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = seriallzers.CategorySerialier


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = seriallzers.CourseSerialier
    pagination_class = paginators.CoursePaginatior

    def get_queryset(self):
        query = self.queryset


        if self.action.__eq__('list'):
            q = self.request.query_params.get('q')
            if q:
                query = query.filter(subject__icontains=q)

            cate_id = self.request.query_params.get('category_id')
            if cate_id:
                query = query.filter(category_id=cate_id)

        return query


    @action(methods=['get'], detail=True, url_path='lessons')
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)
        return Response(seriallzers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.filter(active=True)
    serializer_class = seriallzers.LessonSerializer