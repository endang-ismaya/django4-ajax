from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from .models import Hall, Video
from .forms import SearchForm, VideoForm

# from django.forms import formset_factory

# Create your views here.
def home(request):
    ctx = {}
    return render(request, "app_halls/home.html", ctx)


def dashboard(request):
    ctx = {}
    return render(request, "app_halls/dashboard.html", ctx)


def add_video(request, pk):
    form = VideoForm
    search_form = SearchForm()

    if request.method == "POST":
        """CREATE"""
        filled_form = VideoForm(request.POST)

        if filled_form.is_valid():
            video = Video()
            video.url = filled_form.cleaned_data["url"]
            video.title = filled_form.cleaned_data["title"]
            video.youtube_id = filled_form.cleaned_data["youtube_id"]
            video.hall = Hall.objects.get(pk=pk)
            video.save()

    ctx = {"form": form, "search_form": search_form}
    return render(request, "app_halls/add_video.html", ctx)


# def add_video(request, pk):
#     VideoFormSet = formset_factory(VideoForm, extra=5)
#     form = VideoFormSet
#     search_form = SearchForm()

#     if request.method == "POST":
#         """CREATE"""
#         filled_form = VideoFormSet(request.POST)

#         if filled_form.is_valid():

#             for form in filled_form:
#                 video = Video()
#                 video.url = filled_form.cleaned_data["url"]
#                 video.title = filled_form.cleaned_data["title"]
#                 video.youtube_id = filled_form.cleaned_data["youtube_id"]
#                 video.hall = Hall.objects.get(pk=pk)
#                 video.save()

#     ctx = {"form": form, "search_form": search_form}
#     return render(request, "app_halls/add_video.html", ctx)


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


class UpdateHall(generic.UpdateView):
    model = Hall
    template_name = "app_halls/update_hall.html"
    fields = ["title"]
    success_url = reverse_lazy("dashboard")


class DeleteHall(generic.DeleteView):
    model = Hall
    template_name = "app_halls/delete_hall.html"
    success_url = reverse_lazy("dashboard")
