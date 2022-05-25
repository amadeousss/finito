from django import forms
from .models import Movie
import re


class MovieForm(forms.Form):
    # def __init__(self, runtime):
    #     super().__init__()
    minutes_seen = forms.IntegerField(label=f'Minutes seen', min_value=0, max_value=500)
    is_fully_seen = forms.BooleanField(label='Seen fully', required=False)
    #
    # @classmethod
    # def get_form(cls, runtime):
    #     cls.minutes_seen.max_value
    #     return cls
