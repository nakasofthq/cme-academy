from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import Q
from django.dispatch import receiver
from django.db import models
from embed_video.fields import EmbedVideoField


   

# project import
from .utils import *
# from core.models import ActivityLog
from plans.models import Plan


GRADE_0 = "0"
GRADE_1 = "1"
GRADE_2 = "2"
GRADE_3 = "3"
GRADE_4 = "4"
GRADE_5 = "5"
GRADE_6 = "6"

GRADE_CHOICES = (
    # (LEVEL_COURSE, "Level course"),
    (GRADE_0, "Grade Zero"),
    (GRADE_1, "Grade One"),
    (GRADE_2, "Grade Two"),
    (GRADE_3, "Grade Three"),
    # (GRADE_4, "Grade Four"),
    # (GRADE_5, "Grade Five"),
    # (GRADE_6, "Grade Six"),
)

# class ProgramManager(models.Manager):
#     def search(self, query=None):
#         queryset = self.get_queryset()
#         if query is not None:
#             or_lookup = Q(title__icontains=query) | Q(description__icontains=query)
#             queryset = queryset.filter(
#                 or_lookup
#             ).distinct()  # distinct() is often necessary with Q lookups
#         return queryset


# class Program(models.Model):
#     title = models.CharField(max_length=150, unique=True)
#     description = models.TextField(null=True, blank=True)

#     objects = ProgramManager()

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse("program_detail", kwargs={"pk": self.pk})


# @receiver(post_save, sender=Program)
# def log_save(sender, instance, created, **kwargs):
#     verb = "created" if created else "updated"
#     ActivityLog.objects.create(message=f"The program '{instance}' has been {verb}.")


# @receiver(post_delete, sender=Program)
# def log_delete(sender, instance, **kwargs):
#     ActivityLog.objects.create(message=f"The program '{instance}' has been deleted.")












# def image_location(instance, filename):
#     # filebase = filename.split(".")[0]
#     return "courses/images/%s/%s" %(instance.code, filename)



def image_validator(fieldfile_obj):
    filesize = fieldfile_obj.size
    megabyte_limit = 1.0
    if filesize > megabyte_limit*1024*1024:
        raise ValidationError("Image too large, Maximum size allowed is %sMB" %(megabyte_limit))


class CourseManager(models.Manager):
    # def get_queryset(self):
    #     return CourseQuerySet(self.model, using=self._db).filters(active=True)

    def all(self):
        return self.get_queryset().all().filter(active=True)

    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(code__icontains=query)
                | Q(slug__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


class Course(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(blank=True, unique=True, editable=False)
    code = models.CharField(max_length=200, unique=True, null=True)
    description = models.TextField(max_length=600, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0.0, editable=False)
    plan = models.ForeignKey(Plan, related_name='course_plan', on_delete=models.SET_NULL, null=True) 
    video = EmbedVideoField(blank=True)
    # grade = models.CharField(max_length=25, choices=GRADE_CHOICES, null=True)
    # program = models.ForeignKey(Program, on_delete=models.CASCADE)
    # level = models.CharField(max_length=25, choices=LEVEL, null=True)
    # year = models.IntegerField(choices=YEARS, default=0)
    # semester = models.CharField(choices=SEMESTER, max_length=200)
    # video_id = models.CharField(max_length=200, null=True, blank=True, help_text="Only input the video ID without the domain")
    # video_link = models.URLField(max_length=200, null=True, blank=True, help_text="Include https:// or http://",)
    upload_file = models.FileField(
        upload_to="course_files/",
        help_text="Valid Files: Portable Documents File (PDF)",# pdf, docx, doc, xls, xlsx, ppt, pptx,
        validators=[
            FileExtensionValidator(
                [
                    "pdf",
                    # "docx",
                    # "doc",
                    # "xls",
                    # "xlsx",
                    # "ppt",
                    # "pptx",
                    # "rar",
                    # "zip",
                    # "7zip",
                ]
            )
        ],
        blank = True,
        null = True,
    )
    thumbnail = models.ImageField(
        upload_to = "course_images/", #image_location,
        validators=[image_validator,
            FileExtensionValidator(
                [
                    "png",
                    "jpg",
                    "jpeg",
                ]
            )
        ],
        blank = True,
        null = True,
        # height_field = "home_image_height",
        # width_field = "home_image_width",
        editable=False
    )
    is_public = models.BooleanField(default=False, blank=True, null=True)
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    created = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = CourseManager()

    class Meta:
        ordering = ("code", "created",)

    def __str__(self):
        return "{0} ({1})".format(self.title, self.code)

    def get_absolute_url(self):
        return reverse("dashboard:course_detail", kwargs={"slug": self.slug})

    @property
    def get_image_url(self):
        if self.thumbnail:
            return self.thumbnail.url
        return None

    @property
    def get_file_extension_short(self):
        ext = str(self.file).split(".")
        ext = ext[len(ext) - 1]

        if ext in ("doc", "docx"):
            return "word"
        elif ext == "pdf":
            return "pdf"
        elif ext in ("xls", "xlsx"):
            return "excel"
        elif ext in ("ppt", "pptx"):
            return "powerpoint"
        elif ext in ("zip", "rar", "7zip"):
            return "archive"


    def get_course_grade(self):
        if self.plan.title == "free":
            grade = 0
        elif self.plan.title == "basic":
            grade = 1
        elif self.plan.title == "standard":
            grade = 2
        elif self.plan.title == "pro":
            grade = 3
        else:
            grade = 0
        return grade


    # === Try to resize image while saving
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.thumbnail.path)
            if img.height > 600 or img.width > 400:
                output_size = (600, 400)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)
        except:
            pass


    def delete(self, *args, **kwargs):
        self.image.delete()
        self.file.delete()
        self.video.delete()
        # if self.image:
        #     self.image.delete()
        # if self.file:
        #     self.file.delete()
        # if self.video:
        #     self.video.delete()
        super().delete(*args, **kwargs)


def course_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(course_pre_save_receiver, sender=Course)


@receiver(post_save, sender=Course)
def log_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"The course '{instance}' has been {verb}.")


@receiver(post_delete, sender=Course)
def log_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"The course '{instance}' has been deleted.")











# class CourseAllocation(models.Model):
#     lecturer = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="allocated_lecturer",
#     )
#     courses = models.ManyToManyField(Course, related_name="allocated_course")
#     session = models.ForeignKey(
#         "core.Session", on_delete=models.CASCADE, blank=True, null=True
#     )

#     def __str__(self):
#         return self.lecturer.get_full_name

#     def get_absolute_url(self):
#         return reverse("edit_allocated_course", kwargs={"pk": self.pk})














# class Thumbnail(models.Model):
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     image = models.ImageField(
#         upload_to = "course_images/", #image_location,
#         validators=[image_validator,
#             FileExtensionValidator(
#                 [
#                     "png",
#                     "jpg",
#                     "jpeg",
#                 ]
#             )
#         ],
#         blank = True,
#         null = True,
#         # height_field = "home_image_height",
#         # width_field = "home_image_width",
#     )
#     timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

#     # class Meta:
#     #     db_table = 'auth_user'

#     class Meta:
#         abstract = False
#         verbose_name = _("Upload Thumbnail")
#         verbose_name_plural = _("Upload Thumbnails")










# class Upload(models.Model):
#     title = models.CharField(max_length=100)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     file = models.FileField(
#         upload_to="course_files/",
#         help_text="Valid Files: pdf, docx, doc, xls, xlsx, ppt, pptx, zip, rar, 7zip",
#         validators=[
#             FileExtensionValidator(
#                 [
#                     "pdf",
#                     "docx",
#                     "doc",
#                     "xls",
#                     "xlsx",
#                     "ppt",
#                     "pptx",
#                     "zip",
#                     "rar",
#                     "7zip",
#                 ]
#             )
#         ],
#     )
#     updated_date = models.DateTimeField(auto_now=True, auto_now_add=False, null=True)
#     upload_time = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

#     def __str__(self):
#         return str(self.file)[6:]


#     class Meta:
#         abstract = False
#         verbose_name = _("Upload File")
#         verbose_name_plural = _("Upload Files")


#     def get_extension_short(self):
#         ext = str(self.file).split(".")
#         ext = ext[len(ext) - 1]

#         if ext in ("doc", "docx"):
#             return "word"
#         elif ext == "pdf":
#             return "pdf"
#         elif ext in ("xls", "xlsx"):
#             return "excel"
#         elif ext in ("ppt", "pptx"):
#             return "powerpoint"
#         elif ext in ("zip", "rar", "7zip"):
#             return "archive"

#     def delete(self, *args, **kwargs):
#         self.file.delete()
#         super().delete(*args, **kwargs)


# @receiver(post_save, sender=Upload)
# def log_save(sender, instance, created, **kwargs):
#     if created:
#         ActivityLog.objects.create(
#             message=f"The file '{instance.title}' has been uploaded to the course '{instance.course}'."
#         )
#     else:
#         ActivityLog.objects.create(
#             message=f"The file '{instance.title}' of the course '{instance.course}' has been updated."
#         )


# @receiver(post_delete, sender=Upload)
# def log_delete(sender, instance, **kwargs):
#     ActivityLog.objects.create(
#         message=f"The file '{instance.title}' of the course '{instance.course}' has been deleted."
#     )









# class UploadVideo(models.Model):
#     title = models.CharField(max_length=100)
#     slug = models.SlugField(blank=True, unique=True)
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     video = models.FileField(
#         upload_to="course_videos/",
#         help_text="Valid video formats: mp4, mkv, wmv, 3gp, f4v, avi, mp3",
#         validators=[
#             FileExtensionValidator(["mp4", "mkv", "wmv", "3gp", "f4v", "avi", "mp3"])
#         ],
#     )
#     description = models.TextField(null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

#     def __str__(self):
#         return str(self.title)


#     class Meta:
#         abstract = False
#         verbose_name = _("Upload Video")
#         verbose_name_plural = _("Upload Videos")

#     def get_absolute_url(self):
#         return reverse(
#             "video_single", kwargs={"slug": self.course.slug, "video_slug": self.slug}
#         )

#     def delete(self, *args, **kwargs):
#         self.video.delete()
#         super().delete(*args, **kwargs)


# def video_pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)


# pre_save.connect(video_pre_save_receiver, sender=UploadVideo)


# @receiver(post_save, sender=UploadVideo)
# def log_save(sender, instance, created, **kwargs):
#     if created:
#         ActivityLog.objects.create(
#             message=f"The video '{instance.title}' has been uploaded to the course {instance.course}."
#         )
#     else:
#         ActivityLog.objects.create(
#             message=f"The video '{instance.title}' of the course '{instance.course}' has been updated."
#         )


# @receiver(post_delete, sender=UploadVideo)
# def log_delete(sender, instance, **kwargs):
#     ActivityLog.objects.create(
#         message=f"The video '{instance.title}' of the course '{instance.course}' has been deleted."
#     )







# class CourseOffer(models.Model):
#     """NOTE: Only department head can offer semester courses"""

#     dep_head = models.ForeignKey("accounts.DepartmentHead", on_delete=models.CASCADE)

#     def __str__(self):
#         return "{}".format(self.dep_head)











#########################################################
# Extra models
#############################################################
# class Session(models.Model):
#     session = models.CharField(max_length=200, unique=True)
#     is_current_session = models.BooleanField(default=False, blank=True, null=True)
#     next_session_begins = models.DateField(blank=True, null=True)

#     def __str__(self):
#         return self.session


# class Semester(models.Model):
#     semester = models.CharField(max_length=10, choices=SEMESTER, blank=True)
#     is_current_semester = models.BooleanField(default=False, blank=True, null=True)
#     session = models.ForeignKey(
#         Session, on_delete=models.CASCADE, blank=True, null=True
#     )
#     next_semester_begins = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return self.semester


class ActivityLog(models.Model):
    message = models.TextField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.created}]{self.message}"


