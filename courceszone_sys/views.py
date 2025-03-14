from django.shortcuts import render, redirect
from .models import Cources, Lessons
from django.contrib import messages
from .forms import CreatCourceForm, CreateLessonForm

# Create your views here.

def ncourse_view(request):
    if request.method == "POST":
        form = CreatCourceForm(request.POST)
        if form.is_valid():
            ncourse = form.save()
            messages.success(request, "Курс додано до списку")
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, we have a trouble, you forgot to add something")
    else:
        form = CreatCourceForm()  # Створюємо нову форму для GET запиту

    return render(request, 'base_o_info.html', {'form': form})  # Змініть 'template_name.html' на ваш шаблон

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
    cources = Cources.objects.filter(c_type="Photos")
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



