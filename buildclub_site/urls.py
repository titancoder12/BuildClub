from django.contrib import admin
from django.urls import include, path

from courses import views as course_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", course_views.home, name="home"),
    path("register/success/", course_views.register_success, name="register_success"),
    path("courses/", include("courses.urls")),
]
