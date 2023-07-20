import email

from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from django.contrib.sites import requests
import requests
from .models import Class
from .models import Tutorme_User
from .forms import CreateUserForm
from .models import CustomUser
import json
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .models import Request

from django.views import generic
from .forms import AddRequestForm

from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth.models import User

@login_required
def my_view(request):
    # Get the user profile of the authenticated user
    user_profile = UserProfile.objects.get(user=request.user)



CLIENT_ID = '853234160427-o777vtaqulfap4blmp1moav55o34acja.apps.googleusercontent.com'
CLIENT_SECRET = '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'
REDIRECT_URI = 'http://localhost:8000/google-auth'





def google_auth(request):
    flow = Flow.from_client_config(
        {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET},
        scopes=['openid', 'https://www.googleapis.com/auth/userinfo.profile', 'https://www.googleapis.com/auth/userinfo.email'],
        redirect_uri=REDIRECT_URI)

    if 'code' not in request.GET:
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)

    else:
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        request.session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }

        # Check if the user already exists in your system
        try:
            user = CustomUser.objects.get(email=email)
            login(request, user)
            if user.user_type:
                if user.user_type == 'tutor':
                    return redirect('tutor_dashboard')
                elif user.user_type == 'tutoree':
                    return redirect('tutoree_dashboard')
            else:
                return redirect('choose_user_type')
        except CustomUser.DoesNotExist:
            # Create a new user in your system
            return redirect('choose_user_type')


def home(request):
    if request.user.is_authenticated:
        tutorme_user = Tutorme_User.objects.filter(username=request.user.username)
        if tutorme_user.exists():
            if tutorme_user.get().is_student:
                tutors = Tutorme_User.objects.filter(is_student=False)
                matched_tutors = []
                for tutor in tutors:
                    if set(tutorme_user.get().enrolled_classes.all()).intersection(tutor.enrolled_classes.all()):
                        matched_tutors.append(tutor)
                return render(request, "tutorme11/studentHomePage.html",{'matched_tutors':matched_tutors})
            else:
                return render(request, "tutorme11/tutorHomePage.html")
        else:
            form = CreateUserForm(initial={'username':request.user.username})
            #https://stackoverflow.com/questions/604266/django-set-default-form-values
            #https://docs.djangoproject.com/en/4.2/ref/forms/fields/#disabled
            form.fields['username'].disabled = True
            return render(request, "tutorme11/loginPage2.html", {
                'form':form,
            })
    else:
        return render(request, "tutorme11/home.html")
    '''return render(request, "tutorme11/loggedInHomePage.html", context)'''

def create_tutorme_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.cleaned_data['username'] = request.user.username
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            is_student = form.cleaned_data['is_student']

            if is_student:
                rate = 0.00
                start_time = timezone.now()
                end_time = timezone.now()
            else:
                rate = form.cleaned_data['rate']
                start_time = form.cleaned_data['start_time']
                end_time = form.cleaned_data['end_time']

            venmo_username = form.cleaned_data['venmo_username'] if not is_student else None
            t = Tutorme_User(username=username, name=name, is_student=is_student, rate=rate, start_time=start_time, end_time=end_time, venmo_username=venmo_username)
            t.save()


        else:
            print("FORM IS NOT VALID")
    print(request.method)
    return HttpResponseRedirect(reverse("home"))


def index(request):
    query = request.GET.get('q', '')

    if Class.objects.all().count() == 0:
        # make all objects and save in database
        PAGES = 89
        url = 'https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&'

        for page in range(1,PAGES+1):
            print("Processing page " + str(page))
            r = requests.get(url + f'page={page}')
            for c in r.json():
                new_class = Class(subject=c['subject'],catalog_nbr=c['catalog_nbr'],descr=c['descr'])
                new_class.save()

    classesList = set()
    for cur_class in Class.objects.all():
        if query in str(cur_class):
            classesList.add(str(cur_class))
    classesList = sorted(list(classesList))

    if request.method == 'POST':
        selected_class_id = request.POST.get('selected_class')
        selected_class_name = request.POST.get('selected_class_name')
        print(selected_class_id)
        print(selected_class_name)

        if request.user.is_authenticated:
            # Save the selected class to the user's Tutorme_User instance
            # TODO: get rid of get_or_create (check if tutor me user exists)
            tutorme_user, created = Tutorme_User.objects.get_or_create(username=request.user.username)

            # Split the selected_class_id to get the catalog_nbr and class_section
            splitted = selected_class_id.split(' ')
            subject = splitted[0]
            catalog_nbr = splitted[1]
            descr = " ".join(splitted[2:])

            # Create or get the Class instance based on the catalog_nbr and class_section
            selected_class, class_created = Class.objects.get_or_create(subject=subject,catalog_nbr=catalog_nbr,descr=descr)

            tutorme_user.enrolled_classes.add(selected_class)
            tutorme_user.save()

            messages.success(request, "Class saved successfully.")
            return redirect('index')
        else:
            messages.error(request, "You need to be logged in to save a class.")
            return redirect('home')

    context = {'classesList': classesList, 'query': query}
    return render(request, "tutorme11/index.html", context)



def choose_user_type(request):
    if request.method == 'POST':
        user_type = request.POST.get('user_type')
        user = request.user
        user.user_type = user_type
        user.save()
        if user_type == 'tutor':
            return redirect('tutor_dashboard')
        elif user_type == 'tutoree':
            return redirect('tutoree_dashboard')
    return render(request, 'choose_user_type.html')

def loggedInHomePage(request):
    return render(request, "tutorme11/loggedInHomePage.html")

def loggedOut(request):
    return render(request, "tutorme11/loggedOut.html")

def tutor_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    tutorme_user = Tutorme_User.objects.filter(username=request.user.username)
    if tutorme_user.exists() and not tutorme_user.get().is_student:
        tutorees = Tutorme_User.objects.filter(is_student=True)
        matched_tutorees = []
        for tutoree in tutorees:
            if set(request.user.enrolled_classes.all()).intersection(tutoree.enrolled_classes.all()):
                matched_tutorees.append(tutoree)
        return render(request, 'tutorme11/tutor_dashboard.html', {'tutorees': matched_tutorees})
    else:
        return redirect('home')

def tutoree_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('home')
    tutorme_user = Tutorme_User.objects.filter(username=request.user.username)
    if tutorme_user.exists() and tutorme_user.get().is_student:
        tutors = Tutorme_User.objects.filter(is_student=False)
        matched_tutors = []
        for tutor in tutors:
            if set(tutorme_user.get().enrolled_classes.all()).intersection(tutor.enrolled_classes.all()):
                matched_tutors.append(tutor)
        return render(request, 'tutorme11/tutoree_dashboard.html', {'matched_tutors': matched_tutors})
    else:
        return redirect('home')

def save_class(request):
    if request.method == 'POST':
        class_id = request.POST['selected_class']
        class_to_save = Class.objects.get(id=class_id)
        request.user.enrolled_classes.add(class_to_save)
        return redirect('loggedInHomePage')

def view_requests(request):

    if request.user.is_authenticated:
        tutorme_user = Tutorme_User.objects.filter(username=request.user.username)
        if tutorme_user.exists():
            if tutorme_user.get().is_student:
                cur_requests = Request.objects.filter(student_username=request.user.username)
                return render(request, "tutorme11/tutoree_requests.html", {'requests': cur_requests})
            else:
                cur_requests = Request.objects.filter(tutor_username=request.user.username)
                return render(request, "tutorme11/tutor_requests.html", {'requests': cur_requests})

    return redirect('home')

def accept_request(request, request_id):
    cur_request = get_object_or_404(Request, pk=request_id)
    cur_request.status = Request.ACCEPTED
    cur_request.save()
    return redirect('view_requests')

def reject_request(request, request_id):
    cur_request = get_object_or_404(Request, pk=request_id)
    cur_request.status = Request.REJECTED
    cur_request.save()
    return redirect('view_requests')

def user_profile(request,username):
    if request.user.is_authenticated:
        tutorme_user = Tutorme_User.objects.filter(username=request.user.username)
        if tutorme_user.exists():
            user = get_object_or_404(Tutorme_User,username=username)
            auth_user = get_object_or_404(User,username=username)
            form = AddRequestForm()
            context = {
                'user':user,
                'is_student':tutorme_user.get().is_student,
                'email':auth_user.email,
                'form':form,
            }

            return render(request,'tutorme11/user_profile.html',context)
    

    return redirect('home')

def add_request(request,student_username,tutor_username):
    if request.method == 'POST':
        form = AddRequestForm(request.POST)
        if form.is_valid():
            tutor = Tutorme_User.objects.filter(username=tutor_username)
            if tutor.get().start_time < form.cleaned_data['time'] < tutor.get().end_time:
                req = Request(student_username=student_username,tutor_username=tutor_username,time=form.cleaned_data['time'])
                req.save()
            else:
                print("time out of available range")
            
    return redirect(f'/user/{tutor_username}')


def pay_now(request, tutor_username):
    tutor = get_object_or_404(Tutorme_User, username=tutor_username)
    venmo_url = f'https://venmo.com/{tutor.venmo_username}'
    return redirect(venmo_url)
