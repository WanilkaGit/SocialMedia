from django.shortcuts import render, redirect
from .models import Audio, Music
from django.http import HttpResponse
from django.contrib import messages
import asyncio
# Create your views here.
def audio_view(request):
    if request.method == 'POST':
        audio = request.FILES.get('audio')
        title = request.POST.get('title')
        description = request.POST.get('description')

        if audio:
            new_audio = Audio(
                    audio=audio,
                    title=title if title else '',
                    description=description if description else '',
                    size=audio.size,
                    share_link='',
                    share_title=title if title else ''
                )
            new_audio.save()
            messages.success(request=request, message="Ваш аудіо файл успішно завантажено")
            return redirect('audiozone_sys:audio')
        else:
            messages.error(request, 'Будь ласка, виберіть ваш аудіо файл для завантаження.')

    try:
        audios_list = Audio.objects.all()
        content = {"audios": audios_list}
    except Audio.DoesNotExist:
        audios_list = []
        content = {"audios": audios_list}
    
    return render(request=request, template_name='audiozone_sys/audio.html', context=content)


def music_view(request):
    if request.method == 'POST':
        music = request.FILES.get('music')
        title = request.POST.get('title')
        description = request.POST.get('description')

        if music:
            new_music = Music(
                    music=music,
                    title=title if title else '',
                    description=description if description else '',
                    size=music.size,
                    share_link='',
                    share_title=title if title else ''
                )
            new_music.save()
            messages.success(request=request, message="Ваш музичний файл успішно завантажено")
            return redirect('audiozone_sys:music')
        else:
            messages.error(request, 'Будь ласка, виберіть ваш музичний файл для завантаження.')

    try:
        musics_list = Music.objects.all()
        content = {"musics": musics_list}
    except Music.DoesNotExist:
        musics_list = []
        content = {"musics": musics_list}
    
    return render(request=request, template_name='audiozone_sys/music.html', context=content)