from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from models import UserProfile
from forms import UserProfileForm

class ProfileView:

    def get(self,request):
        user = request.user
        if not user.is_active:
            return HttpResponseNotFound('<h1>You are not logged in </h1>')

        userprofile, created = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(instance=userprofile)
        context = {'form': form}
        return render(request,"pick10/profile_form.html", context)

    def post(self,request):
        user = request.user
        form = UserProfileForm(request.POST)
        context = {'form': form}
        if form.is_valid():
            cd = form.cleaned_data
            userprofile = UserProfile.objects.get(user=user)
            userprofile.company = cd['company']
            userprofile.preferredtz = cd['preferredtz']
            userprofile.save()
            return redirect('/pick10/')
        return render(request, 'pick10/user_profile.html', context)

