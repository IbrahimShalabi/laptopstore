from django.db.models.signals import post_save
from django.contrib.auth.models import User,Group
from .models import Coustomer




def coustomer_created_profile(sender,instance,created,**kwargs):
    if  created:
        group=Group.objects.get(name="customar")
        instance.groups.add(group)
        
        Coustomer.objects.create(
            user=instance,
            name=instance.username
        )
        print("Customar profle created!!!!")
post_save.connect(coustomer_created_profile,sender=User)


