from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Hall


# Create your views here.
def home(request):
    # ctx = {"user": {"is_authenticated": True}}
    ctx = {}
    return render(request, "app_halls/dashboard.html", ctx)


def dashboard(request):
    pass


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

    def form_valid(self, form):
        view_form = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get("username"), form.cleaned_data.get(
            "password1"
        )
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return view_form

    # def get_context_data(self, **kwargs):
    #     context = super(SignUp, self).get_context_data(**kwargs)
    #     context.update({"user": {"is_authenticated": True}})
    #     return context


class CreateHall(generic.CreateView):
    model = Hall
    fields = ["title"]
    template_name = "app_halls/create_hall.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        super(CreateHall, self).form_valid(form)
        return redirect(reverse_lazy("home"))


class DetailHall(generic.DetailView):
    model = Hall
    template_name = "app_halls/detail_hall.html"


class UpdateHall(generic.CreateView):
    pass


class DeleteHall(generic.CreateView):
    pass
