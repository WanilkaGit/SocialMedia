from django.shortcuts import render, redirect
from .models import Cources, Lessons
from django.contrib import messages

# Create your views here.

def ncourse_view(request):
    if request.method == "POST":
        c_title = request.POST.get("c-title")
        c_description = request.POST.get("c-description")
        c_type = request.POST.get("c-type")
        c_prize = request.POST.get("c-prize")
        c_addeting_files = request.POST.get("c-addeting-files")
        c_files = request.POST.get("c-files")
        c_pay_choices = request.POST.get("c-pay-choices")

        if c_title and c_type and c_addeting_files and c_pay_choices:
            ncourse = Cources(
                c_title=c_title,
                c_description=c_description,
                c_type = c_type,
                c_prize=c_prize,
                c_addeting_files=c_addeting_files,
                c_files=c_files,
                c_pay_choices=c_pay_choices,
            )
            ncourse.save()
            messages.success(request, "Курс додано до списку")
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, we have a trouble, you furgot to add something")

def nlesson_view(request):
    if request.method == "POST":
        l_file = request.FILES.get("l-file")
        l_title = request.POST.get("l-title")
        l_description = request.POST.get("l-description")
        l_time = request.POST.get("l-time")
        lc_id = request.POST.get("l-id")
        l_course = request.POST.get("l_course")
        if l_title and lc_id and l_course:
            nlesson = Lessons(
                l_title=l_title,
                l_description=l_description,
                l_time=l_time,
                lc_id=lc_id,
            )
            nlesson.save()
            addicted_course = Cources.objects.get(id=l_course)
            addicted_course.c_lessons.add(nlesson)
            addicted_course.save()
            return redirect("index_o_info")
        else:
            messages.error(request, "Capitan, SOS, we have trouble some requirment fields is NONE")

def audiocos_view(request):
    if request.method == "POST":
        cources = Cources.objects.filter(c_type="video")
        context = {
            "title": "Couces that describes how to edit your videos",
            "cources": cources
        }
        return render(request, "cources/cources.html", context=context)



