from django.urls import path

from . import views


app_name = "pages"

urlpatterns = [
    path("1988/", views.year_1988, name="year_1988"),
    path("about/", views.about, name="about"),
    path("governance/", views.governance, name="governance"),
    path("safety/", views.safety, name="safety"),
    path("privacy/", views.privacy, name="privacy"),
    path("conduct/", views.conduct, name="conduct"),
    path("get-involved/", views.get_involved, name="get_involved"),
    path("contact/", views.contact, name="contact"),
]
