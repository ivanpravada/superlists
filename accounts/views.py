from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib import messages, auth
from accounts.models import Token
from django.urls import reverse

def send_login_email(request):
    '''отправить сообщение для входа в систему'''

    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in: \n\n{url} '
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    '''логин пользователя'''
    
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')

def logout_view(request):
    '''выход из системы'''

    auth.logout(request)
    return redirect('/')