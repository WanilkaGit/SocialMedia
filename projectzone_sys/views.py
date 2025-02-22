from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Project, ProjectFile, ProjectsComments

def projectszone_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        share_link = request.POST.get('share_link')
        share_title = request.POST.get('share_title')
        
        # Створюємо новий проект
        new_project = Project(
            title=title,
            description=description,
            share_link=share_link,
            share_title=share_title
        )
        new_project.save()

        # Обробка файлів
        files = request.FILES.getlist('data-files')  # Отримуємо список файлів
        for file in files:
            ProjectFile.objects.create(project=new_project, file=file, size=file.size)

        messages.success(request, 'Дані успішно завантажено!')
        return redirect('projectszone_sys:projects')
    
    data_list = Project.objects.all()
    content = {"data": data_list}
    
    return render(request=request, template_name='projectszone_sys/project.html', context=content)

def add_project_comment(request, project_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        project = Project.objects.get(id=project_id)
        
        if text and author:
            comment = ProjectsComments.objects.create(text=text, author=author)
            comment.project.add(project)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('projectzone_sys:project_detail', project_id=project_id)