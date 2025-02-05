from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.urls import reverse

from django.db.models import Q
from PIL import Image

# from course.models import Program
from .validators import ASCIIUsernameValidator






# LEVEL_COURSE = "Level course"
BASIC = "Basic"
STANDARD = "Standard"

PACKAGE = (
    # (LEVEL_COURSE, "Level course"),
    (BASIC, "Basic"),
    (STANDARD, "Standard"),
)


# def image_location(instance, filename):
#     # filebase = filename.split(".")[0]
#     return "profiles/%s/photos/%s" %(instance.user, filename)


# def image_validator(fieldfile_obj):
#     filesize = fieldfile_obj.size
#     megabyte_limit = 1.0
#     if filesize > megabyte_limit*1024*1024:
#         raise ValidationError("Image too large, Maximum size allowed is %sMB" %(megabyte_limit))




class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query is not None:
            or_lookup = (
                Q(username__icontains=query)
                | Q(first_name__icontains=query)
                | Q(last_name__icontains=query)
                | Q(email__icontains=query)
            )
            queryset = queryset.filter(
                or_lookup
            ).distinct()  # distinct() is often necessary with Q lookups
        return queryset


GENDERS = (("M", "Male"), ("F", "Female"))
# USER_TYPE = (('student','STUDENT'), ('instructor','INSTRUCTOR'), ('manager','MANAGER'))

class User(AbstractUser):
    phone = models.CharField(max_length=17, blank=True, null=True, validators=[RegexValidator(regex='^[0-9]{9,15}$', message='Please enter a valid phone number', code='invalid number')])
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(max_length=60, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    picture = models.ImageField(
        upload_to="profile_pictures/", default="default.png", null=True
    )
    username_validator = ASCIIUsernameValidator()
    # user_type = models.CharField(max_length=24, choices=USER_TYPE, default='student')
    is_student = models.BooleanField(default=False)
    is_instructor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    objects = CustomUserManager()

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return "{} ({})".format(self.username, self.get_full_name)
    
    @property
    def is_student(self):
        return self.is_student
        # if self.is_student == True:
        #     return True
        # else:
        #     return False
    
    @property
    def is_instructor(self):
        return self.is_instructor
        # if self.is_instructor == True:
        #     return True
        # else:
        #     return False
    
    @property
    def is_manager(self):
        return self.is_manager
        # if self.is_student == True:
        #     return True
        # else:
        #     return False

    @property
    def get_full_name(self):
        full_name = self.username
        if self.first_name and self.last_name:
            full_name = self.first_name + " " + self.last_name
        return full_name

    @classmethod
    def get_student_count(cls):
        return cls.objects.filter(is_student=True).count()

    @classmethod
    def get_instructor_count(cls):
        return cls.objects.filter(is_instructor=True).count()

    @classmethod
    def get_manager_count(cls):
        return cls.objects.filter(is_manager=True).count()

    @property
    def get_user_role(self):
        if self.is_superuser:
            role = "Admin"
        elif self.is_manager:
            role = "Manager"
        elif self.is_instructor:
            role = "Instructor"
        elif self.is_student:
            role = "Student"

        return role

    def get_picture(self):
        try:
            return self.picture.url
        except:
            no_picture = settings.MEDIA_URL + "default.png"
            return no_picture

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.picture.path)
        except:
            pass

    def delete(self, *args, **kwargs):
        if self.picture.url != settings.MEDIA_URL + "default.png":
            self.picture.delete()
        super().delete(*args, **kwargs)


# class StudentManager(models.Manager):
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query is not None:
#             or_lookup = Q(level__icontains=query) | Q(program__icontains=query)
#             qs = qs.filter(
#                 or_lookup
#             ).distinct()  # distinct() is often necessary with Q lookups
#         return qs


# class Student(models.Model):
#     student = models.OneToOneField(User, on_delete=models.CASCADE)
#     # id_number = models.CharField(max_length=20, unique=True, blank=True)
#     package = models.CharField(max_length=25, choices=PACKAGE, null=True)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

#     objects = StudentManager()

#     class Meta:
#         ordering = ("-student__date_joined",)

#     def __str__(self):
#         return self.student.get_full_name

#     @classmethod
#     def get_gender_count(cls):
#         males_count = Student.objects.filter(student__gender="M").count()
#         females_count = Student.objects.filter(student__gender="F").count()

#         return {"M": males_count, "F": females_count}

#     def get_absolute_url(self):
#         return reverse("profile_single", kwargs={"id": self.id})

#     def delete(self, *args, **kwargs):
#         self.student.delete()
#         super().delete(*args, **kwargs)


# # class Parent(models.Model):
# #     """
# #     Connect student with their parent, parents can
# #     only view their connected students information
# #     """

# #     user = models.OneToOneField(User, on_delete=models.CASCADE)
# #     student = models.OneToOneField(Student, null=True, on_delete=models.SET_NULL)
# #     first_name = models.CharField(max_length=120)
# #     last_name = models.CharField(max_length=120)
# #     phone = models.CharField(max_length=60, blank=True, null=True)
# #     email = models.EmailField(blank=True, null=True)

# #     # What is the relationship between the student and
# #     # the parent (i.e. father, mother, brother, sister)
# #     relation_ship = models.TextField(choices=RELATION_SHIP, blank=True)

# #     class Meta:
# #         ordering = ("-user__date_joined",)

# #     def __str__(self):
# #         return self.user.username


# class Manager(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True)

#     class Meta:
#         ordering = ("-user__date_joined",)

#     def __str__(self):
#         return "{}".format(self.user)




# We create a one-to-one relation from EmailVerification to whichever User model our project is using through the AUTH_USER_MODEL setting.
class EmailVerification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="verification"
    )
    verified = models.BooleanField(default=False)


