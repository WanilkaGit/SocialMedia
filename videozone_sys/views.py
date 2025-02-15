from django.shortcuts import render, redirect
from .models import LongVideo, ShortVideo
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
            return redirect('videozone_sys:long_video')
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