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
async def get_rooms(matrix_user_id, access_token):
    client = AsyncClient("https://matrix.org", matrix_user_id)
    client.access_token = access_token  # Використовуємо токен доступу

    sync_response = await client.sync(30000)  # Отримуємо оновлення про кімнати
    rooms = sync_response.rooms.join  # Отримуємо приєднані кімнати

    room_list = []
    for room_id, room_info in rooms.items():
        room_list.append({
            "room_id": room_id,
            "room_name": getattr(room_info, "name", "Unnamed Room")
        })

    await client.close()
    return room_list

async def send_message(matrix_user_id, access_token, room_id, message):
    client = AsyncClient("https://matrix.org", matrix_user_id)
    client.access_token = access_token

    try:
        response = await client.room_send(
            room_id=room_id,
            message_type="m.room.message",
            content={
                "msgtype": "m.text",
                "body": message
            }
        )
        return response
    finally:
        await client.close()

@login_required
def rooms_view(request):
    sm_user = request.user
    current_user = sm_user.current_user
    print(current_user.access_token)

    # Check if the user has a stored access token
    if not current_user.access_token:
        return JsonResponse({"error": "No access token available"}, status=403)

    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        message_body = request.POST.get('message_body')
        
        if room_id and message_body:
            response = async_to_sync(send_message)(
                current_user.matrix_user_id,
                current_user.access_token,
                room_id,
                message_body
            )
            if response and hasattr(response, 'event_id'):
                return JsonResponse({"success": True, "event_id": response.event_id})
            else:
                return JsonResponse({"error": "Failed to send message"}, status=500)
        else:
            return JsonResponse({"error": "Missing room_id or message_body"}, status=400)

    # Run async function safely in sync Django view
    room_list = async_to_sync(get_rooms)(current_user.matrix_user_id, current_user.access_token)
    print(room_list)
    if room_list != None:
        # Pass data to template
        content = {'rooms': room_list}
        return render(request, 'messenger_sys/rooms.html', content)
    else:
        print("Error fetching rooms")
        return JsonResponse({"error": "Failed to fetch rooms"}, status=500)