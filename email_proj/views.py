from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import messages
from django.core.mail import send_mail, send_mass_mail
from email_proj.models import E_mail
from django.shortcuts import render


import datetime
import threading
import time
import os
# Create your views here.


def index(request):
    return HttpResponse("Hello, world.")

def e_list(request):
    e_mails = E_mail.objects.all().order_by('-id')[:10]


    return render(
        request,
        "main.html",
        {"e_mails": e_mails},
    )

class SendFormEmail(View):

    def  get(self, request):

        delay = request.GET.get('delay', None)
        message = request.GET.get('message', None)
        #print("Delay: ", str(delay),', message:',message)
        e = E_mail(text=message, time_to_send = delay)
        e.save()
        #print(e.pk)
        init_send()
        messages.success(request, ('Сообщение поставлено в очередь.'))
        return redirect('home1')

def init_send():

    e_mails = E_mail.objects.all().filter(sent = False)
    for e_mail in e_mails:
        if check_time_stamp(e_mail):
            print (e_mail.text)
            t = threading.Thread(target=e_mail_mail, args=(e_mail, 0))
            t.start()

        else:
            t_delta = e_mail.time_to_send*60 - int((datetime.datetime.now(datetime.timezone.utc) - e_mail.time_stamp).seconds)
            t = threading.Thread(target=e_mail_mail, args=(e_mail, t_delta))
            t.start()

def check_time_stamp(e_mail):
    b = datetime.datetime.now(datetime.timezone.utc) - e_mail.time_stamp
    if ((b.seconds)/60) > e_mail.time_to_send:
        print((b.seconds)/60, 'True')
        return True
    else:
        print((b.seconds)/60, 'False')
        return False #возвращает True если письмо должно быть отправленно немедленно (сроки прошли)

def e_mail_mail(e_mail, delay):
    time.sleep(delay)
    send_mail(
        'Test e-mail',
        e_mail.text,
        os.environ.get('DJANGO_HOST_USER'), # Admin
        [
            os.environ.get('DJANGO_HOST_USER'),
        ]
    )
    e_mail.sent = True
    e_mail.save()
