from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    avatar = CloudinaryField(null=True)  # models.ImageField(upload_to='User/%Y/%m/', null=True)


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Category(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    subject = models.CharField(max_length=255)
    description = RichTextField()
    image = CloudinaryField(null=True)  # models.ImageField(upload_to='courses/%Y/%m/')
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    def __str__(self):
        return self.subject


class Lesson(BaseModel):
    subject = models.CharField(max_length=255)
    content = RichTextField()
    image = CloudinaryField(null=True)  # models.ImageField(upload_to='lessons/%Y/%m/')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.subject


class Tag(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


# Lưu trữ thông tin Tương Tác (Interaction) giữa người dùng và bài học
class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    class Meta:
        abstract = True


# Người dùng Tương Tác (Interact) với bài học bằng Comment
class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.content


# Người dùng Tương Tác (Interact) Thích với bài học
class Like(Interaction):
    class Meta:
        # Mỗi người chỉ thích bài học 1 lần
        unique_together = ('user', 'lesson')
