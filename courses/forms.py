from django import forms
from accounts.models import User
from .models import Course#, Program, CourseAllocation, Upload, UploadVideo


# class ProgramForm(forms.ModelForm):
#     class Meta:
#         model = Program
#         fields = "__all__"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["title"].widget.attrs.update({"class": "form-control"})
#         self.fields["description"].widget.attrs.update({"class": "form-control"})


class CourseAddForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.update({"class": "form-control"})
        self.fields["code"].widget.attrs.update({"class": "form-control"})
        self.fields["description"].widget.attrs.update({"class": "form-control"})
        self.fields["video"].widget.attrs.update({"class": "form-control"})
        self.fields["upload_file"].widget.attrs.update({"class": "form-control"})
        # self.fields['courseUnit'].widget.attrs.update({'class': 'form-control'})
        # self.fields["credit"].widget.attrs.update({"class": "form-control"})
        # self.fields["year"].widget.attrs.update({"class": "form-control"})
        # self.fields["semester"].widget.attrs.update({"class": "form-control"})


# class CourseAllocationForm(forms.ModelForm):
#     courses = forms.ModelMultipleChoiceField(
#         queryset=Course.objects.all().order_by("level"),
#         widget=forms.CheckboxSelectMultiple(
#             attrs={"class": "browser-default checkbox"}
#         ),
#         required=True,
#     )
#     lecturer = forms.ModelChoiceField(
#         queryset=User.objects.filter(is_lecturer=True),
#         widget=forms.Select(attrs={"class": "browser-default custom-select"}),
#         label="lecturer",
#     )

#     class Meta:
#         model = CourseAllocation
#         fields = ["lecturer", "courses"]

#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop("user")
#         super(CourseAllocationForm, self).__init__(*args, **kwargs)
#         self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


# class EditCourseAllocationForm(forms.ModelForm):
#     courses = forms.ModelMultipleChoiceField(
#         queryset=Course.objects.all().order_by("level"),
#         widget=forms.CheckboxSelectMultiple,
#         required=True,
#     )
#     lecturer = forms.ModelChoiceField(
#         queryset=User.objects.filter(is_lecturer=True),
#         widget=forms.Select(attrs={"class": "browser-default custom-select"}),
#         label="lecturer",
#     )

#     class Meta:
#         model = CourseAllocation
#         fields = ["lecturer", "courses"]

#     def __init__(self, *args, **kwargs):
#         #    user = kwargs.pop('user')
#         super(EditCourseAllocationForm, self).__init__(*args, **kwargs)
#         self.fields["lecturer"].queryset = User.objects.filter(is_lecturer=True)


# # Upload files to specific course
# class UploadFormFile(forms.ModelForm):
#     class Meta:
#         model = Upload
#         fields = (
#             "title",
#             "file",
#         )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["title"].widget.attrs.update({"class": "form-control"})
#         self.fields["file"].widget.attrs.update({"class": "form-control"})


# # Upload video to specific course
# class UploadFormVideo(forms.ModelForm):
#     class Meta:
#         model = UploadVideo
#         fields = (
#             "title",
#             "video",
#         )

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["title"].widget.attrs.update({"class": "form-control"})
#         self.fields["video"].widget.attrs.update({"class": "form-control"})
