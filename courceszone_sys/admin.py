from django.contrib import admin
from .models import Cources, Lessons, LessonFile

# Реєстрація моделі Cources
@admin.register(Cources)
class CourcesAdmin(admin.ModelAdmin):
    list_display = ('c_title', 'c_type', 'c_prize', 'c_rating', 'c_bye_count')  # Поля для відображення в списку
    search_fields = ('c_title',)  # Поле для пошуку
    list_filter = ('c_type',)  # Фільтр за типом курсу
    ordering = ('-c_uploaded',)  # Сортування за датою завантаження

# Реєстрація моделі Lessons
@admin.register(Lessons)
class LessonsAdmin(admin.ModelAdmin):
    list_display = ('l_title', 'l_time')  # Поля для відображення в списку
    search_fields = ('l_title',)  # Поле для пошуку

# Реєстрація моделі LessonFile
@admin.register(LessonFile)
class LessonFileAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'file')  # Поля для відображення в списку 