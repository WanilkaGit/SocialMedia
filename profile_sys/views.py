from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from auth_sys.models import SMUser

@login_required
def user_profile_view(request):
    # Отримуємо поточного користувача
    user = request.user

    # Отримуємо дані, пов'язані з користувачем
    photos = user.photos.all()
    videos_long = user.videos_long.all()
    videos_short = user.videos_short.all()
    audio = user.audio.all()
    music = user.music.all()
    projects = user.project.all()

    # Створюємо контекст для передачі в шаблон
    context = {
        'user': user,
        'photos': photos,
        'videos_long': videos_long,
        'videos_short': videos_short,
        'audio': audio,
        'music': music,
        'projects': projects,
    }

    # Відображаємо шаблон з даними
    return render(request, 'profilezone_sys/profile.html', context)    