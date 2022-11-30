from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from .models import Hall

# Create your views here.
def home(request):
    # ctx = {"user": {"is_authenticated": True}}
    ctx = {}
    return render(request, "app_halls/home.html", ctx)


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    # def get_context_data(self, **kwargs):
    #     context = super(SignUp, self).get_context_data(**kwargs)
    #     context.update({"user": {"is_authenticated": True}})
    #     return context


class CreateHall(generic.CreateView):
    model = Hall
    fields = ["title"]
    template_name = "app_halls/create_hall.html"
    success_url = reverse_lazy("home")
