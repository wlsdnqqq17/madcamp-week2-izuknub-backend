import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import User

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
                nickname=nickname
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
