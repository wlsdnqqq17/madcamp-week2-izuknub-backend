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

