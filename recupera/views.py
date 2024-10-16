from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from reportes.models import Usuario


@login_required
def home(request):
    return render(
        request,
        'home.html'
    )


@login_required
def profile(request, username):
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
        if user.rank == 'senior':
            pass
        elif user.rank == 'semisenior':
            pass
        else:
            pass

        messages.success(request, 'Informacion Actualizada con exito')
        return redirect('profile', username=request.user.username)

    return render(
        request,
        'profile.html',
        context={
            'user': request.user,
        }
    )


def custom_403_handler(request, exception):
    return render(
        request,
        '403.html',
        status=403
    )
