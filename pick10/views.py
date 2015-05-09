from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

from pick10.models import Team
from pick10.forms import UserForm

def register(request):
    registered = False

    if request.method == 'POST':
        # HTTP POST
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            # Save to db, hash password, save again
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True

        else:
            # Invalid form, mistakes, print to term, show to user
            print user_form.errors

    else:
        # not HTTP POST (GET)
        user_form = UserForm()

    # Render the template depending on the context.
    return render(request, 'pick10/register.html', {'user_form': user_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # HTTP POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # authenticate, user object or None is returned.
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/pick10/')
            else:
                # Inactive account
                return HttpResponse('Your account is diabled.')
        else:
            # Bad login
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        # not HTTP POST (GET), empty context
        return render(request, 'pick10/login.html', {})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can just log them out.
    logout(request)
    return HttpResponseRedirect('/pick10/')

@login_required
def home(request):
    return render(request, 'pick10/home.html')

def index(request):
    return render(request, 'pick10/index.html')

