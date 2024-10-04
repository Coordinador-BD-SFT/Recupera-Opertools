from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages


@login_required
def home(request):
    return render(
        request,
        'home.html'
    )


@login_required
def profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user = request.user
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        if not user.is_staff:
            campaign = request.POST.get('campaign')
            rank = request.POST.get('rank')
            user.campaign = campaign
            user.rank = rank
        user.save()
        messages.success(request, 'Informacion Actualizada con exito')
        return redirect('profile')

    return render(
        request,
        'profile.html',
        context={
            'user': request.user,
        }
    )
