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
        daily_goal = data.get('daily_goal', 0)

        try:
            user = User.objects.get(login_id=login_id)
            user.nickname = nickname
            user.save()
            return JsonResponse({'status': 'updated'}, status=200)
        except User.DoesNotExist:
            User.objects.create(
                login_id=login_id,
                nickname=nickname,
                daily_goal=daily_goal
            )
            return JsonResponse({'status': 'created'}, status=201)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def search_user(request):
    print("search_user view called")  # 디버깅 로그 추가
    if request.method == 'GET':
        login_id = request.GET.get('loginId')
        print(f"Received loginId: {login_id}")  # 디버깅 로그 추가
        try:
            user = User.objects.get(login_id=login_id)
            return JsonResponse({
                'success': True,
                'message': 'User found',
                'data': {
                    'login_id': user.login_id,
                    'nickname': user.nickname,
                    'daily_goal': user.daily_goal,
                    'current_potato': user.current_potato,
                }
            }, status=200)
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request'}, status=400)
