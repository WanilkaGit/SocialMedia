from django.shortcuts import render, redirect
from .models import Photos, PhotosComments, Imgs4Designs, Imgs4DesignsComments
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
                size=photo.size,
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

def imgs_4_designs_view(request):
    if request.method == 'POST':
        img = request.FILES.get('image')
        title = request.POST.get('title')
        description = request.POST.get('description')

        if img:
            new_img = Imgs4Designs(
                    images=img,
                    title=title if title else '',
                    description=description if description else '',
                    size=img.size,
                    share_link='',
                    share_title=title if title else ''
                )
            new_img.save()
            messages.success(request=request, message="Ваший фото-дезайн завантажений")
            return redirect('photozone_sys:images')
        else:
            messages.error(request, 'Будь ласка, виберіть ваший дизайн для завантаження для завантаження.')

    try:
        imgs_list = Imgs4Designs.objects.all()
        content = {"imgs": imgs_list}
    except Imgs4Designs.DoesNotExist:
        imgs_list = []
        content = {"imgs": imgs_list}
    
    return render(request=request, template_name='photozone_sys/imgs.html', context=content)

def add_photo_comment(request, photo_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        photo = Photos.objects.get(id=photo_id)
        
        if text and author:
            comment = PhotosComments.objects.create(text=text, author=author)
            comment.photo.add(photo)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('photozone_sys:photo_detail', photo_id=photo_id)

def add_image_comment(request, image_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        image = Imgs4Designs.objects.get(id=image_id)
        
        if text and author:
            comment = Imgs4DesignsComments.objects.create(text=text, author=author)
            comment.image.add(image)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('photozone_sys:image_detail', image_id=image_id)