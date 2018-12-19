import redis
import json
import mailsetting
from django.core.mail import send_mail


def email(receiver, random_token):
    message = mailsetting.message+random_token
    recipient_list = [receiver, ]
    send_mail(mailsetting.subject, message,
              mailsetting.email_from, recipient_list)


while(True):
    connRedis = redis.StrictRedis(
        host='localhost', port=6379, password='', charset="utf-8",
        decode_responses=True)
    mail = connRedis.blpop('email')
    mail = json.loads(mail[1])
    email(mail['receiver'], mail['token'])
