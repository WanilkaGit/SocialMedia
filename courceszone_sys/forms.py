from django import forms
from .models import Lessons, Cources


class CreatCourceForm():
    class Meta:
        model = Cources
        fields = ["c_title",]
        exclude = ["c_uploaded", "c_lessons", "c_rating", "c_bye_count"]
        help_texts = {
            "c_title": "Введіть повну назву",
        }

class CreateLessonForm():
    class Meta:
        model = Lessons
        exclude = ["lc_id"]
        help_texts = {
            "l_title": "Введіть повну назву книги.",
        }