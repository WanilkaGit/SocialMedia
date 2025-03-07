from django.shortcuts import render, redirect
from .models import Cources, Lessons
from .forms import CourcesForm, LessonsForm
from django.contrib import messages

# Create your views here.

def ncourse_view(request):
    if request.method == "POST":
        form = CourcesForm(request.POST)
        if form.is_valid():
            ncourse = form.save()
            messages.success(request, "Курс додано до списку")
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, we have a trouble, you forgot to add something")
    else:
        form = CourcesForm()

    return render(request, 'create_cource.html', {'form': form})

def nlesson_view(request):
    if request.method == "POST":
        form = LessonsForm(request.POST, request.FILES)
        if form.is_valid():
            nlesson = form.save(commit=False)  # Не зберігаємо ще
            nlesson.save()  # Зберігаємо урок

            # Обробка завантажених файлів
            for file in request.FILES.getlist('l_file'):
                # Тут ви можете обробити кожен файл, якщо потрібно
                # Наприклад, зберегти їх у базі даних або в іншому місці
                pass

            messages.success(request, "Урок додано до курсу")
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, SOS, we have trouble some required fields are NONE")
    else:
        form = LessonsForm()

    return render(request, 'create_lesson.html', {'form': form})

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



