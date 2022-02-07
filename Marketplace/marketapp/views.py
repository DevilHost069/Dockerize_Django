from unittest.result import failfast
from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Listingproducts,Userprofile,Category,Subcategory,Listingimages,Review 
from .forms import ListingForm,ReviewForm
from django.contrib import messages
from django.core.mail import send_mail
# Create your views here.
#   search_query = ''
#     if request.GET.get('search_query'):
#         search_query = request.GET.get('search_query')
#     tags = Tag.objects.filter(name__icontains = search_query)
#     projects = Project.objects.distinct().filter(
#         Q(title__icontains=search_query) |
#         Q(descriptions__icontains=search_query) | 
#         Q(owner__name__icontains=search_query) |
#         Q(tags__in=tags)
#     )
def mainpage(request):
    searchproduct_query = ''
    searchlocation_query = ''
    print(f"searchQuery: {request.GET.get('searchproduct_query')}")
    if request.GET.get('searchproduct_query') or request.GET.get('searchlocation_query'):
        searchproduct_query = request.GET.get('searchproduct_query')
        searchlocation_query = request.GET.get('searchlocation_query')
    # products = Listingproducts.objects.distinct().filter(
    #     Q(title__icontains=searchproduct_query) 
    #     # Q(city__icontains=searchlocation_query) |
    #     # Q(districts__icontains=searchlocation_query)
    # ) 
    products = Listingproducts.objects.distinct().filter(
        Q(title__icontains=searchproduct_query)
        ).prefetch_related('listingimages_set')
    
    
    count_bikes=Listingproducts.objects.filter(subcategory__name='Bikes').count()
    context = {'products': products,'count_bikes':count_bikes}
    return render(request, 'marketapp/mainpage.html', context)

def productwiseAutomobiles(request, data=None):
    product_page = 'Automobiles'
    if data == None:
        pass
    elif data in  ['Bikes','Car','Van','HeavyVechiles','PartsAccessories']:
        subcatobj = Listingproducts.objects.filter(subcategory__name=data).prefetch_related('listingimages_set')
        context = {'subcatobj':subcatobj, 'product_page':product_page}
        return render(request, 'marketapp/productwise.html', context)

def productwisepc(request,data=None):
    product_page_pc = 'PC'
    if data == None:
        pass
    elif data in ['Laptops','Laptops-Accessories','DesktopPC','Networking-Equipments','Graphics-Video-Cards','Printers-Scanners','Storage-Drives','Monitors']:
        subcatobjpc = Listingproducts.objects.filter(subcategory__name=data).prefetch_related('listingimages_set')
        context = {'subcatobjpc':subcatobjpc, 'product_page_pc':product_page_pc}
        return render(request, 'marketapp/productwise.html', context)

def productwisemobile(request, data=None):
    product_page_mobile = 'mobile'
    if data == None:
        pass
    elif data in ['Apple-Iphone','Samsung','Realmi','Oppo','Mi-Xiaomi','Nokia','OnePlus','Other-Phones']:
        subcatobjmobile = Listingproducts.objects.filter(subcategory__name=data).prefetch_related('listingimages_set')
        context = {'subcatobjmobile':subcatobjmobile, 'product_page_mobile':product_page_mobile}
        return render(request, 'marketapp/productwise.html', context)

def productwiseApparels(request, data=None):
    product_page_apparels = 'apparels'
    if data == None:
        pass
    elif data in ['BabyChildren-Accessories','BabyChildren-Clothing','Men-Clothing','Men-Accessories','Men-Shoes','Women-Accessories','Women-Clothing','Womens-shoes','Lauggage-Bags','Jewellery','Sunglasses','Watches',]:
        subcatobjapparels = Listingproducts.objects.filter(subcategory__name=data).prefetch_related('listingimages_set')
        context = {'subcatobjapparels':subcatobjapparels, 'product_page_apparels':product_page_apparels}
        return render(request, 'marketapp/productwise.html', context)

def productwiseRealState(request, data=None):
    product_page_RealState = 'RealState'
    if data == None:
        pass
    elif data in ['ForSale_Land','ForSale_House','ForSale_Appartments','ForRent_Shutter_Shop_Space','ForRent-Office_Space','ForRent-Land','ForRent-House','ForSale-Business-And-Shop',]:
        print(f"DatainURL: {data}")
        subcatobjRealState = Listingproducts.objects.filter(subcategory__name=data).prefetch_related('listingimages_set')
        for i in subcatobjRealState:
            for h in i.listingimages_set.all():
                print(f"HouseName is: {h.featured_image}")
        context = {'subcatobjRealState':subcatobjRealState, 'product_page_RealState':product_page_RealState}
        return render(request, 'marketapp/productwise.html', context)


def singleproduct(request,pk):
    singleitem = Listingproducts.objects.get(id=pk)
    itemsprofile = Userprofile.objects.distinct().get(listingproducts__owner=singleitem.owner)
    listingimages = Listingimages.objects.filter(listingproducts_id=singleitem.id)
    
   

    form = ReviewForm()
    if  request.method == 'POST':
        if 'reviewsubmit' in request.POST:
           
            form = ReviewForm(request.POST)
            if form.is_valid():
                    review = form.save(commit=False)
                    review.project = singleitem
                    review.owner = request.user.userprofile
                    review.save()
                    messages.success(request, 'Your review was successfully submitted!!!')
                    return redirect('singleproduct', pk=singleitem.id)
          
        elif 'reviewReplysubmit' in request.POST:
            form = ReviewForm(request.POST)
            reviewId = request.POST.get("reviewid")
            print(f"Debuging Review ID: {reviewId}")
            try:
                parent = Review.objects.get(id=reviewId)
            except Review.DoesNotExist:
                parent = None
            if form.is_valid():
                    review = form.save(commit=False)
                    review.project = singleitem
                    review.owner = request.user.userprofile
                    review.parent = parent
                    review.save()
                    messages.success(request, 'Your Reply was successfully submitted!!!')
                    return redirect('singleproduct', pk=singleitem.id)

        elif 'sendmail' in request.POST:
                name = request.POST.get('your_name')
                email = request.POST.get('your_email')
                message = request.POST.get('your_message')
                print(f"Sender name is {name} email is {email} and your messages are {message} ")
                
                send_mail(
                    name,
                    message,
                    'devilhost069@gmail.com',
                    [email],
                    fail_silently=False
                )
                return redirect('mainpage')
        else:
                print(f"Something went wrong{request.POST.get('sendmail')}")
    context = {'singleitem':singleitem,'listingimages':listingimages,'form': form,'itemsprofile':itemsprofile}
    return render(request, 'marketapp/singleproducts.html', context)

def Addlikes(request, pk):
        singleitem = Listingproducts.objects.get(id=pk)

        is_dislike = False

        for dislike in singleitem.dislikes.all():
            if dislike == request.user.userprofile:
                is_dislike = True
                break

        if is_dislike:
            singleitem.dislikes.remove(request.user.userprofile)

        is_like = False

        for like in singleitem.likes.all():
            if like == request.user.userprofile:
                is_like = True
                break

        if not is_like:
            singleitem.likes.add(request.user.userprofile)

        if is_like:
            singleitem.likes.remove(request.user.userprofile)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
def AddDislikes(request,pk):
        singleitem = Listingproducts.objects.get(id=pk)

        is_like = False

        for like in singleitem.likes.all():
            if like == request.user.userprofile:
                is_like = True
                break

        if is_like:
            singleitem.likes.remove(request.user.userprofile)

        is_dislike = False

        for dislike in singleitem.dislikes.all():
            if dislike == request.user.userprofile:
                is_dislike = True
                break

        if not is_dislike:
            singleitem.dislikes.add(request.user.userprofile)

        if is_dislike:
            singleitem.dislikes.remove(request.user.userprofile)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
# AJAX
def load_subcategory(request):
    category_id = request.GET.get('category_id')
    categoryformValue = Category.objects.get(id=category_id)
    print(f"CategoryValue: {categoryformValue}")
    print(f"CategoryValue: {category_id}")
    subcategoryobj = Subcategory.objects.filter(category_id=category_id)
    return render(request, 'marketapp/dropdownlist.html', {'subcategoryobj': subcategoryobj, 'categoryformValue':categoryformValue})
    # return JsonResponse(list(subcategoryobj.values('id', 'name')), safe=False)
    
@login_required(login_url='userlogin')
def publishproducts(request):
    category = Category.objects.all()
    form = ListingForm()
    print("You are on publised page !!!")
    if request.method == 'POST':
        if 'productlist' in request.POST:
                images = request.FILES.getlist('listingimg')
                form = ListingForm(request.POST, request.FILES)
                if form.is_valid():
                    listingdata=form.save(commit=False)
                    listingdata.owner=request.user.userprofile
                    listingdata.save()
                    if images:
                        for image in images:
                            # print(f"Image Name: {image}")
                            Listingimages.objects.create(featured_image=image,listingproducts=listingdata)
                    else:
                        print(f"No any Images loaded: {images}")
                        return redirect('mainpage')      
                    messages.add_message(request, messages.INFO,'Your Data has been Successfully Uploaded !!!')         
                    return redirect('mainpage')
                else:
                     print(f"Invalid  form: {form.errors}")  
               
        else:
            print(f"Another forrm is disturbing ....")
    else:
        print(f"Submit request method not called: {request.method}")
    context = {'form': form,'category':category}
    return render(request, 'marketapp/submitform.html', context)

@login_required(login_url='userlogin')
def editAds(request,pk):
    profile = request.user.userprofile
    adslist = profile.listingproducts_set.get(id=pk)
    # print(f"GetSQLQuery: {connection.queries}")
    form = ListingForm(instance=adslist)
    
    if request.method == 'POST':
        form = ListingForm(request.POST,request.FILES,instance=adslist)
        if form.is_valid():
            form.save()
            return redirect('usersHome')
    
    context ={'form':form}
    return render(request,'marketapp/submitform.html',context)

@login_required(login_url='userlogin')
def deleteAds(request,pk):
    profile = request.user.userprofile
    adslist = profile.listingproducts_set.get(id=pk)
    page = 'adslist'
    if request.method == 'POST':
        adslist.delete()
        return redirect('usersAds')
    context = {'delobj': adslist,'page':page}
    return render(request,'usersapp/userhome.html',context)

# employee_set = employess ---> (related_name='employees')
# Department.objects.get(name='devil').employee_set.all()
# Department.objects.all().filter(employee_set__name__startswith='bhuwan') ----> will outs Department name of employee table
# Employee.objects.filter(name='evil').department.name ----> will outs department name from Employee Table
# Employee.objects.filter(department__name='Accounts') ---> Will outs the name of employee of Account Departs

#  Userprofile.objects.filter(listingproducts__owner=singleitem.owner)
# SQLQuery:-  SELECT `usersapp_userprofile`.`user_id`, `usersapp_userprofile`.`name`, `usersapp_userprofile`.`locations`, `usersapp_userprofile`.`listingcity`, `usersapp_userprofile`.`phonnumber`, `usersapp_userprofile`.`email`, `usersapp_userprofile`.`social_facebook`, `usersapp_userprofile`.`profile_image`, `usersapp_userprofile`.`created`, `usersapp_userprofile`.`id` 
# FROM `usersapp_userprofile` INNER JOIN `marketapp_listingproducts` ON (`usersapp_userprofile`.`id` = `marketapp_listingproducts`.`owner_id`) WHERE `marketapp_listingproducts`.`owner_id` = e7f005a26d9240fea0601a89a6e6bc7d