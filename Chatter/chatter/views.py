from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import datetime
from django import forms
from .models import User, GlobalMessage, Friends, ProfilePic, Direct, DirectMessage, Group, GroupMessage, GroupInvite
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class ImageForm(forms.ModelForm):
    class Meta:
        model = ProfilePic
        fields = ['image']

# Create your views here.


def index(request):
    return render(request, "chatter/index.html")

@csrf_exempt
def global_message(request):
    if request.method == "POST":
        try:
            user_message = GlobalMessage.objects.filter(messager = request.user).order_by("-id")[0]
            tomorrow = user_message.date + datetime.timedelta(1)
        except:
            tomorrow = datetime.date.today()
        if datetime.date.today() >= tomorrow:
            data = json.loads(request.body)
            content = data.get("content")
            global_message = GlobalMessage(content = content, messager = request.user)
            global_message.save()
            return HttpResponse(status=204)
        else:
            print(datetime.date.today())
            return JsonResponse({'error': f'You are on cooldown. Please wait until {tomorrow}'})
    

@csrf_exempt
def reply_global(request):
    if request.method == "POST":
        try:
            user_message = GlobalMessage.objects.filter(messager = request.user).order_by("-id")[0]
            tomorrow = user_message.date + datetime.timedelta(1)
        except:
            tomorrow = datetime.date.today()
        if datetime.date.today() >= tomorrow:
            data = json.loads(request.body)
            content = data.get("content")
            reply = data.get("reply")
            global_message = GlobalMessage(content = content, reply = reply, messager = request.user)
            global_message.save()
            return HttpResponse(status=204)
        else:
            print(datetime.date.today())
            return JsonResponse({'error': f'You are on cooldown. Please wait until {tomorrow}'})

def get_global_message(request, id):
    messages = GlobalMessage.objects.all().order_by("-id")[:id]
    new_message = []
    for i in range(len(messages)):
        new_message.append(messages[len(messages) - (i+1)])

    return JsonResponse([message.serialize() for message in new_message], safe=False)

@csrf_exempt
def like_global(request, id):
    if request.method == "PUT":
        message = GlobalMessage.objects.get(pk = id)
        likers = message.likes.all()
        if request.user not in likers:
            message.likes.add(request.user)
        else:
            message.likes.remove(request.user)
        return HttpResponse(status=204)
    
def profile(request, username):
    user = User.objects.get(username = username)
    profile_pic = ProfilePic.objects.get(user = user)
    form = ImageForm(request.POST, request.FILES, instance = profile_pic)
    friend_request = True
    pending = []
    direct = False
    invite = []
    try:
        friend = Friends.objects.get(follower = request.user, following = user)
    except:
        friend_request = False
    try:
        pending_request = Friends.objects.filter(following = request.user)
        for i in pending_request:
            follower = User.objects.get(username = i.follower)
            try:
                check = Friends.objects.get(follower = request.user, following = follower)
            except:
                pending.append(i)
    except:
        pass
    
    try:
        direct = Direct.objects.get(friend_1 = request.user, friend_2 = user)
    except:
        try:
            direct = Direct.objects.get(friend_1 = user, friend_2 = request.user)
        except:
            pass

    try:
        groups = GroupInvite.objects.filter(user = request.user)
    except:
        pass
            
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile", args = (username, ))) 
    return render(request, "chatter/profile.html",{
        "profile": user,
        "profile_pic": profile_pic,
        "form": form,
        "friends": friend_request,
        "pending_request": pending,
        "direct": direct, 
        "groups": groups,
    })

def update_bio(request, username):
    if request.method == "POST":
        bio = request.POST["bio"]
        user = User.objects.get(username=username)
        user.bio = bio
        user.save()
        return HttpResponseRedirect(reverse("profile", args = (username, ))) 

def friend_request(request, username):
    if request.method == "POST":
        target = request.POST["user"]
        user = User.objects.get(username = target)
        friend = Friends(follower = request.user, following = user)
        friend.save()
        try:
            pending_request = Friends.objects.filter(following = request.user)
            for i in pending_request:
                follower = User.objects.get(username = i.follower)
                try:
                    check = Friends.objects.get(follower = request.user, following = follower)
                    try:
                        direct = Direct.objects.get(Q(friend_1 = request.user, friend_2 = follower) | Q(friend_2 = request.user, friend_1 = follower))
                    except:
                        direct = Direct(friend_1 = request.user, friend_2 = follower)
                        direct.save()
                except:
                    pass
        except:
            pass
        return HttpResponseRedirect(reverse("profile", args = (username, ))) 

def unfriend_request(request, username):
    if request.method == "POST":
        target = request.POST["user"]
        user = User.objects.get(username = target)
        try:
            friend = Friends.objects.get(follower = request.user, following = user)
            friend.delete()
        except:
            pass
        try:
            friend = Friends.objects.get(follower = user, following = request.user)
            friend.delete()
        except:
            pass
        try:
            direct = Direct.objects.get(friend_1 = request.user, friend_2 = user)
            direct.delete()
            friend_2 = Friends.objects.get(follower = user, following=request.user)
            friend_2.delete()
        except:
            pass
        try:
            direct = Direct.objects.get(friend_1 = user, friend_2 = request.user)
            direct.delete()
            friend_2 = Friends.objects.get(follower = user, following=request.user)
            friend_2.delete()
        except:
            pass
        return HttpResponseRedirect(reverse("profile", args = (username, ))) 
    
def search(request):
    return render(request, "chatter/search.html")

def search_friends(request):
    if request.method == "POST":
        friend = request.POST["friends"]
        friends = User.objects.filter(username__icontains=friend)
        print(friends)
        return render(request, "chatter/search.html",{
            "friends": friends,
        })
    

def direct_home(request):
    friends = Direct.objects.filter(Q(friend_1 = request.user) | Q(friend_2 = request.user))
    for i in range(len(friends)):
        if friends[i].friend_1 == request.user:
            image = ProfilePic.objects.get(user = friends[i].friend_2)
            setattr(friends[i], 'image', image.image)
            try:
                last_message = DirectMessage.objects.filter(direct = friends[i]).order_by("-id")[0]
                setattr(friends[i], 'last_message', last_message.content)
            except:
                pass
            
            
        else:
            image = ProfilePic.objects.get(user = friends[i].friend_1)
            
            setattr(friends[i], 'image', image.image)
            try:
                last_message = DirectMessage.objects.filter(direct = friends[i]).order_by("-id")[0]
                setattr(friends[i], 'last_message', last_message.content)
            except:
                pass

    return render(request, "chatter/direct_home.html",{
        "friends": friends,
    })

def direct(request, id):
    direct = Direct.objects.get(pk = id)
    if request.user == direct.friend_1:
        friend = direct.friend_2
    else:
        friend = direct.friend_1
    image = ProfilePic.objects.get(user = friend)
    return render(request, "chatter/direct.html", {
        "friend": friend,
        "image":image,
        "direct": direct,

    })

@csrf_exempt
def direct_message(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        direct = Direct.objects.get(pk = id)
        direct_message = DirectMessage(direct = direct, content = content, messager = request.user)
        direct_message.save()
        return HttpResponse(status=204)

def get_direct_message(request, id, num):
    direct = Direct.objects.get(pk = id)
    messages = DirectMessage.objects.filter(direct = direct).order_by("-id")[:num]
    new_message = []
    for i in range(len(messages)):
        new_message.append(messages[len(messages) - (i+1)])
    return JsonResponse([message.serialize() for message in new_message], safe=False)

@csrf_exempt
def like_direct(request, id):
    if request.method == "PUT":
        message = DirectMessage.objects.get(pk = id)
        likers = message.likes.all()
        if request.user not in likers:
            message.likes.add(request.user)
        else:
            message.likes.remove(request.user)
        return HttpResponse(status=204)
    
@csrf_exempt
def reply_direct(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        reply = data.get("reply")
        direct = Direct.objects.get(pk = id)
        direct_message = DirectMessage(direct = direct, content = content, reply = reply, messager = request.user)
        direct_message.save()
        return HttpResponse(status=204)
    


def group_home(request):
    groups = Group.objects.all().order_by("-id")
    display_groups = []
    user_groups = []
    for i in groups:
        if request.user in i.members.all():
            setattr(i, 'member_count', i.members.count())
            try:
                last_message = GroupMessage.objects.filter(group = i).order_by("-id")[0]
                setattr(i, 'last_message', last_message)
            except:
                pass
            user_groups.append(i)
        else:
            setattr(i, 'member_count', i.members.count())
            display_groups.append(i)
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST["description"]
        category = request.POST["category"]
        group = Group(group_name = name, owner = request.user, description = description, category = category)
        group.save()
        group.members.add(request.user)
        group.save()
        return HttpResponseRedirect(reverse("group_home")) 
    return render(request, "chatter/group_home.html", {
        "groups": display_groups,
        "user_groups": user_groups,

    })

def group_join(request, id):
    if request.method == "POST":
        group = Group.objects.get(pk = id)
        members = group.members.all()
        if request.user not in members:
            group.members.add(request.user)
            try:
                invite = GroupInvite.objects.get(group = group, user = request.user)
                invite.delete()
            except:
                pass
        else:
            group.members.remove(request.user)
        return HttpResponseRedirect(reverse("group_home")) 
    
def group(request, id):
    everyone = User.objects.all()
    group = Group.objects.get(pk = id)
    members = group.members.all()
    invite = []
    for i in range(len(everyone)):
        if everyone[i] not in members:
            invite.append(everyone[i])
    return render(request, "chatter/group.html", {
        "group":group,
        "members":members,
        "invite": invite,

    })

@csrf_exempt
def group_message(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        group = Group.objects.get(pk = id)
        group_message = GroupMessage(group = group, content = content, messager = request.user)
        group_message.save()
        return HttpResponse(status=204)

def get_group_message(request, id, num):
    group = Group.objects.get(pk = id)
    messages = GroupMessage.objects.filter(group = group).order_by("-id")[:num]
    new_message = []
    for i in range(len(messages)):
        new_message.append(messages[len(messages) - (i+1)])
    return JsonResponse([message.serialize() for message in new_message], safe=False)

                
@csrf_exempt
def like_group(request, id):
    if request.method == "PUT":
        message = GroupMessage.objects.get(pk = id)
        likers = message.likes.all()
        if request.user not in likers:
            message.likes.add(request.user)
        else:
            message.likes.remove(request.user)
        return HttpResponse(status=204)
    
@csrf_exempt
def reply_group(request, id):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("content")
        reply = data.get("reply")
        group = Group.objects.get(pk = id)
        group_message = GroupMessage(group = group, content = content, reply = reply, messager = request.user)
        group_message.save()
        return HttpResponse(status=204)
    
def group_invite(request, id):
    if request.method == "POST":
        member = request.POST["invite"]
        try:
            user = User.objects.get(username = member)
            group = Group.objects.get(pk=id)
            if user in group.members.all():
                return HttpResponseRedirect(reverse("group", args = (id, ))) 
            invite = GroupInvite(user = user, group = group)
            invite.save()
            return HttpResponseRedirect(reverse("group", args = (id, ))) 
        except:
            return HttpResponseRedirect(reverse("group", args = (id, ))) 



def search_groups(request):
     if request.method == "POST":
        search = request.POST["groups"]
        groups = Group.objects.filter(Q(group_name__icontains = search)| Q(category__icontains = search))
        for i in groups:
            setattr(i, 'member_count', i.members.count())
            if request.user in i.members.all():
                setattr(i, 'is_member', True)
        return render(request, "chatter/search.html",{
            "groups": groups,
        })
     
def reject_group(request, username):
    if request.method == "POST":
        group = request.POST['group']
        g = Group.objects.get(pk = group)
        invite = GroupInvite.objects.filter(user = request.user, group = g)
        invite[0].delete()
        return HttpResponseRedirect(reverse("profile", args = (username, ))) 





def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "chatter/index.html", {
                "message": "Invalid username and/or password."
            })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "chatter/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile_pic = ProfilePic(user = user)
            profile_pic.save()
        except IntegrityError:
            return render(request, "chatter/register.html", {
                "message": "Username already taken. Please choose another username"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "chatter/register.html")


    


