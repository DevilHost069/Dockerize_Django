from django.db import models
from django.db.models.fields import DateTimeField
from usersapp.models import Userprofile
from django.contrib.auth.models import User
import uuid
# Create your models here.

ads_expiry = (
    ('TwoWeaks', 'Two Weaks'),
    ('1Months', 'One Months'),
    ('2Months', 'Two Months'),
    ('3Months', 'Three Months'),
    ('4Months', 'Four Months'),
    ('5Months', 'Five Months'),
    ('6Months', 'Six Months'),
   
)

condition_type = (
        ('LikeNew', 'Like New'),
        ('BrandNew', 'Brand New')
    )


negotiate = (
    ('yes','Yes'),
    ('fixedprice','Fixed price')
)
isdeliver = (
    ('yes','Yes'),
    ('no','No')
)
delivery_area = (
    ('withInMyArea','With in my Area'),
    ('withInMyCity','With in my City'),
    ('anywhere','Any where in Nepal')
)
auto_anchal = (
    ('koshi','Koshi'),
    ('mechi','Mechi'),
    ('bagmati','Bagmati'),
    ('sagarmatha','Sagarmatha'),
    ('lumbini','Lumbini'),
    ('gandaki','Gandaki'),
    ('janakpur','Janakpur'),
    ('mahakali','Mahakali'),
    ('karnali','Karnali'),
    ('narayani','Narayani'),
    ('rapti','Rapti'),
    ('seti','Seti'),
    ('bheri','Bheri'),
    ('dhawalagiri','Dhawalagiri')
)
storage_type = (
    ('SSD','SSD'),
    ('HDD','HDD'),
    ('both','Both')
)
processors_type = (
    ('pentium4','Intel Pentium 4'),
    ('pentiumDualCore','Intel Pentium Dual Core'),
    ('intelCeleron','Intel Celeron or Dual'),
    ('intelCorei3','Intel core i3'),
    ('intelCorei5','Intel core i5'),
    ('intelCorei7','Intel core i7'),
    ('intelCorei9','Intel core i9'),
    ('amdRyzen3','AMD Ryzen 3'),
    ('amdRyzen5','AMD Ryzen 5'),
    ('amdRyzen7','AMD Ryzen 7'),
    ('others','others')
)
processorsgen_type = (
    ('donotknow','Donot Know'),
    ('4th','4th'),
    ('5th','5th'),
    ('6th','6th'),
    ('7th','7th'),
    ('8th','8th'),
    ('9th','9th'),
    ('10th','10th'),
    ('11th','11th'),
)
class Category(models.Model):
    name = models.CharField(max_length=40,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    
class Listingproducts(models.Model):
    owner = models.ForeignKey(Userprofile, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL,blank=True, null=True)
    title = models.CharField(max_length=200,null=True)
    price = models.IntegerField(null=True)
    isnegotiate = models.CharField(max_length=200, choices=negotiate, null=True)
    adsexpiry = models.CharField(max_length=200, choices=ads_expiry, null=True)
    deliverycharges = models.CharField(max_length=200,blank=True,null=True)  
    isdeliver = models.CharField(max_length=200, choices=isdeliver, null=True)
    deliveryarea = models.CharField(max_length=200, choices=delivery_area, null=True)
    conditions = models.CharField(max_length=200, choices=condition_type, null=True)
    userfor = models.CharField(max_length=200, blank=True, null=True)
    descriptions = models.TextField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
  
    def __str__(self):
        return self.title
    
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset
    
class Listingimages(models.Model):
    listingproducts = models.ForeignKey(Listingproducts,on_delete=models.CASCADE,null=True)
    featured_image = models.ImageField(null=True, default='default.jpg')
    created = models.DateTimeField(auto_now_add=True,null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    def __str__(self):
        return f"ListingImage {self.featured_image}"
# class AutovechFeatures(models.Model):
#     listingproducts = models.ForeignKey(Listingproducts,on_delete=models.CASCADE,null=True)
#     lotno = models.CharField(max_length=200,null=True) 
#     enginecc = models.IntegerField(blank=True,null=True) 
#     kilometersrun = models.IntegerField(blank=True,null=True)
#     makeyear = models.DateField(null=True,blank=True)
#     autoanchal = models.CharField(max_length=200, choices=auto_anchal, null=True)
    
#     def __str__(self):
#         return str("Automobiles Features")

# class ComputersFeatures(models.Model):
#     listingproducts = models.ForeignKey(Listingproducts,on_delete=models.CASCADE,null=True)
#     processors = models.CharField(max_length=200,choices= processors_type, null=True)
#     processorsgen = models.CharField(max_length=200,choices=processorsgen_type , null=True)
#     memory = models.CharField(max_length=200,null=True)
#     storagetype = models.CharField(max_length=200,choices= storage_type, null=True)
#     storagegbtb = models.CharField(max_length=200,null=True)
    
#     def __str__(self):
#         return str("Computers Items Features")

class Review(models.Model):
        vote_type = (('up', 'Up Vote'), ('down', 'Down Vote'))
        owner = models.ForeignKey(Userprofile, on_delete=models.CASCADE, null=True)
        body = models.TextField(null=True, blank=True)
        project = models.ForeignKey(Listingproducts, on_delete=models.CASCADE, null=True)
        value = models.CharField(max_length=200, choices=vote_type, null=True)
        created = models.DateTimeField(auto_now_add=True)
        id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

        class Meta:
            unique_together = [['owner', 'project']]
        def __str__(self):
            return str(self.value)


