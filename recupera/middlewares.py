from django.conf import settings
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib import messages


class SessionTimeOutMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            if last_activity:
                last_activity = timezone.datetime.fromisoformat(last_activity)
                if (timezone.now() - last_activity).total_seconds() > settings.SESSION_TIMEOUT:
                    logout(request)
                elif (timezone.now() - last_activity).total_seconds() < 300:
                    messages.warning(request, 'Su sesion expirará pronto')

            request.session['last_activity'] = timezone.now().isoformat()

        response = self.get_response(request)
        return response
