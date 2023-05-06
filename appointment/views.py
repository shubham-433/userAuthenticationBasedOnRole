from django.shortcuts import redirect,HttpResponse,render,HttpResponseRedirect
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from django.conf import settings
from django.http  import JsonResponse
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta





def google_calendar_permission(request):
    # set up the Google API credentials and flow
    flow = Flow.from_client_secrets_file(
        'clientSecret.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=request.build_absolute_uri('/appointment/google_calendar_callback/')
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    # save the state to the session so we can use it later
    request.session['google_calendar_state'] = state
    print(request.session['google_calendar_state'])

    return redirect(authorization_url)



def google_calendar_callback(request):
    print("hi")
    # retrieve the state from the session
    state = request.session.pop('google_calendar_state', None)

    # set up the Google API credentials and flow
    flow = Flow.from_client_secrets_file(
        'clientSecret.json',
        scopes=['https://www.googleapis.com/auth/calendar'],
        redirect_uri=request.build_absolute_uri('/appointment/google_calendar_callback/')
    )
    flow.fetch_token(authorization_response=request.build_absolute_uri(),
                     state=state)

    # save the credentials to the database or a JSON file
    credentials = Credentials.to_json(flow.credentials)
    # save to database
    user = request.user
    user.google_credentials = credentials
    print(user.google_credentials)
    user.save()
    print(user.google_credentials)
    # or save to a JSON file
    with open('clientSecret', 'w') as f:
        f.write(credentials)
    print("hi")
    return redirect('success_page')

def success(request):
    return  HttpResponse("success")
def home(request):
   return  HttpResponse("hi")



# for appointment list 

def appointment_list(request):
    # doctors = settings.AUTH_USER_MODEL.objects.all(is_doctor=True)
    # print(doctors)
    User = get_user_model()
    doctors = User.objects.filter(is_doctor=True)
    print(doctors)
    for doctor in doctors:
        print(doctor.username)  # assuming 'name' is a field on your custom User model
        print(doctor.email)  # assuming 'email' is a field on your custom User model
        
    # add more fields as needed
    return render(request, 'appointmentList.html', {'doctors':doctors})


SCOPES=['https://www.googleapis.com/auth/calendar'] 
def get_calender_event(request):
    doctor = get_user_model()
    doctor = get_object_or_404(doctor, id=3)
    print(doctor.google_credentials)
    tokenDic=json.loads(doctor.google_credentials)
    print(tokenDic['token'])

    cre = json.loads(doctor.google_credentials)
    creds = Credentials.from_authorized_user_info(  cre ,SCOPES)
    service = build('calendar', 'v3', credentials=creds)
    event = {
    'summary': 'Google I/O 2023',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
        'dateTime': '2023-05-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'end': {
        'dateTime': '2023-05-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
    },
    'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
    ],
    'attendees': [
        {'email': 'lpage@example.com'},
        {'email': 'sbrin@example.com'},
    ],
    'reminders': {
        'useDefault': False,
        'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
        ],
    },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    # now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                         maxResults=10, singleEvents=True,
    #                                         orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    #     return HttpResponse("ok")

    # # Prints the start and name of the next 10 events
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])
    return redirect("home")
    # return render(request, 'doctor_list.html', {'doctors': doctors})

# book appointment 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from django.utils import timezone
from datetime import datetime
from .forms import *
# from .models import Doctor, Patient

import json 
from django.utils import timezone
def book_appointment(request, doctor_id):
    doctor = get_user_model()
    doctor = get_object_or_404(doctor, id=doctor_id)
    print(doctor.google_credentials)
    tokenDic=json.loads(doctor.google_credentials)
    # print(tokenDic['token'])
    
    if request.method == 'POST':
        print("hi")
        speciality=request.POST["speciality"]
        appointment_start_time=request.POST["appointment_start_time"]
        start_time = datetime.fromisoformat(appointment_start_time)
        print("type of start time " ,type(start_time))
        # Add 45 minutes to the datetime object
        end_time = start_time + timedelta(minutes=45)
        print("type of end time ", type(end_time))
        # Convert the end time back to an ISO-formatted string
        # end_time_str = end_time.isoformat()

        appointment_start_time = datetime.strptime(appointment_start_time, '%Y-%m-%dT%H:%M')
        # appointment_end_time = datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M')
        # request.POST["appointment_start_time"]
        print(type(appointment_start_time))
        print('Start time:', appointment_start_time.isoformat())
        print('End time:', end_time.isoformat())
        doctor = get_user_model()
        doctor = get_object_or_404(doctor, id=doctor_id)
        # print(doctor.google_credentials)
        tokenDic=json.loads(doctor.google_credentials)
        # print(tokenDic['token'])

        cre = json.loads(doctor.google_credentials)
        creds = Credentials.from_authorized_user_info(  cre ,SCOPES)
        service = build('calendar', 'v3', credentials=creds)
        event = {
        'summary': "Book Appoinment" ,
        'location': 'Mumbai',
        'description': 'Book a Appointment for a patient',
        'start': {
            'dateTime':  str(start_time.isoformat()),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'recurrence': [
            'RRULE:FREQ=DAILY;COUNT=2'
        ],
        'attendees': [
            {'email': 'lpage@example.com'},
            {'email': 'sbrin@example.com'},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
            {'method': 'email', 'minutes': 24 * 60},
            {'method': 'popup', 'minutes': 10},
            ],
        },
        }
        print("hello")
        event = service.events().insert(calendarId='primary', body=event).execute()
        appointment=Appointment(
            doctor=doctor,
            patient=request.user,
            speciality=speciality,
            appointment_start_time=timezone.make_aware(start_time),
            appointment_end_time=timezone.make_aware(end_time),
            appointment_date=timezone.make_aware(end_time),
            
        )
        appointment.save()
        
        messages.success(request, 'Appointment booked successfully!')
        return redirect("home")
        # return redirect('appointment_details', doctor_id=doctor.id, appointment_id=event['id'])

       
    
        # return  HttpResponseRedirect('/appointment/list')
    return render(request, 'bookAppointment.html', {'doctor': doctor})
    


def appointment_details(request, doctor_id, appointment_id):
    doctor=settings.AUTH_USER_MODEL.objects.filter(is_doctor=True)
    print(doctor)
    doctor = get_object_or_404(doctor, id=doctor_id)
    appointment = None
    try:
        credentials = Credentials.from_authorized_user_info(request.session['google_auth_credentials'])
        service = build('calendar', 'v3', credentials=credentials)
        appointment = service.events().get(calendarId='primary', eventId=appointment_id).execute()
    except HttpError as error:
        messages.error(request, f'Error fetching appointment details: {error}')

    return render(request, 'appointmentDetails.html', {'doctor': doctor, 'appointment': appointment})