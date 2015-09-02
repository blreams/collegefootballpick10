from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from models import UserProfile
from forms import UserProfileForm

class ProfileView:

    def get(self,request):
        user = request.user
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        form = UserProfileForm(instance=userprofile)
        tzchoices = [choice[0] for choice in form.fields['preferredtz'].choices]
        favchoices = sorted([choice[0] for choice in form.fields['favorite_team'].choices])
        context = {'form': form, 'tzchoices': tzchoices, 'favchoices': favchoices, 'userprofile': userprofile}
        return render(request,"pick10/profile_form.html", context)

    def post(self,request):
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        form = UserProfileForm(request.POST)
        tzchoices = [choice[0] for choice in form.fields['preferredtz'].choices]
        favchoices = sorted([choice[0] for choice in form.fields['favorite_team'].choices])
        context = {'form': form, 'tzchoices': tzchoices, 'favchoices': favchoices, 'userprofile': userprofile}
        if form.is_valid():
            cd = form.cleaned_data
            userprofile.company = cd['company']
            userprofile.preferredtz = cd['preferredtz']
            userprofile.favorite_team = cd['favorite_team']
            userprofile.save()
            return redirect('/pick10/')
        return render(request, 'pick10/profile_form.html', context)

