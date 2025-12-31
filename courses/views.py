from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import RegistrationForm
from .models import Course


def home(request):
    highlights = [
        {
            "title": "Build technology from the ground up",
            "body": (
                "Build Club teaches students how to build real systems step by step, "
                "not just follow tutorials."
            ),
        },
        {
            "title": "Hands-on learning with software + hardware",
            "body": (
                "Students create projects that connect software, logic, and physical "
                "components for a full picture of how technology works."
            ),
        },
        {
            "title": "Microcontrollers, processors, and 3D printing",
            "body": (
                "Hands-on exploration includes microcontrollers, processors, and "
                "designing and fabricating parts with 3D printing."
            ),
        },
    ]
    return render(
        request,
        "home.html",
        {
            "highlights": highlights,
        },
    )


def courses_list(request):
    courses = Course.objects.filter(published=True)
    return render(request, "courses/list.html", {"courses": courses})


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, published=True)
    return render(request, "courses/detail.html", {"course": course})


def course_register(request, slug):
    course = get_object_or_404(Course, slug=slug, published=True)
    if request.method == "POST":
        form = RegistrationForm(request.POST, course=course)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.course = course
            registration.save()
            return redirect(reverse("register_success"))
    else:
        form = RegistrationForm(course=course)
    return render(
        request,
        "courses/register.html",
        {
            "course": course,
            "form": form,
            "is_full": course.is_full(),
        },
    )


def register_success(request):
    return render(request, "courses/register_success.html")
