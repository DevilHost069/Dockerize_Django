from django.contrib import admin
from .models import Listingproducts, Review,Category,Subcategory,Listingimages

admin.site.register(Listingproducts)
admin.site.register(Review)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Listingimages)

