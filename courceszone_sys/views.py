from django.shortcuts import render, redirect
from .models import Cources, Lessons
from django.contrib import messages
from .forms import CreatCourceForm, CreateLessonForm

# Create your views here.

def ncourse_view(request):
    if request.method == 'POST':
        # Отримання даних з форми
        c_title = request.POST.get('c_title')
        c_description = request.POST.get('c_description')
        c_type = request.POST.get('c_type')
        c_prize = request.POST.get('c_prize')
        c_addeting_files = request.POST.get('c_addeting_files') == 'on'  # Перевірка на checkbox
        c_files = request.POST.get('c_files')
        c_pay_choices = request.POST.get('c_pay_choices')

        # Перевірка наявності всіх необхідних полів
        if c_title and c_description and c_type and c_prize and c_pay_choices:
            # Створення нового об'єкта Cources
            new_course = Cources(
                c_title=c_title,
                c_description=c_description,
                c_type=c_type,
                c_prize=c_prize,
                c_addeting_files=c_addeting_files,
                c_files=c_files,
                c_pay_choices=c_pay_choices
            )
            new_course.save()  # Збереження в базі даних
            messages.success(request, "Курс додано до списку")
            return redirect("index_o_info")
        else:
            messages.error(request, "Будь ласка, заповніть всі обов'язкові поля.")
    return render(request, "index_o_info.html")

def nlesson_view(request):
    if request.method == "POST":
        c_id = request.POST.get("c_id")
        form = CreateLessonForm(request.POST)
        if form.is_valid():
            nlesson = form.save()
            addicted_course = Cources.objects.get(id=c_id)
            addicted_course.c_lessons.add(nlesson)
            addicted_course.save()
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, SOS, we have trouble form is not valid")
    else:
        messages.error(request, "Capitan, method not POST you fucken DUMN")
    messages.error(request, "Capitan, SOS, we have trouble some requirment fields is NONE")

def videocos_view(request):
    cources = Cources.objects.filter(c_type="video")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)
    
def audiocos_view(request):
    cources = Cources.objects.filter(c_type="audio")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)
    
def photocos_view(request):
    cources = Cources.objects.filter(c_type="photos")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)

def model3dcos_view(request):
    cources = Cources.objects.filter(c_type="3d-models")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)

def codecos_view(request):
    cources = Cources.objects.filter(c_type="code")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)

def financecos_view(request):
    cources = Cources.objects.filter(c_type="finance")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)

def cryptographycos_view(request):
    cources = Cources.objects.filter(c_type="cryptography")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)

def scincecos_view(request):
    cources = Cources.objects.filter(c_type="science")
    if cources:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": ""
        }
    else:
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources,
            "special_message": "We found none cources, but you can create your own"
        }
    return render(request, "cources/cources.html", context=context)



