from django.shortcuts import render, redirect
from .models import Photos
from django.http import HttpResponse
from django.contrib import messages
import asyncio
# Create your views here.

def photoszone_view(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if photo:
            new_photo = Photos(
                photos=photo,
                title=title if title else '',
                description=description if description else '',
                size='',
                share_link='',
                share_title=title if title else ''
            )
            new_photo.save()
            messages.success(request, 'Фотографію успішно завантажено!')
            return redirect('photozone_sys:photos')
        else:
            messages.error(request, 'Будь ласка, виберіть фотографію для завантаження.')
    
    try:
        photos_list = Photos.objects.all()
        content = {"photos": photos_list}
    except Photos.DoesNotExist:
        photos_list = []
        content = {"photos": photos_list}
    
    return render(request=request, template_name='photozone_sys/photos.html', context=content)