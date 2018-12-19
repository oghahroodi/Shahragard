from django.conf import settings
settings.configure(EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend',
                   EMAIL_HOST='smtp.gmail.com',
                   EMAIL_USE_TLS=True,
                   EMAIL_PORT=587,
                   EMAIL_HOST_USER='shahragard@gmail.com',
                   EMAIL_HOST_PASSWORD='memtas-saqmU4-defryp')

subject = 'Thank you for registering to our app'
message = 'برای فعال سازی اکانت بر روی لینک زیر کلیک کنید \n' + \
    '127.0.0.1:8000/apiv1/verification/'
email_from = settings.EMAIL_HOST_USER
