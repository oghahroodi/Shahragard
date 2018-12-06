import redis
import json
from django.core.mail import send_mail
from django.conf import settings
settings.configure(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                   EMAIL_HOST='smtp.gmail.com',
                   EMAIL_USE_TLS=True,
                   EMAIL_PORT=587,
                   EMAIL_HOST_USER='shahragard@gmail.com',
                   EMAIL_HOST_PASSWORD='memtas-saqmU4-defryp')


def email(receiver, random_token):
    subject = 'Thank you for registering to our app'
    message = 'برای فعال سازی اکانت بر روی لینک زیر کلیک کنید \n' + \
        '127.0.0.1:8000/apiv1/verification/' + random_token + '/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [receiver, ]
    send_mail(subject, message, email_from, recipient_list)


while(True):
    connRedis = redis.StrictRedis(
        host='localhost', port=6379, password='', charset="utf-8",
        decode_responses=True)
    mail = connRedis.blpop('email')
    mail = json.loads(mail[1])
    email(mail['receiver'], mail['token'])
