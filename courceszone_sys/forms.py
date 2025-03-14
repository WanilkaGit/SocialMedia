from django import forms
from .models import Lessons, Cources


class CreatCourceForm(forms.ModelForm):
    class Meta:
        model = Cources
        exclude = ["c_uploaded", "c_lessons", "c_rating", "c_bye_count"]

class CreateLessonForm(forms.ModelForm):
    class Meta:
        model = Lessons
        exclude = ["lc_id"]
        help_texts = {
            "l_title": "Введіть повну назву книги.",
        }