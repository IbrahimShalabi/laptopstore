from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Coustomer
from .models import Order
from django import forms
from .models import Laptop


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']  # تعديل الحقول حسب الحاجة


class CustomerForm(ModelForm): 
    class Meta: 
        model = Coustomer
        fields = "__all__"
        exclude=['user']


class Createnewuser(UserCreationForm):
    class Meta:  
        model = User
        fields = ['username','email','password1','password2']


# في ملف forms.py
from django import forms
from .models import Laptop, Tag

class LaptopForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)  # لتحديد الـ Tags

    class Meta:
        model = Laptop
        fields = ['name', 'category', 'ram', 'rom', 'cpu', 'gpu', 'weight', 'size_battery', 'size_monitor', 'camera', 'fingerprint', 'price', 'description', 'tag']


class LaptopForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), required=False)  # لتحديد الـ Tags

    class Meta:
        model = Laptop
        fields = ['name', 'category', 'ram', 'rom', 'cpu', 'gpu', 'weight', 'size_battery', 'size_monitor', 'camera', 'fingerprint', 'price', 'description', 'tag', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5']



class ContactForm(forms.Form):
    email = forms.EmailField(label='Your Email Address', required=True)
    message = forms.CharField(widget=forms.Textarea, label='Your Message', required=True)


