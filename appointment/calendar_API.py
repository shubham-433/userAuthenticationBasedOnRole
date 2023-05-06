from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

from django.conf import settings
from django.shortcuts import redirect

from main.settings import GOOGLE_REDIRECT_URI

def oauth2callback(request):
    flow = Flow.from_client_secrets_file(
        'client_secret.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=GOOGLE_REDIRECT_URI
    )
    flow.redirect_uri = GOOGLE_REDIRECT_URI
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    request.session['credentials'] = credentials.to_json()
    
    # Save the credentials to the doctor's model
    doctor = request.user.doctor
    doctor.google_credentials = credentials.to_json()
    doctor.save()

    return redirect('appointment_book')