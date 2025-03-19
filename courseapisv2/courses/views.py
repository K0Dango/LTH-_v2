from venv import create

from django.template.defaulttags import CommentNode
from rest_framework.decorators import action
from rest_framework.response import Response

from courses.models import Category, Course, Lesson, User, Comment, Like
from courses import  paginators, serializers, perms
from rest_framework import viewsets, generics, parsers, status, permissions


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePagination

    # ghi đè queryset
    def get_queryset(self):
        query = self.queryset

        if self.action.__eq__('list'):
            # Thuộc tính request nằm trong self
            q = self.request.query_params.get("q")
            if q:
                query = query.filter(subject__icontains=q)

            cate_id = self.request.query_params.get("category_id")
            if cate_id:
                query = query.filter(category_id=cate_id)

        return query

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):
        lessons = self.get_object().lesson_set.filter(active=True)
        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)
        return Response(serializers.LessonSerializer(lessons, many=True).data, status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailSerializer

    def get_permissions(self):
        if self.action.__eq__('get_comments'):
            if self.request.method.__eq__('POST'):
                return [permissions.IsAuthenticated()]
        elif self.action.__eq__('like'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny]

    @action(methods=['get', 'post'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        if request.method.__eq__('POST'):
            t = serializers.CommentSerializer(data={
                'content': request.data.get('content'),
                'user': request.user.pk,
                'lesson': pk
            })
            t.is_valid(raise_exception=True)
            c = t.save()
            return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)
        else:
            comments = self.get_object().comment_set.select_related('user').filter(active=True)
            return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=['POST'], url_path='like',detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(user=request.user, lesson=self.get_object())
        if not created:
            li.active = not li.active


        li.save()
        return Response(serializers.LessonDetailSerializer(self.get_object(), context={'request': self.request}).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser]


    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH']:
            return [perms.OwnerPerms()]

        return [permissions.AllowAny()]


    @action(methods=['get'], url_name='current-user', detail=False, permissions_class=[permissions.IsAuthenticated])
    def get_current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [perms.CommentOwner]
