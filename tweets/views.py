from django.shortcuts import render, redirect
from .forms import newTweetform, editTweetform
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Tweets, Likes
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from social.models import Follower, Following
from .models import Comments, Commentsrel
from django.http import HttpResponseRedirect
from django.urls import reverse
from json import dumps


@login_required(login_url='login')
def newtweet(request):
    if request.method == 'POST':
        form = newTweetform(request.POST, auto_id=True)
        print(form)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.tweeter = request.user
            tweet.save()
            messages.success(
                request, f'Tweeted Succesfully for {request.user.username}!')
        return redirect('newtweet')
    else:
        form = newTweetform(instance=request.user, auto_id=True)
    print(form)
    fools = []
    for i in User.objects.all():
        fools.append(i.username)
    fool = {'fools': fools}
    dataJSON = dumps(fool)
    return render(request, 'tweets/newtweet.html', {'form': form, 'data': dataJSON})


@login_required(login_url='login')
def newcomment(request, pk):
    parent_tweet = Tweets.objects.all().filter(id=pk).first()
    if request.method == 'POST':
        form = newTweetform(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.tweeter = request.user
            tweet.save()
            current_tweet_list = Tweets.objects.all().filter(id=tweet.id)
            current_tweet = Tweets.objects.all().filter(id=tweet.id).first()
            try:
                Comments.objects.all().filter(
                    main_tweet=parent_tweet).first().your_tweet.add(current_tweet)
            except:
                instance = Comments.objects.create(main_tweet=parent_tweet)
                instance.your_tweet.add(*current_tweet_list)
            # try:
            Commentsrel.objects.create(
                commented_tweet=current_tweet, parent_tweet=parent_tweet)
            messages.success(
                request, f'Tweeted Succesfully for {request.user.username}!')
        return redirect('tweetdetail', pk)
    else:
        form = newTweetform(instance=request.user)
    return render(request, 'tweets/newtweet.html', {'form': form})


@login_required(login_url='login')
def mytweets(request, username=None):
    username = get_object_or_404(User, username=username)
    content = Tweets.objects.all().filter(tweeter=username)
    all_tweets = Tweets.objects.all()
    for i in all_tweets:
        try:
            retweeters = i.retweeted.all()
            if username in retweeters:
                content |= Tweets.objects.all().filter(id=i.id)
        except:
            pass
    x = list(content.values())
    for i in range(len(x)):
        x[i]['tweeter'] = content[i].tweeter
        try:
            x[i]['likes'] = Likes.objects.all().filter(
                tweet=content[i]).first().liker.all().count
        except:
            x[i]['likes'] = 0
        try:
            x[i]['retweets'] = content[i].retweeted.all().count
        except:
            x[i]['retweets'] = 0
        try:
            retweeter = content[i].retweeted.all()
        except:
            retweeter = content[i].retweeted.none()
        rflag = False
        if request.user in retweeter:
            rflag = True
        x[i]['retweeter'] = rflag
        tweeter = Tweets.objects.all().filter(id=x[i]['id']).first()
        try:
            likers = Likes.objects.all().filter(tweet=tweeter).first().liker.all()
        except:
            likers = []
        flag = False
        if request.user in likers:
            flag = True
        x[i]['liker'] = flag
    sorted_content = sorted(x, key=lambda k: k['tweet_time'], reverse=True)
    content_object = []
    from collections import namedtuple
    for i in sorted_content:
        object_name = namedtuple("Object", i.keys())(*i.values())
        content_object.append(object_name)
    print(content_object)
    return render(request, 'tweets/mytweets.html', {'content': content_object, 'username': username})


def getcount(request, content):
    try:
        content.likes = Likes.objects.all().filter(
            tweet=content).first().liker.all().count
    except:
        content.likes = 0
    try:
        content.retweets = content.retweeted.all().count
    except:
        content.retweets = 0
    try:
        retweeter = content.retweeted.all()
    except:
        retweeter = content.retweeted.none()
    rflag = False
    if request.user in retweeter:
        rflag = True
    content.retweeter = rflag
    try:
        likers = Likes.objects.all().filter(tweet=content).first().liker.all()
    except:
        likers = []
    flag = False
    if request.user in likers:
        flag = True
    content.liker = flag
    return content


@login_required(login_url='login')
def spetweet(request, pk):
    tweet = Tweets.objects.filter(id=pk).first()
    content = getcount(request, tweet)
    comment = Comments.objects.all().filter(
        main_tweet=tweet).first()
    try:
        comment = comment.your_tweet.all()
    except:
        comment = []
    for i in comment:
        i = getcount(request, i)
    print(comment)
    return render(request, 'tweets/particular.html', {'content': content, 'comment': comment})


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
    try:
        likers = Likes.objects.all().filter(tweet=tweeter).first().liker.all()
    except:
        likers = []
    return render(request, 'tweets/liker.html', {'likers': likers})


def changing_object(request, content):
    x = list(content.values())
    for i in range(len(x)):
        tweet = Tweets.objects.all().filter(id=content[i].id).first()
        try:
            x[i]['comments'] = Comments.objects.all().filter(
                main_tweet=tweet).first().your_tweet.all()
        except:
            pass
        try:
            x[i]['retweets'] = content[i].retweeted.all().count
        except:
            x[i]['retweets'] = 0
        try:
            retweeter = content[i].retweeted.all()
        except:
            retweeter = content[i].retweeted.none()
        rflag = False
        if request.user in retweeter:
            rflag = True
        x[i]['retweeter'] = rflag
        x[i]['tweeter'] = content[i].tweeter
        try:
            x[i]['likes'] = Likes.objects.all().filter(
                tweet=content[i]).first().liker.all().count
        except:
            x[i]['likes'] = 0
        tweeter = Tweets.objects.all().filter(id=x[i]['id']).first()
        try:
            likers = Likes.objects.all().filter(tweet=tweeter).first().liker.all()
        except:
            likers = []
        flag = False
        if request.user in likers:
            flag = True
        x[i]['liker'] = flag
    sorted_content = sorted(x, key=lambda k: k['tweet_time'], reverse=True)
    content_object = []
    from collections import namedtuple
    for i in sorted_content:
        object_name = namedtuple("ObjectName", i.keys())(*i.values())
        content_object.append(object_name)
    return content_object


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
    objects = changing_object(request, content)
    content_object = []
    for i in objects:
        try:
            j = changing_object(request, i.comments)
            i = i._replace(comments=j)
            content_object.append(i)
        except:
            content_object.append(i)
    print(content_object)
    return render(request, 'tweets/home.html', {'content': content_object})


@ login_required(login_url='login')
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def retweet(request):
    if request.method == 'POST':
        _retweeted = request.POST['retweeted']
        id = request.POST['id']
        s = ''.join(filter(str.isdigit, id))
        pk = int(s)
        tweet = Tweets.objects.all().filter(id=pk).first()
        if (_retweeted == "True"):
            tweet.retweeted.remove(request.user)
        else:
            try:
                tweet.retweeted.add(request.user)
            except:
                pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
