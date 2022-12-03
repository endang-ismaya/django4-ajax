import urllib
import requests

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.http import Http404, JsonResponse
from django.forms.utils import ErrorList

from .models import Hall, Video
from .forms import SearchForm, VideoForm
from dotenv import load_dotenv

load_dotenv()

# from django.forms import formset_factory


# Create your views here.
def home(request):
    ctx = {}
    return render(request, "app_halls/home.html", ctx)

def dashboard(request):
    ctx = {}
    return render(request, "app_halls/dashboard.html", ctx)

def video_search(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        encoded_term = urllib.parse.quote(search_form.cleaned_data["search_term"])
        response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={encoded_term}&key={settings.YOUTUBE_API_KEYS}")
        json = response.json()
        return JsonResponse({"data": json})
    return JsonResponse({"data": "null"})

def add_video(request, pk):
    form = VideoForm
    search_form = SearchForm()
    hall = Hall.objects.get(pk=pk)

    if not hall.user == request.user:
        raise Http404

    if request.method == "POST":
        """CREATE"""
        form = VideoForm(request.POST)

        if form.is_valid():
            video = Video()
            video.hall = hall
            video.url = form.cleaned_data["url"]

            parsed_url = urllib.parse.urlparse(video.url)
            video_id = urllib.parse.parse_qs(parsed_url.query).get("v")

            if video_id:
                video.youtube_id = video_id[0]
                response = requests.get(f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={settings.YOUTUBE_API_KEYS}")
                json = response.json()
                title = json["items"][0]['snippet']['title']
                video.title = title
                video.save()
                return redirect("detail_hall", pk)
            else:
                errors = form._errors.setdefault("url", ErrorList())
                errors.append("please provide a valid Youtube's URL")

    ctx = {"form": form, "search_form": search_form, "hall": hall}
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
