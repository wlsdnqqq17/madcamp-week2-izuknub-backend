import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *

@csrf_exempt
def save_kakao_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        login_id = data.get('login_id')
        nickname = data.get('nickname')

        try:
            user = User.objects.get(login_id=login_id)
            user.nickname = nickname
            user.save()
            return JsonResponse({'status': 'updated'}, status=200)
        except User.DoesNotExist:
            User.objects.create(
                login_id=login_id,
                nickname=nickname,
            )
            return JsonResponse({'status': 'created'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def search_user(request):
    if request.method == 'GET':
        login_id = request.GET.get('loginId')
        try:
            user = User.objects.get(login_id=login_id)
            return JsonResponse({
                'success': True,
                'message': 'User found',
                'data': {
                    'login_id': user.login_id,
                    'nickname': user.nickname
                }
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(['GET'])
def get_items(request):
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_friend(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')

    try:
        from_user = User.objects.get(login_id=from_user_id)
        to_user = User.objects.get(login_id=to_user_id)

        friend_request, created = Friend.objects.get_or_create(
            from_user=from_user,
            to_user=to_user,
            defaults={'are_we_friend': False}
        )

        if created:
            return Response({'status': 'request_sent'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'request_already_exists'}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_friends(request, user_id):
    try:
        user = User.objects.get(login_id=user_id)
        friends = Friend.objects.filter(from_user=user, are_we_friend=True).select_related('to_user')
        friend_list = [friend.to_user for friend in friends]
        serializer = UserSerializer(friend_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_friend_requests(request, user_id):
    try:
        user = User.objects.get(login_id=user_id)
        friend_requests = Friend.objects.filter(to_user=user, are_we_friend=False).select_related('from_user')
        request_list = [friend.from_user for friend in friend_requests]
        serializer = UserSerializer(request_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def accept_friend_request(request):
    from_user_id = request.data.get('from_user_id')
    to_user_id = request.data.get('to_user_id')

    try:
        from_user = User.objects.get(login_id=from_user_id)
        to_user = User.objects.get(login_id=to_user_id)
        friend_request = Friend.objects.get(from_user=from_user, to_user=to_user, are_we_friend=False)
        friend_request.are_we_friend = True
        friend_request.save()
        return Response({'status': 'friend request accepted'}, status=status.HTTP_200_OK)
    except (User.DoesNotExist, Friend.DoesNotExist):
        return Response({'error': 'Friend request not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
def purchase_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        item_id = data.get('item_id')

        try:
            user = User.objects.get(login_id=user_id)
            item = Item.objects.get(id=item_id)
            user_item, created = UserItem.objects.get_or_create(user_id=user, item_id=item)
            if created:
                return JsonResponse({'status': 'Item purchased successfully'}, status=201)
            else:
                return JsonResponse({'status': 'Item already purchased'}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        except Item.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def get_user_items(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        try:
            user = User.objects.get(login_id=user_id)
            user_items = UserItem.objects.filter(user_id=user)
            items = [ui.item_id for ui in user_items]
            items_data = [{'id': item.id, 'name': item.name, 'category': item.category,
                           'item_image_url': item.item_image_url, 'price': item.price,
                           'is_purchased': True} for item in items]
            return JsonResponse(items_data, safe=False, status=200)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@csrf_exempt
def update_avatar_state(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_id = data.get('user_id')
        item_id = data.get('item_id')

        try:
            user = User.objects.get(login_id=user_id)
            item = Item.objects.get(id=item_id)

            avatar_state, created = UserAvatarState.objects.get_or_create(user=user)

            if item.category == 'hat':
                avatar_state.hat_item = item
            elif item.category == 'clothes':
                avatar_state.clothes_item = item
            elif item.category == 'accessory':
                avatar_state.accessory_item = item
            elif item.category == 'background':
                avatar_state.background_item = item
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid category.'}, status=400)

            avatar_state.save()

            return JsonResponse({'status': 'success', 'message': 'Avatar state updated successfully.'}, status=200)

        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found.'}, status=404)
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)

@csrf_exempt
def get_avatar_state(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')

        try:
            user = User.objects.get(login_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

        try:
            avatar_state = UserAvatarState.objects.get(user=user)
        except UserAvatarState.DoesNotExist:
            avatar_state = UserAvatarState.objects.create(
                user=user,
                hat_item=None,
                clothes_item=None,
                accessory_item=None,
                background_item=None,
            )

        data = {
            'user_id': user.login_id,
            'hat_item_id': avatar_state.hat_item.id if avatar_state.hat_item else None,
            'clothes_item_id': avatar_state.clothes_item.id if avatar_state.clothes_item else None,
            'accessory_item_id': avatar_state.accessory_item.id if avatar_state.accessory_item else None,
            'background_item_id': avatar_state.background_item.id if avatar_state.background_item else None,
        }

        return JsonResponse({'status': 'success', 'avatar_state': data}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


@csrf_exempt
def get_item_image_url(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')

        try:
            item = Item.objects.get(id=item_id)
            data = {
                'item_id': item.id,
                'item_image_url': item.item_image_url
            }
            return JsonResponse({'status': 'success', 'data': data}, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
