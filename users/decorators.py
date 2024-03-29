from collections import defaultdict
from csgame.views import over
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.sessions.models import Session
from django.shortcuts import redirect
from functools import wraps
from .models import HIT


NUMROUNDS = settings.NUMROUNDS


def player_required(func):
    '''
    Decorator for views that checks that the logged in user is a mturk worker, or staff
    redirects to the log-in page if necessary.
    '''
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        assignmentId = request.GET.get('assignmentId')
        is_mturker = assignmentId not in (None, 'ASSIGNMENT_ID_NOT_AVAILABLE')

        if is_mturker:
            request.session['assignmentId'] = assignmentId

        if (request.user.is_staff or request.user.is_superuser) and "assignmentId" not in request.session:
            request.session['assignmentId'] = request.user.username

        if "assignmentId" in request.session:
            hitObj = HIT.objects.only('data').get_or_create(session=request.session.session_key, defaults={'data': {}})[0]
            hit = hitObj.data

            roundnums = hit.setdefault('roundnums', {})

            numInPhase = roundnums.get(func.__name__, 0) # this line is pretty unsafe, but it will do

            if request.method == 'POST':
                output = func(request, *args, **kwargs)
                roundnums[func.__name__] = numInPhase + 1
                hitObj.data = hit
                hitObj.save()
                return output
            else:
                return over(request) if numInPhase >= NUMROUNDS else func(request, *args, **kwargs)
        else:
            return func(request, *args, **{'previewMode': True, **kwargs})
    return wrapper


# decorator that will not be used now
def requester_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    Decorator for views that checks that the logged in user is a player,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_staff or (u.is_active and u.is_requester),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
