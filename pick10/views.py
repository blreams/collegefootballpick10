from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from pick10.models import Team
from pick10.forms import UserForm

def register(request):
    # A boolean value for telling the template whether the registration was
    # successful. Set to False initially. Code changes value to True when 
    # registration succeeds.
    registered = False

    # If it is HTTP POST, we are interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form.
        user_form = UserForm(data=request.POST)

        # If the form is valid...
        if user_form.is_valid():
            # Save the user form data to the db.
            user = user_form.save()

            # Hash password using set_password method, then update user object
            user.set_password(user.password)
            user.save()

            # Update our variable to tell the template registration success.
            registered = True

        # Invalid form, mistakes or something else?
        # Print problems to the terminal, show to user.
        else:
            print user_form.errors

    # Not a HTTP POST, so we render our form using ModelForm instance.
    # This form will be blank, ready for user input.
    else:
        user_form = UserForm()

    # Render the template depending on the context.
    return render(
            request, 
            'pick10/register.html',
            {'user_form': user_form, 'registered': registered}
            )

def user_login(request):
    # If the request is HTTP POST, try to pull out the information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use django's machinery to see if username/password is valid.
        # A user object is returned.
        user = authenticate(username=username, password=password)

        if user:
            # Active? could have been disabled.
            if user.is_active:
                # We can login the user
                login(request, user)
                return HttpResponseRedirect('/pick10/')
            else:
                # Inactive account
                return HttpResponse('Your account is diabled.')
        else:
            # Bad login
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not HTTP POST, so display login form.
    else:
        # No context variable to pass.
        return render(request, 'pick10/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can just log them out.
    logout(request)
    return HttpResponseRedirect('/pick10/')

def home(request):
    return render(request, 'pick10/home.html')

@login_required
def index(request):
    return render(request, 'pick10/index.html')

