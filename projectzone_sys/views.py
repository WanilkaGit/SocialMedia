from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Project, ProjectFile, ProjectsComments

def projectszone_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        share_link = request.POST.get('share_link')
        share_title = request.POST.get('share_title')

        # Переконайтеся, що користувач автентифікований
        if not request.user.is_authenticated:
            messages.error(request, "Ви повинні бути авторизовані для створення проекту.")
            return redirect('projectszone_sys:projects')

        # Створюємо новий проект
        new_project = Project.objects.create(
            title=title,
            description=description,
            share_link=share_link,
            share_title=share_title,
            user=request.user  # Додаємо користувача
        )

        # Обробка файлів
        files = request.FILES.getlist('data-files')
        for file in files:
            ProjectFile.objects.create(project=new_project, file=file, size=file.size)

        messages.success(request, 'Дані успішно завантажено!')
        return redirect('projectszone_sys:projects')

    data_list = Project.objects.all()
    return render(request, 'projectszone_sys/project.html', {"data": data_list})

def add_project_comment(request, project_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        project = get_object_or_404(Project, id=project_id)

        if not text:
            messages.error(request, 'Будь ласка, введіть коментар.')
            return redirect('projectszone_sys:project_detail', project_id=project_id)

        # Створюємо коментар
        ProjectsComments.objects.create(
            text=text,
            author=request.user,  # Використовуємо request.user
            project=project
        )

        messages.success(request, 'Коментар успішно додано!')
    
    return redirect('projectszone_sys:project_detail', project_id=project_id)
