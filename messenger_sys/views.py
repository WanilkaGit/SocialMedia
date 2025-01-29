from django.shortcuts import render
import requests
import asyncio
from nio import AsyncClient, SyncResponse
from django.http import JsonResponse
from auth_sys.models import SMUser
from django.contrib.auth.decorators import login_required

# Create your views here.
async def get_rooms(matrix_user_id, password):
    client = AsyncClient("https://matrix.org", matrix_user_id)
    await client.login(password)

    sync_response = await client.sync(30000)  # Отримуємо оновлення з сервера
    rooms = sync_response.rooms.join  # Отримуємо список кімнат, до яких належить користувач

    room_list = []
    for room_id, room_info in rooms.items():
        room_list.append({
            "room_id": room_id,
            "room_name": room_info.name
        })

    return room_list

@login_required
def rooms_view(request):
    try:
        # Отримуємо SMUser для поточного користувача
        sm_user = SMUser.objects.get(display_name=request.user.username)
        
        # Отримуємо current_user
        current_user = sm_user.current_user

        # Використовуємо current_user для отримання кімнат
        room_list = asyncio.run(get_rooms(current_user.matrix_user_id, current_user.password))
        return JsonResponse(room_list, safe=False)
    except SMUser.DoesNotExist:
        return JsonResponse({'error': 'SMUser not found'}, status=404)
