from django.contrib import admin
# from django.contrib.auth.models import Group
from django_summernote.admin import SummernoteModelAdmin
from embed_video.admin import AdminVideoMixin

from .models import Course#, Upload, UploadVideo, Program, CourseAllocation


class CourseAdmin(AdminVideoMixin, SummernoteModelAdmin, admin.ModelAdmin):
    list_display  = ["title", "code", "plan", "video", "upload_file", 'is_public', "active", 'updated', 'created']
    list_filter = ["created", "updated", "active", "plan"]
    search_fields = ['title', "description", "video"]
    ordering = ['created']
    # prepopulated_fields = {'slug': ('title', )} 
    summernote_fields = ('description', ) 

    class Meta:
        model = Course

admin.site.register(Course, CourseAdmin) 


# admin.site.register(Program)
# admin.site.register(Course)
# admin.site.register(Upload)
# admin.site.register(UploadVideo)
# admin.site.register(Thumbnail)
# admin.site.register(CourseAllocation)


