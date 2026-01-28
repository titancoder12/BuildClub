from django.shortcuts import render


def about(request):
    return render(request, "pages/about.html")


def governance(request):
    return render(request, "pages/governance.html")


def safety(request):
    return render(request, "pages/safety.html")


def privacy(request):
    return render(request, "pages/privacy.html")


def conduct(request):
    return render(request, "pages/conduct.html")


def get_involved(request):
    return render(request, "pages/get_involved.html")


def contact(request):
    return render(request, "pages/contact.html")


def year_1988(request):
    return render(request, "pages/1988.html")
