from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from nio import AsyncClient
from auth_sys.models import SMUser

async def get_rooms(matrix_user_id, password):
    client = AsyncClient("https://matrix.org", matrix_user_id)
    
    try:
        await client.login(password)  # Логін за допомогою пароля

        sync_response = await client.sync(30000)  # Отримання оновлень
        rooms = getattr(sync_response.rooms, 'join', {})  # Безпечне отримання кімнат

        room_list = []
        for room_id, room_info in rooms.items():
            room_name = getattr(room_info, "name", "Unnamed Room")  # Запобігаємо помилці
            room_list.append({
                "room_id": room_id,
                "room_name": room_name
            })
        
        return room_list

    except Exception as e:
        print(f"Помилка отримання кімнат: {e}")  # Логування помилок
        return []

    finally:
        await client.close()  # Закриваємо клієнт після використання

@login_required
def rooms_view(request):
    sm_user = request.user
    current_user = sm_user.current_user

    print(f"Matrix User ID: {current_user.matrix_user_id}")
    print(f"Password: {current_user.password}")  # ⚠️ ВАЖЛИВО: У реальному додатку не виводь паролі в консоль!

    # Викликаємо асинхронну функцію у синхронному контексті
    room_list = async_to_sync(get_rooms)(current_user.matrix_user_id, current_user.password)

    context = {'rooms': room_list}
    return render(request, 'messenger_sys/rooms.html', context)