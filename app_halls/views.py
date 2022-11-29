from django.shortcuts import render

# Create your views here.
def home(request):
    ctx = {"user": {"is_authenticated": True}}
    return render(request, "app_halls/home.html", ctx)
