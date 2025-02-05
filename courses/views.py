# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib import messages
# from django.db.models import Sum, Avg, Max, Min, Count
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.views.generic import ListView, FormView, CreateView, View, DetailView, TemplateView, UpdateView, DeleteView
# from django.core.paginator import Paginator
# from django.conf import settings
# from django.utils.decorators import method_decorator
# from django.views.generic import ListView
# from django_filters.views import FilterView

# from accounts.models import User#, Student
# # from core.models import Session, Semester
# # from result.models import TakenCourse
# from accounts.decorators import lecturer_required, student_required
# from .forms import (
#     ProgramForm,
#     CourseAddForm,
#     CourseAllocationForm,
#     EditCourseAllocationForm,
#     UploadFormFile,
#     UploadFormVideo,
# )


import calendar
from decimal import Decimal, FloatOperation
from unicodedata import category
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Sum#, Avg, Count
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import View 
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from cme.mixins import (
    StaffRequiredMixin,
    LoginRequiredMixin,
    InsurerRequiredMixin,
    SubmitBtnMixin,
    AccountStaffRequiredMixin,
    MedicalStaffRequiredMixin,
    AjaxRequiredMixin,
    # FilterMixin
    )

# from .filters import ProgramFilter, CourseAllocationFilter
from plans.models import UserPlan
from .models import Course#, Upload, UploadVideo, Program










class CourseListView(ListView):
    model = Course
    template_name = "courses/course-list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(**kwargs)
        if self.request.user.is_authenticated:
            # user_courses = self.request.user.UserPlan.get_user_courses()
            # user_plan = self.request.user.UserPlan.plan.plan_type
            user_plan = UserPlan.objects.filter(user=self.request.user).first()
            ## qs = user_plan.get_plan_courses()
            qs = [] #user_plan.get_user_grade()
        else:
            qs = [] #qs.filter(level="0")

        query = self.request.GET.get("search")
        if query:
            qs = qs.filter(
                    Q(title__iexact=query)|
                    Q(description__icontains=query)
                    ).distinct()

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["course_list"] = Course.objects.all()
        return context






class CourseDetail(View):
    template_name = 'courses/course-detail.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})






class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    # form_class = PaymentForm
    template_name = 'courses/course-detail.html'

    # def get_object(self, *args, **kwargs):
    #     slug = self.kwargs.get("slug")
    #     ModelClass = self.model
    #     if slug is not None:
    #         try:
    #             obj = get_object_or_404(ModelClass, slug=slug)
    #             # print('===FRIEND NAME profile id===', obj.id)
    #             # print('===FRIEND NAME user id===', obj.user.id)
    #         except ModelClass.MultipleObjectsReturned:
    #             obj = ModelClass.objects.filter(slug=slug).order_by("timestamp").first()
    #             # print('===FRIEND NAME except===', obj)
    #     else:
    #         obj = super().get_object(*args, **kwargs)
    #     return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        
        if self.request.user.is_authenticated:
            user_plan = UserPlan.objects.filter(user=self.request.user).first()
            course_list = user_plan.get_plan_courses()
        else:
            course_list = Course.objects.all().filter(level="0")

        context["course_list"] = course_list
        # context["sum_amount_due"] = self.get_queryset().aggregate(Sum('amount_due'))['amount_due__sum']
        # context["sum_amount_paid"] = self.get_queryset().aggregate(Sum('amount_paid'))['amount_paid__sum']
        # context["sum_amount_pending"] = self.get_queryset().aggregate(Sum('amount_pending'))['amount_pending__sum']
        # context["instance"] = NhisPac.objects.get(code=instance.code)
        return context



# class CourseDetailView(LoginRequiredMixin, DetailView):
#     model = Course
#     template_name = "courses/course-detail.html"



# get_absolute_url



# class CapitationCreateView(InsurerRequiredMixin, CreateView):
#     model = Course
#     template_name = "capitation/capitation_form.html"
#     form_class = CapitationForm
#     # success_url = reverse_lazy('authcode:nhis')

#     def form_valid(self, form):
#         # form.instance.user = self.request.user
#         # form.instance.staff_email = self.request.user.email
#         # form.instance.staff_id = self.request.user.profile.staff_id
#         # form.instance.rate = 750
#         valid_data = super().form_valid(form)
#         messages.success(self.request, "Course Added.")
#         return valid_data

#     # def get_success(self):
#     #   return reverse("authcode:nhis_code_detail", pk=id)

#     def get_context_data(self, *args, **kwargs):
#       context = super().get_context_data(*args, **kwargs)
#       context["provider_list"] = Provider.objects.all() 
#       return context






# class CapitationUpdateView(InsurerRequiredMixin, UpdateView):
#     model = Course
#     template_name = "capitation/capitation_form.html"
#     form_class = CapitationForm 
#     # success_url = reverse_lazy('capitation:list')
#     # submit_btn = "Update Product"

#     # def get_initial(self):
#     #     initial = super().get_initial()
#     #     tags = self.get_object().tag_set.all()
#     #     initial["tags"] = ", ".join([x.title for x in tags])
#     #     """
#     #     tag_list = []
#     #     for x in tags:
#     #         tag_list.append(x.title)
#     #     """
#     #     return initial

#     def form_valid(self, form):
#         valid_data = super().form_valid(form)
#         messages.success(self.request, "Course Updated.")
#         return valid_data

#     def form_invalid(self, form):
#         messages.success(self.request, "Update Failed.")
#         return super().form_invalid(form)

#     def get_context_data(self, *args, **kwargs):
#       context = super().get_context_data(*args, **kwargs)
#       context["provider_list"] = Provider.objects.all() 
#       return context
 



























# @method_decorator([login_required], name="dispatch")
# class ProgramFilterView(FilterView):
#     filterset_class = ProgramFilter
#     template_name = "course/program_list.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Programs"
#         return context


# @login_required
# @lecturer_required
# def program_add(request):
#     if request.method == "POST":
#         form = ProgramForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, request.POST.get("title") + " program has been created."
#             )
#             return redirect("programs")
#         else:
#             messages.error(request, "Correct the error(S) below.")
#     else:
#         form = ProgramForm()

#     return render(
#         request,
#         "course/program_add.html",
#         {
#             "title": "Add Program",
#             "form": form,
#         },
#     )


# @login_required
# def program_detail(request, pk):
#     program = Program.objects.get(pk=pk)
#     courses = Course.objects.filter(program_id=pk).order_by("-year")
#     credits = Course.objects.aggregate(Sum("credit"))

#     paginator = Paginator(courses, 10)
#     page = request.GET.get("page")

#     courses = paginator.get_page(page)

#     return render(
#         request,
#         "course/program_single.html",
#         {
#             "title": program.title,
#             "program": program,
#             "courses": courses,
#             "credits": credits,
#         },
#     )


# @login_required
# @lecturer_required
# def program_edit(request, pk):
#     program = Program.objects.get(pk=pk)

#     if request.method == "POST":
#         form = ProgramForm(request.POST, instance=program)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, str(request.POST.get("title")) + " program has been updated."
#             )
#             return redirect("programs")
#     else:
#         form = ProgramForm(instance=program)

#     return render(
#         request,
#         "course/program_add.html",
#         {"title": "Edit Program", "form": form},
#     )


# @login_required
# @lecturer_required
# def program_delete(request, pk):
#     program = Program.objects.get(pk=pk)
#     title = program.title
#     program.delete()
#     messages.success(request, "Program " + title + " has been deleted.")

#     return redirect("programs")


# # ########################################################


# # ########################################################
# # Course views
# # ########################################################
# @login_required
# def course_single(request, slug):
#     course = Course.objects.get(slug=slug)
#     files = Upload.objects.filter(course__slug=slug)
#     videos = UploadVideo.objects.filter(course__slug=slug)

#     # lecturers = User.objects.filter(allocated_lecturer__pk=course.id)
#     lecturers = CourseAllocation.objects.filter(courses__pk=course.id)

#     return render(
#         request,
#         "course/course_single.html",
#         {
#             "title": course.title,
#             "course": course,
#             "files": files,
#             "videos": videos,
#             "lecturers": lecturers,
#             "media_url": settings.MEDIA_ROOT,
#         },
#     )


# @login_required
# @lecturer_required
# def course_add(request, pk):
#     users = User.objects.all()
#     if request.method == "POST":
#         form = CourseAddForm(request.POST)
#         course_name = request.POST.get("title")
#         course_code = request.POST.get("code")
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, (course_name + "(" + course_code + ")" + " has been created.")
#             )
#             return redirect("program_detail", pk=request.POST.get("program"))
#         else:
#             messages.error(request, "Correct the error(s) below.")
#     else:
#         form = CourseAddForm(initial={"program": Program.objects.get(pk=pk)})

#     return render(
#         request,
#         "course/course_add.html",
#         {
#             "title": "Add Course",
#             "form": form,
#             "program": pk,
#             "users": users,
#         },
#     )


# @login_required
# @lecturer_required
# def course_edit(request, slug):
#     course = get_object_or_404(Course, slug=slug)
#     if request.method == "POST":
#         form = CourseAddForm(request.POST, instance=course)
#         course_name = request.POST.get("title")
#         course_code = request.POST.get("code")
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, (course_name + "(" + course_code + ")" + " has been updated.")
#             )
#             return redirect("program_detail", pk=request.POST.get("program"))
#         else:
#             messages.error(request, "Correct the error(s) below.")
#     else:
#         form = CourseAddForm(instance=course)

#     return render(
#         request,
#         "course/course_add.html",
#         {
#             "title": "Edit Course",
#             # 'form': form, 'program': pk, 'course': pk
#             "form": form,
#         },
#     )


# @login_required
# @lecturer_required
# def course_delete(request, slug):
#     course = Course.objects.get(slug=slug)
#     # course_name = course.title
#     course.delete()
#     messages.success(request, "Course " + course.title + " has been deleted.")

#     return redirect("program_detail", pk=course.program.id)


# # ########################################################


# # ########################################################
# # Course Allocation
# # ########################################################
# @method_decorator([login_required], name="dispatch")
# class CourseAllocationFormView(CreateView):
#     form_class = CourseAllocationForm
#     template_name = "course/course_allocation_form.html"

#     def get_form_kwargs(self):
#         kwargs = super(CourseAllocationFormView, self).get_form_kwargs()
#         kwargs["user"] = self.request.user
#         return kwargs

#     def form_valid(self, form):
#         # if a staff has been allocated a course before update it else create new
#         lecturer = form.cleaned_data["lecturer"]
#         selected_courses = form.cleaned_data["courses"]
#         courses = ()
#         for course in selected_courses:
#             courses += (course.pk,)
#         # print(courses)

#         try:
#             a = CourseAllocation.objects.get(lecturer=lecturer)
#         except:
#             a = CourseAllocation.objects.create(lecturer=lecturer)
#         for i in range(0, selected_courses.count()):
#             a.courses.add(courses[i])
#             a.save()
#         return redirect("course_allocation_view")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Assign Course"
#         return context


# @method_decorator([login_required], name="dispatch")
# class CourseAllocationFilterView(FilterView):
#     filterset_class = CourseAllocationFilter
#     template_name = "course/course_allocation_view.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = "Course Allocations"
#         return context


# @login_required
# @lecturer_required
# def edit_allocated_course(request, pk):
#     allocated = get_object_or_404(CourseAllocation, pk=pk)
#     if request.method == "POST":
#         form = EditCourseAllocationForm(request.POST, instance=allocated)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "course assigned has been updated.")
#             return redirect("course_allocation_view")
#     else:
#         form = EditCourseAllocationForm(instance=allocated)

#     return render(
#         request,
#         "course/course_allocation_form.html",
#         {"title": "Edit Course Allocated", "form": form, "allocated": pk},
#     )


# @login_required
# @lecturer_required
# def deallocate_course(request, pk):
#     course = CourseAllocation.objects.get(pk=pk)
#     course.delete()
#     messages.success(request, "successfully deallocate!")
#     return redirect("course_allocation_view")


# # ########################################################


# # ########################################################
# # File Upload views
# # ########################################################
# @login_required
# @lecturer_required
# def handle_file_upload(request, slug):
#     course = Course.objects.get(slug=slug)
#     if request.method == "POST":
#         form = UploadFormFile(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.course = course
#             obj.save()

#             messages.success(
#                 request, (request.POST.get("title") + " has been uploaded.")
#             )
#             return redirect("course_detail", slug=slug)
#     else:
#         form = UploadFormFile()
#     return render(
#         request,
#         "upload/upload_file_form.html",
#         {"title": "File Upload", "form": form, "course": course},
#     )


# @login_required
# @lecturer_required
# def handle_file_edit(request, slug, file_id):
#     course = Course.objects.get(slug=slug)
#     instance = Upload.objects.get(pk=file_id)
#     if request.method == "POST":
#         form = UploadFormFile(request.POST, request.FILES, instance=instance)
#         # file_name = request.POST.get('name')
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, (request.POST.get("title") + " has been updated.")
#             )
#             return redirect("course_detail", slug=slug)
#     else:
#         form = UploadFormFile(instance=instance)

#     return render(
#         request,
#         "upload/upload_file_form.html",
#         {"title": instance.title, "form": form, "course": course},
#     )


# def handle_file_delete(request, slug, file_id):
#     file = Upload.objects.get(pk=file_id)
#     # file_name = file.name
#     file.delete()

#     messages.success(request, (file.title + " has been deleted."))
#     return redirect("course_detail", slug=slug)


# # ########################################################
# # Video Upload views
# # ########################################################
# @login_required
# @lecturer_required
# def handle_video_upload(request, slug):
#     course = Course.objects.get(slug=slug)
#     if request.method == "POST":
#         form = UploadFormVideo(request.POST, request.FILES)
#         if form.is_valid():
#             obj = form.save(commit=False)
#             obj.course = course
#             obj.save()

#             messages.success(
#                 request, (request.POST.get("title") + " has been uploaded.")
#             )
#             return redirect("course_detail", slug=slug)
#     else:
#         form = UploadFormVideo()
#     return render(
#         request,
#         "upload/upload_video_form.html",
#         {"title": "Video Upload", "form": form, "course": course},
#     )


# @login_required
# # @lecturer_required
# def handle_video_single(request, slug, video_slug):
#     course = get_object_or_404(Course, slug=slug)
#     video = get_object_or_404(UploadVideo, slug=video_slug)
#     return render(request, "upload/video_single.html", {"video": video})


# @login_required
# @lecturer_required
# def handle_video_edit(request, slug, video_slug):
#     course = Course.objects.get(slug=slug)
#     instance = UploadVideo.objects.get(slug=video_slug)
#     if request.method == "POST":
#         form = UploadFormVideo(request.POST, request.FILES, instance=instance)
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, (request.POST.get("title") + " has been updated.")
#             )
#             return redirect("course_detail", slug=slug)
#     else:
#         form = UploadFormVideo(instance=instance)

#     return render(
#         request,
#         "upload/upload_video_form.html",
#         {"title": instance.title, "form": form, "course": course},
#     )


# def handle_video_delete(request, slug, video_slug):
#     video = get_object_or_404(UploadVideo, slug=video_slug)
#     # video = UploadVideo.objects.get(slug=video_slug)
#     video.delete()

#     messages.success(request, (video.title + " has been deleted."))
#     return redirect("course_detail", slug=slug)


# # ########################################################


# # ########################################################
# # Course Registration
# # ########################################################
# # @login_required
# # @student_required
# # def course_registration(request):
# #     if request.method == "POST":
# #         student = [] #Student.objects.get(student__pk=request.user.id)
# #         ids = ()
# #         data = request.POST.copy()
# #         data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
# #         for key in data.keys():
# #             ids = ids + (str(key),)
# #         for s in range(0, len(ids)):
# #             course = Course.objects.get(pk=ids[s])
# #             obj = TakenCourse.objects.create(student=student, course=course)
# #             obj.save()
# #         messages.success(request, "Courses registered successfully!")
# #         return redirect("course_registration")
# #     else:
# #         current_semester = [] #Semester.objects.filter(is_current_semester=True).first()
# #         if not current_semester:
# #             messages.error(request, "No active semester found.")
# #             return render(request, "course/course_registration.html")

# #         # student = [] #Student.objects.get(student__pk=request.user.id)
# #         student = [] #get_object_or_404(Student, student__id=request.user.id)
# #         taken_courses = TakenCourse.objects.filter(student__student__id=request.user.id)
# #         t = ()
# #         for i in taken_courses:
# #             t += (i.course.pk,)

# #         courses = (
# #             Course.objects.filter(
# #                 program__pk=student.program.id,
# #                 level=student.level,
# #                 semester=current_semester,
# #             )
# #             .exclude(id__in=t)
# #             .order_by("year")
# #         )
# #         all_courses = Course.objects.filter(
# #             level=student.level, program__pk=student.program.id
# #         )

# #         no_course_is_registered = False  # Check if no course is registered
# #         all_courses_are_registered = False

# #         registered_courses = Course.objects.filter(level=student.level).filter(id__in=t)
# #         if (
# #             registered_courses.count() == 0
# #         ):  # Check if number of registered courses is 0
# #             no_course_is_registered = True

# #         if registered_courses.count() == all_courses.count():
# #             all_courses_are_registered = True

# #         total_first_semester_credit = 0
# #         total_sec_semester_credit = 0
# #         total_registered_credit = 0
# #         for i in courses:
# #             if i.semester == "First":
# #                 total_first_semester_credit += int(i.credit)
# #             if i.semester == "Second":
# #                 total_sec_semester_credit += int(i.credit)
# #         for i in registered_courses:
# #             total_registered_credit += int(i.credit)
# #         context = {
# #             "is_calender_on": True,
# #             "all_courses_are_registered": all_courses_are_registered,
# #             "no_course_is_registered": no_course_is_registered,
# #             "current_semester": current_semester,
# #             "courses": courses,
# #             "total_first_semester_credit": total_first_semester_credit,
# #             "total_sec_semester_credit": total_sec_semester_credit,
# #             "registered_courses": registered_courses,
# #             "total_registered_credit": total_registered_credit,
# #             "student": student,
# #         }
# #         return render(request, "course/course_registration.html", context)


# # @login_required
# # @student_required
# # def course_drop(request):
# #     if request.method == "POST":
# #         student = [] #Student.objects.get(student__pk=request.user.id)
# #         ids = ()
# #         data = request.POST.copy()
# #         data.pop("csrfmiddlewaretoken", None)  # remove csrf_token
# #         for key in data.keys():
# #             ids = ids + (str(key),)
# #         for s in range(0, len(ids)):
# #             course = Course.objects.get(pk=ids[s])
# #             obj = TakenCourse.objects.get(student=student, course=course)
# #             obj.delete()
# #         messages.success(request, "Successfully Dropped!")
# #         return redirect("course_registration")


# # # ########################################################


# # @login_required
# # def user_course_list(request):
# #     if request.user.is_lecturer:
# #         courses = Course.objects.filter(allocated_course__lecturer__pk=request.user.id)

# #         return render(request, "course/user_course_list.html", {"courses": courses})

# #     elif request.user.is_student:
# #         student = [] #Student.objects.get(student__pk=request.user.id)
# #         taken_courses = TakenCourse.objects.filter(
# #             student__student__id=student.student.id
# #         )
# #         courses = Course.objects.filter(level=student.level).filter(
# #             program__pk=student.program.id
# #         )

# #         return render(
# #             request,
# #             "course/user_course_list.html",
# #             {"student": student, "taken_courses": taken_courses, "courses": courses},
# #         )

# #     else:
# #         return render(request, "course/user_course_list.html")
