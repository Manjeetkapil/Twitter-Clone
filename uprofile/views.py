from django.shortcuts import render, redirect
from .forms import profileUpdateform, userUpdateform
# Create your views here.
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def profile(request):
    if request.method == 'POST':
        u_form = userUpdateform(request.POST, instance=request.user)
        p_form = profileUpdateform(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = userUpdateform(instance=request.user)
        p_form = profileUpdateform(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'uprofile/profile.html', context)


@login_required(login_url='login')
def homepage(request):
    return render(request, 'uprofile/home.html')
