from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Coustomer(models.Model):
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,null=True)
    email = models.CharField(max_length=50,null=True)
    phone = models.CharField(max_length=50,null=True)
    avatar= models.ImageField(blank=True,null=True,default="avatar.png")
    age = models.CharField(max_length=50,null=True)
    date_Created = models.DateField(auto_now_add=True,null=True)


    def __str__(self):
        return self.name
   
class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)  
    def __str__(self):
        return self.name
    


class Laptop(models.Model):
    CATEGORY = [
        ('gaming', 'Gaming'),            # لابتوب مخصص للألعاب
        ('ultrabook', 'Ultrabook'),      # لابتوب خفيف ورفيع
        ('business', 'Business'),        # لابتوب مخصص للأعمال
        ('2-in-1', '2-in-1 Convertible'),# لابتوب يتحول إلى تابلت
        ('student', 'Student'),          # لابتوب للطلاب
        ('workstation', 'Workstation'),  # لابتوب محطة عمل
    ]
    Tag=models.ManyToManyField(Tag)
    name = models.CharField(max_length=50, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY, null=True)  # فئة اللابتوب
    ram = models.CharField(max_length=50, null=True)
    rom = models.CharField(max_length=50, null=True)
    cpu = models.CharField(max_length=50, null=True)
    gpu = models.CharField(max_length=50, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    size_battery = models.CharField(max_length=50, null=True)
    size_monitor = models.CharField(max_length=50, null=True)
    camera = models.CharField(max_length=50, null=True)
    fingerprint = models.CharField(max_length=50, null=True)
    price = models.FloatField(null=True)
    description = models.TextField(null=True)
    date_created = models.DateField(auto_now_add=True, null=True)

    image_1 = models.ImageField(upload_to='laptop_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='laptop_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='laptop_images/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='laptop_images/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='laptop_images/', blank=True, null=True)

    
    def __str__(self):
        return self.name
    @property
    def image_list(self):
        """Return a list of all non-empty images."""
        return [image.url for image in [self.image_1, self.image_2, self.image_3, self.image_4, self.image_5] if image]
   
from django.db import models
from django.contrib.auth.models import User
from .models import Laptop

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    laptop = models.ForeignKey(Laptop, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'laptop')  # لضمان أن كل مستخدم يمكنه إضافة نفس اللابتوب مرة واحدة فقط

    def __str__(self):
        return f"{self.user.username} - {self.laptop.name}"


class Order(models.Model):
    STATUS = [
        ('Pending', 'Pending'),       # قيد الانتظار
        ('Completed', 'Completed'),   # مكتمل
        ('Canceled', 'Canceled'),     # ملغي
        ('Shipped', 'Shipped'),       # تم الشحن
        ('Processing', 'Processing'), # قيد المعالجة
    ]
    Coustomer=models.ForeignKey(Coustomer,null=True,on_delete=models.SET_NULL)
    Laptop=models.ForeignKey(Laptop,null=True,on_delete=models.SET_NULL)
    Tag=models.ManyToManyField(Tag)
    date_created = models.DateField(auto_now_add=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS,null=True)  # حالة الطلب
