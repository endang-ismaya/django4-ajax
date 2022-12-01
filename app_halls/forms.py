from .models import Video
from django import forms
from django.utils.translation import gettext_lazy as _


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ["title", "url", "youtube_id"]
        labels = {
            "title": _("Youtube Title"),
            "url": _("Youtube URL"),
            "youtube_id": _("Youtube ID"),
        }


class SearchForm(forms.Form):
    search_term = forms.CharField(max_length=255, label="Search for Videos:")
