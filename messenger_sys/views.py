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
    client.access_token = access_token  # Use access token instead of password

    sync_response = await client.sync(30000)  # Fetch room updates
    rooms = sync_response.rooms.join  # Get joined rooms
    print(client.access_token)

    room_list = []
    for room_id, room_info in rooms.items():
        room_list.append({
            "room_id": room_id,
            "room_name": getattr(room_info, "name", "Unnamed Room")
        })

    await client.close()
    return room_list

@login_required
def rooms_view(request):
    sm_user = request.user
    current_user = sm_user.current_user

    # Check if the user has a stored access token
    if not current_user.access_token:
        return JsonResponse({"error": "No access token available"}, status=403)

    # Run async function safely in sync Django view
    room_list = async_to_sync(get_rooms)(current_user.matrix_user_id, current_user.matrix_access_token)

    # Pass data to template
    context = {'rooms': room_list}
    return render(request, 'messenger_sys/rooms.html', context)