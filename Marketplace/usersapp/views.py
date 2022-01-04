from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomUserCreationForm, ProfileForm
from .models import Userprofile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

def userprofile(request):
    profile = Userprofile.objects.all()
    context = {'profile': profile}
    return render(request, 'usersapp/userprofile.html', context)

def usersregister(request):
    page = "register"
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"Successfully Register user !!!")
            login(request,user)
            return redirect('editprofile')
        else:
            messages.success(request, "An Error has been Occured")
    context = {'form':form, 'page':page}
    return render(request, 'usersapp/login_registrationform.html', context)

def userlogin(request):
    if request.user.is_authenticated:
        return redirect('mainpage')
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't Exits !!!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in  request.GET else 'usersHome')
    return render(request, 'usersapp/login_registrationform.html')

def userlogout(request):
    logout(request)
    messages.info(request,"Username was Sucessfully logout !!!")
    return redirect('userlogin')


@login_required(login_url='userlogin')
def editprofile(request):
    profile=request.user.userprofile
    form = ProfileForm(instance=profile)
    if request.method == "POST":
        if 'profilecreate' in request.POST:
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
                return redirect('mainpage')
            else:
                print(f"Not valid form: {form}")
        else:
            print('Another form is disturbing ...')
    context={'form':form}
    return render(request,'usersapp/editprofile.html', context)

@login_required(login_url='userlogin')
def usersHome(request):
    profile = request.user.userprofile
    page = 'usershomepage'
    context = {'page':page ,'homeprofile':profile }
    return render(request, 'usersapp/userhome.html',context)

@login_required(login_url='userlogin')
def usersAds(request):
    page = 'adslist'
    profile = request.user.userprofile
    mylisting = profile.listingproducts_set.all()
    print(f"ProfileType: {type(profile)}")
    print(f"usersAdsSQLQuery: {mylisting.query}")
    # context ={'page':page,}
    context ={'page':page,'mylisting':mylisting}
    return render(request,'usersapp/userhome.html',context)

@login_required(login_url='userlogin')
def buyersMessage(request):
    page = 'buyersmessage'
    context = {'page': page}
    return render(request,'usersapp/userhome.html',context)
