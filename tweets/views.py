from django.shortcuts import render, redirect
from .forms import newTweetform, editTweetform
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tweets


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
    # print(content[0].tweet)
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
