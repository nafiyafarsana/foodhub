from django.contrib.auth import get_user_model
from celery import shared_task 
from django.core.mail import send_mail
from Foodhub import settings
from vendor_api.models import Vendor

@shared_task(bind=True)
def send_menumail_func(self):
    vendors = Vendor.objects.all()
    for vendor in vendors:
        print(vendor)
        print('----------')
        mail_subject = "Hi! New food added"
        message = "new food has been added to our app"
        to_email = vendor.email
        send_mail(
            subject = mail_subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[to_email],
            fail_silently=True,
        )


    return "Done"