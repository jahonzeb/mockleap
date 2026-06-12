from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()

@login_required
def leaderboard(request):
    tab = request.GET.get('tab', 'global')
    users = User.objects.filter(is_active=True).order_by('-xp')[:100]
    user_rank = None
    for i, u in enumerate(users, 1):
        if u == request.user:
            user_rank = i
            break
    return render(request, 'rankings/leaderboard.html', {
        'users': users,
        'tab': tab,
        'user_rank': user_rank,
    })
