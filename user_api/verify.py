import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
verify = client.verify.services(settings.TWILIO_VERIFY_SERVICE_SID)


def send(phone):
    print('-----')
    verify.verifications.create(to=str('+91')+phone, channel='sms')
    


def check(phone, code):
    try:
        result = verify.verification_checks.create(to=str('+91')+phone, code=code)
    except TwilioRestException:
        print('no  ckeck failed')
        return False
    return result.status == 'approved'