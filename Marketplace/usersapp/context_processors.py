from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Subscribers
from marketapp.models import Listingproducts, Subcategory, Category,Listingimages
from usersapp.models import Userprofile
from .forms import SubscriberForm
from django.contrib.auth.decorators import login_required
def Subscriber(request):
    # subsemail = Subscribers.objects.all()
    form = SubscriberForm()
    if request.method == 'POST':
        if 'subscriberform' in request.POST:
            form = SubscriberForm(request.POST)
            if form.is_valid():
                form.save()
                # return redirect('mainpage')
            else:
                print(f"Subscriberform is not Valid ...")
        else:
            print(f"NOT Subscriberform is calling ...")
    else:
        print(f"NOT REQUEST METHOD CALLING ...")
    return {'subscriber':form}
   
def TopRatedSlides(request):
   
    brandnew = Listingproducts.objects.filter(conditions='BrandNew')
    # brandnewImg = ListingImages.objects.filter(listingproducts__id=brandnew.id).distinct()
    return {'brandnew': brandnew,}


def AccountsProfile(request): 
    if request.user.is_authenticated:
        print("USerIs Authenticated")
        profile_obj = Userprofile.objects.get(user=request.user)
        return {'myprofile':profile_obj}

    else:
        print("Not Authenticated User")
    return {}
