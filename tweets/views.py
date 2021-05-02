from django.shortcuts import render, redirect
from .forms import newTweetform, editTweetform
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tweets, Likes
from social.models import Follower, Following


@login_required(login_url='login')
def newtweet(request):
    if request.method == 'POST':
        form = newTweetform(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.tweeter = request.user
            tweet.save()
            messages.success(
                request, f'Tweeted Succesfully for {request.user.username}!')
        return redirect('newtweet')
    else:
        form = newTweetform(instance=request.user)
    return render(request, 'tweets/newtweet.html', {'form': form})


@login_required(login_url='login')
def mytweets(request):
    user = request.user
    content = Tweets.objects.all().filter(tweeter=user)
    for i in content:
        try:
            i.likes = Likes.objects.all().filter(tweet=i).first().liker.all().count
        except:
            i.likes = 0
    return render(request, 'tweets/mytweets.html', {'content': content})


@login_required(login_url='login')
def spetweet(request, pk):
    user = request.user
    content = Tweets.objects.filter(id=pk, tweeter=user)
    # print(content[0].tweet_time)
    return render(request, 'tweets/mytweets.html', {'content': content})


@login_required(login_url='login')
def edittweet(request, pk):
    if request.method == 'POST':
        form = editTweetform(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.tweeter = request.user
            tweet.id = pk
            tweet.save()
            messages.success(
                request, f'Tweeted Succesfully for {request.user.username}!')
            return redirect('mytweets')
    else:
        form = newTweetform(instance=request.user)
    return render(request, 'tweets/edittweet.html', {'form': form})


@login_required(login_url='login')
def likers(request):
    if request.method == 'POST':
        tweet = request.POST['tweet']
    else:
        tweet = None
    tweeter = Tweets.objects.all().filter(id=tweet).first()
    likers = Likes.objects.all().filter(tweet=tweeter).first().liker.all()
    return render(request, 'tweets/liker.html', {'likers': likers})


@login_required(login_url='login')
def homepage(request):
    try:
        following = Following.objects.all().filter(
            person=request.user).first().following.all()
    except:
        following = Following.objects.none()
    content = Following.objects.none()
    for i in following:
        content |= Tweets.objects.all().filter(tweeter=i)
    for i in content:
        try:
            i.likes = Likes.objects.all().filter(tweet=i).first().liker.all().count
        except:
            i.likes = 0
        tweeter = Tweets.objects.all().filter(id=i.pk).first()
        try:
            likers = Likes.objects.all().filter(tweet=tweeter).first().liker.all()
        except:
            likers = []
        flag = False
        if request.user in likers:
            flag = True
        i.liker = flag
    x = list(content.values())
    for i in range(len(x)):
        x[i]['tweeter'] = content[i].tweeter
    sorted_content = sorted(x, key=lambda k: k['tweet_time'], reverse=True)
    content_object = []
    from collections import namedtuple
    for i in sorted_content:
        object_name = namedtuple("ObjectName", i.keys())(*i.values())
        content_object.append(object_name)
    # print(content_object)
    return render(request, 'tweets/home.html', {'content': content_object})


@login_required(login_url='login')
def like_unlike(request):
    if request.method == 'POST':
        likes = request.POST['likes']
        id = request.POST['id']
        s = ''.join(filter(str.isdigit, id))
        pk = int(s)
        tweet = Tweets.objects.all().filter(id=pk).first()
        if (likes == "True"):
            Likes.objects.all().filter(tweet=tweet).first().liker.remove(request.user)
        else:
            try:
                Likes.objects.all().filter(tweet=tweet).first().liker.add(request.user)
            except:
                instance = Likes.objects.create(tweet=tweet)
                user_instance = request.user
                instance.liker.add(*user_instance)
    return homepage(request)
