from django.contrib import admin
from courses.models import Category, Course, Lesson, Tag
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.urls import path
from django.db.models import Count
from django.template.response import TemplateResponse
from django.utils.html import mark_safe

# Register your models here.

class  MyAdminSite(admin.AdminSite):
    site_header = 'Hệ thống khoá học trực tuyến'

    def get_urls(self):
        return [
            path('course-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        stats = Course.objects.annotate(lesson_count=Count('my_lesson')).values('id', 'subject', 'lesson_count')

        return TemplateResponse(request,'admin/course-stats.html', {
                'stats': stats
})


admin_site = MyAdminSite(name='myadmin')



class LessonForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Lesson
        fields = '__all__'




class MyLessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'active', 'created_date', 'course_id']
    search_fields = ['subject', 'content']
    list_display = ['id', 'created_date', 'subject']
    readonly_fields = ['image_view']
    form = LessonForm

    def image_view(selfself, lesson):
        return mark_safe(f"<img src='/static/{lesson.image.name}'width='120' />")

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'description']
    readonly_fields = ['avatar']
    def avatar(self, obj):
        if obj:
            return mark_safe('<img src="/static/{url}" width="120" />'.format(url=obj.image.name)
)

admin_site.register(Category)
admin_site.register(Course, CourseAdmin)
admin_site.register(Lesson, MyLessonAdmin)
admin_site.register(Tag)
