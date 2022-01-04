from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms

from  .models import Listingproducts, Review, Subcategory

from django.core import validators

def starts_with_a(value):
    if value[0] != 'A':
        raise forms.ValidationError('Name should starts with A')
class ListingForm(forms.ModelForm):
    # name = forms.CharField(validators=[validators.MaxLengthValidator(25)])
    # email = forms.EmailField(validators=[starts_with_a])
    class Meta:
        model = Listingproducts
        exclude = ['owner']
        # labels = {'title':'Enter title','phon':'Enter phon', 'name':'Enter name','email':'Enter email','price':'Enter price','isdeliver':'Enter isdeliver','country':'Enter country'}
        # error_messages = {'name':{'required':'Name field is required'}}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.none()
        print(f"Debug mode {self.data}")
        print(f"debug id : {self.data.get('category')}")
        if 'category' in self.data:
            try:
                category_id = self.data.get('category')
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
# class VechForm(forms.ModelForm):
#     class Meta:
#         model = AutovechFeatures
#         exclude = ['listingproducts']
# class ComputerForm(forms.ModelForm):
#     class Meta:
#         model = ComputersFeatures
#         exclude = ['listingproducts']

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['body']