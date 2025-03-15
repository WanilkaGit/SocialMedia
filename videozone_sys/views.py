from django.shortcuts import render, redirect
from .models import LongVideo, ShortVideo, ShortVideoComments, LongVideoComments, TemplateVideo, TemplateVideoComments
from django.http import HttpResponse
from django.contrib import messages
import asyncio
# Create your views here.

def long_videozone_view(request):
    if request.method == 'POST':
        long_video = request.FILES.get('long-video')
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        if long_video:
            new_photo = LongVideo(
                long_video=long_video,
                title=title if title else '',
                description=description if description else '',
                size='',
                share_link='',
                share_title=title if title else ''
            )
            new_photo.save()
            messages.success(request, 'Фотографію успішно завантажено!')
            return redirect('videozone_sys:long-video')
        else:
            messages.error(request, 'Будь ласка, виберіть фотографію для завантаження.')
    
    try:
        long_video_list = LongVideo.objects.all()
        content = {"long_video": long_video_list}
    except LongVideo.DoesNotExist:
        long_video_list = []
        content = {"long_video": long_video_list}
    
    return render(request=request, template_name='videozone_sys/long-video.html', context=content)

def short_videozone_view(request):
    if request.method == 'POST':
        short_video = request.FILES.get('short-video')
        title = request.POST.get('title')
        description = request.POST.get('description')

        if short_video:
            new_img = ShortVideo(
                    short_video=short_video,
                    title=title if title else '',
                    description=description if description else '',
                    size='',
                    share_link='',
                    share_title=title if title else ''
                )
            new_img.save()
            messages.success(request=request, message="Ваший фото-дезайн завантажений")
            return redirect('videozone_sys:short_video')
        else:
            messages.error(request, 'Будь ласка, виберіть ваший дизайн для завантаження для завантаження.')

    try:
        short_video_list = ShortVideo.objects.all()
        content = {"short_video": short_video_list}
    except ShortVideo.DoesNotExist:
        short_video_list = []
        content = {"short_video": short_video_list}
    
    return render(request=request, template_name='videozone_sys/short-video.html', context=content)

def add_short_video_comment(request, short_video_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        short_video = ShortVideo.objects.get(id=short_video_id)
        
        if text and author:
            comment = ShortVideoComments.objects.create(text=text, author=author)
            comment.short_video.add(short_video)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('videozone_sys:short_video_detail', short_video_id=short_video_id)

def add_long_video_comment(request, long_video_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        long_video = LongVideo.objects.get(id=long_video_id)
        
        if text and author:
            comment = LongVideoComments.objects.create(text=text, author=author)
            comment.long_video.add(long_video)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('videozone_sys:long_video_detail', long_video_id=long_video_id)

def add_template_video_comment(request, template_video_id):
    if request.method == 'POST':
        text = request.POST.get('text')
        author = request.POST.get('author')
        template_video = TemplateVideo.objects.get(id=template_video_id)
        
        if text and author:
            comment = TemplateVideoComments.objects.create(text=text, author=author)
            comment.template_video.add(template_video)
            messages.success(request, 'Коментар успішно додано!')
        else:
            messages.error(request, 'Будь ласка, заповніть всі поля.')
    
    return redirect('videozone_sys:template_video_detail', template_video_id=template_video_id)