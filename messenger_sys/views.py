from django.shortcuts import render
import requests
import asyncio
from nio import AsyncClient, SyncResponse
from django.http import JsonResponse
from auth_sys.models import SMUser
from django.contrib.auth.decorators import login_required
from asgiref.sync import async_to_sync
import asyncio

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
        sm_user = request.user
        display_name = sm_user.display_name
        current_user= sm_user.current_user
        print(current_user.matrix_user_id, current_user.password)
        print(display_name, current_user)

        room_list = async_to_sync(get_rooms)(matrix_user_id=current_user.matrix_user_id, password=current_user.password)

        # Pass data to template

        print(room_list)
        context = {'rooms': room_list}
        return render(request, 'messenger_sys/rooms.html', context)