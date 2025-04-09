from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Coustomer)
admin.site.register(Laptop)
admin.site.register(Order)
admin.site.register(Tag)