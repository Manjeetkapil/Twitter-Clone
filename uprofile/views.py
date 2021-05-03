from django.shortcuts import render, redirect
from .forms import profileUpdateform, userUpdateform
from tweets.models import Tweets
from .models import Profile
from django.contrib.auth.models import User
from social.models import Follower, Following
from django.shortcuts import get_object_or_404
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


# @login_required(login_url='login')
def viewprofile(request, username=None):
    username = get_object_or_404(User, username=username)
    content = Profile.objects.all().filter(user=username)
    getfollowers = Follower.objects.all().filter(person=username)
    try:
        follower_count = getfollowers[0].follower.all().count()
    except:
        follower_count = 0
    getfollowing = Following.objects.all().filter(person=username)
    try:
        following_count = getfollowing[0].following.all().count()
    except:
        following_count = 0
    try:
        follower = getfollowers[0].follower.all()
    except:
        follower = []
    follows = False
    if request.user in follower:
        follows = True
    return render(request, 'uprofile/userprofile.html', {'content': content[0], 'puser': username, 'foer': follower_count, 'foing': following_count, 'follows': follows})


@login_required(login_url='login')
def viewfollower(request, username=None):
    username = get_object_or_404(User, username=username)
    getfollowers = Follower.objects.all().filter(person=username)
    try:
        follower = getfollowers[0].follower.all()
    except:
        follower = []
    return render(request, 'uprofile/follower.html', {'content': follower})


@login_required(login_url='login')
def viewfollowing(request, username=None):
    username = get_object_or_404(User, username=username)
    getfollowing = Following.objects.all().filter(person=username)
    try:
        following = getfollowing[0].following.all()
    except:
        following = []
    return render(request, 'uprofile/follower.html', {'content': following})


@login_required(login_url='login')
def follow_unfollow(request, username=None):
    username = get_object_or_404(User, username=username)
    userset = User.objects.all().filter(username=username)
    if request.method == 'POST':
        follows = request.POST['follows']
        print(follows)
        if (follows == "True"):
            Follower.objects.all().filter(person=username).first().follower.remove(request.user)
            Following.objects.all().filter(person=request.user).first().following.remove(username)
        else:
            try:
                Follower.objects.all().filter(person=username).first().follower.add(request.user)
            except:
                instance = Follower.objects.create(person=username)
                user_instance = request.user
                instance.follower.add(*user_instance)
            try:
                Following.objects.all().filter(person=request.user).first().following.add(username)
            except:
                instance = Following.objects.create(person=request.user)
                instance.following.add(*userset)
    return viewprofile(request, username=username)
