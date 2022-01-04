from django.contrib.auth.models import User
from django.db import connection
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Listingproducts,Userprofile,Category,Subcategory,Listingimages
from .forms import ListingForm,ReviewForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
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
    products = Listingproducts.objects.distinct().filter(
        Q(title__icontains=searchproduct_query) 
        # Q(city__icontains=searchlocation_query) |
        # Q(districts__icontains=searchlocation_query)
    )
    # productslist = Listingproducts.objects.prefetch_related(listingimages)
    
    for i in products:
        print(i.title, i.category.name,i.owner.email)
    #     productsImage = Listingimages.objects.filter(listingproducts__id=i.id)
    
    #     print(f"Image: {productsImage.query}")
    # print(f"Image: {productslist}")
    
    count_bikes=Listingproducts.objects.filter(subcategory__name='Bikes').count()
    context = {'products': products,'count_bikes':count_bikes}
    return render(request, 'marketapp/mainpage.html', context)

def productwise(request, data=None):
    product_page = 'Automobiles'
    if data == None:
        pass
    elif data == 'Bikes':
        subcatobj = Listingproducts.objects.filter(subcategory__name=data)
        print(subcatobj.query)
        print(f"This is {data} {subcatobj}")
    context = {'subcatobj':subcatobj, 'product_page':product_page}
    return render(request, 'marketapp/productwise.html', context)
def singleproduct(request,pk):
    singleitem = Listingproducts.objects.get(id=pk)
    itemsprofile = Userprofile.objects.distinct().get(listingproducts__owner=singleitem.owner)
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
    context = {'singleitem':singleitem, 'form': form,'itemsprofile':itemsprofile}
    return render(request, 'marketapp/singleproducts.html', context)

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