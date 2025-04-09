from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import*
from .forms import * 
from .filters import ProductFilter 
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from .decorators import notlogedusers,allowedusers,forAdmin
from django.contrib.auth.models import Group
import requests
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.db.models import Q 

# Create your views here.

@login_required(login_url='login')
@forAdmin
def home(request):
    costomer = Coustomer.objects.all()  # تأكد من أن الاسم صحيح
    orders = Order.objects.all()

    num_of_order = orders.count()
    num_Pending = orders.filter(status='Pending').count()
    num_Completed = orders.filter(status='Completed').count()
    num_Canceled = orders.filter(status='Canceled').count()
    num_Shipped = orders.filter(status='Shipped').count()
    num_Processing = orders.filter(status='Processing').count()

    
    context = {
        'costomer': costomer,
        'orders': orders,
        'num_of_order': num_of_order,
        'num_Pending': num_Pending,
        'num_Completed': num_Completed,
        'num_Canceled': num_Canceled,
        'num_Shipped': num_Shipped,
        'num_Processing': num_Processing,
    }
    return render(request, 'laptopstore/dashboard.html', context)

@login_required(login_url='login')
def laptops(request):
    query = request.GET.get('q', '')  # قراءة استعلام البحث
    if query:
        laptops = Laptop.objects.filter(
            Q(name__icontains=query) | 
            Q(category__icontains=query) |
            Q(cpu__icontains=query) |
            Q(ram__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        laptops = Laptop.objects.all()

    context = {
        'laptops': laptops,
        'query': query,  # إعادة تمرير استعلام البحث للقالب
    }
    return render(request, 'laptopstore/laptops.html', context)

@login_required(login_url='login')
def customer(request,pk):
    customer=Coustomer.objects.get(id=pk)
    orders=customer.order_set.all()
    num_of_order=orders.count()
    searchfilter=ProductFilter(request.GET,queryset=orders)
    orders=searchfilter.qs
    context = {
        'customer': customer,
        'searchfilter': searchfilter,
        'orders': orders,
        'num_of_order': num_of_order,
         
    }
    return render(request,'laptopstore/customer.html',context)



@login_required(login_url='login')
@allowedusers(allowedgroup=['admin'])
def create(request,pk):
    orderformset=inlineformset_factory(Coustomer,Order,fields=('Laptop','status'),extra=1)
    customer=Coustomer.objects.get(id=pk)
    formset=orderformset(queryset=Order.objects.none(),instance=customer)
    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset=orderformset(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
            

    # context = {'form': form }
    context = {'formset': formset }
    return render(request, 'laptopstore/create_order.html', context)





@login_required(login_url='login')
def update_order(request, pk):
    order = get_object_or_404(Order, id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')  

    context = {'form': form, 'order': order}
    return render(request, 'laptopstore/update_order.html', context)



@login_required(login_url='login') 
@allowedusers(allowedgroup=['admin'])  
def delete(request,pk):
    order=Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'order': order}
    return render(request, 'laptopstore/delete_form.html', context)


@notlogedusers
def register(request):
    form = Createnewuser()
    if request.method == 'POST':
        form = Createnewuser(request.POST)
        if form.is_valid(): 
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECABTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            # إرسال طلب التحقق باستخدام requests
            r = requests.post("https://www.google.com/recaptcha/api/siteverify", data=data)
            result = r.json()

            if result['success']:
                user = form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, username + ' Created successfully!!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid reCAPTCHA, please try again.')

    context = {'form': form}
    return render(request, 'laptopstore/register.html', context)
  

@notlogedusers

def userlogin(request): 
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else:
              messages.info(request, "هناك خطأ ما")

        context={}
        return render(request, 'laptopstore/login.html', context)
    
def userlogout(request): 


    logout(request)
    return redirect('login')


@login_required(login_url='login') 
@allowedusers(allowedgroup=['customar']) 
def user_profile(request):
    try:
        orders = request.user.coustomer.order_set.all()
    except Coustomer.DoesNotExist:
        orders = [] 

    num_of_order = orders.count()
    num_Pending = orders.filter(status='Pending').count()
    num_Completed = orders.filter(status='Completed').count()
    num_Canceled = orders.filter(status='Canceled').count()
    num_Shipped = orders.filter(status='Shipped').count()
    num_Processing = orders.filter(status='Processing').count()

    
    context = {
        'orders': orders,
        'num_of_order': num_of_order,
        'num_Pending': num_Pending,
        'num_Completed': num_Completed,
        'num_Canceled': num_Canceled,
        'num_Shipped': num_Shipped,
        'num_Processing': num_Processing,
    } 
    return render(request, 'laptopstore/profile.html', context)




@login_required(login_url='login') 

def profile_info(request):

    coustomer = request.user.coustomer
    form= CustomerForm(instance=coustomer)
    if request.method == 'POST':
        form=CustomerForm(request.POST,request.FILES,instance=coustomer)
        if form.is_valid(): 
            form.save()


    context = {'coustomer':coustomer,
               'form':form} 
    return render(request, 'laptopstore/profile_info.html', context)

# في ملف views.py
from django.shortcuts import render, redirect
from .forms import LaptopForm
from django.contrib.auth.decorators import login_required
from .decorators import allowedusers

@login_required(login_url='login')  # تأكد من أن المستخدم مسجل دخول
@allowedusers(allowedgroup=['admin'])  # إذا كان المستخدم هو المسؤول فقط
def add_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('laptops')  # إعادة التوجيه إلى صفحة اللابتوبات
    else:
        form = LaptopForm()

    context = {'form': form}
    return render(request, 'laptopstore/add_laptop.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Laptop, Favorite



def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'laptopstore/laptop_detail.html', {'laptop': laptop})




from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Laptop, Favorite

# عرض قائمة المفضلة
@login_required
def favorite_laptops(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('laptop').order_by('-added_on')
    laptops = [favorite.laptop for favorite in favorites]
    return render(request, 'laptopstore/favorites.html', {'laptops': laptops})

# إضافة عنصر إلى المفضلة
@login_required
def add_to_favorites(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    Favorite.objects.get_or_create(user=request.user, laptop=laptop)
    return redirect('laptops')

# إزالة عنصر من المفضلة
@login_required
def remove_from_favorites(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    Favorite.objects.filter(user=request.user, laptop=laptop).delete()
    return redirect('favorite_laptops')

@login_required(login_url='login')
def add_to_invoice(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    customer = request.user.coustomer  # المستخدم الحالي
    Order.objects.create(
        Coustomer=customer,
        Laptop=laptop,
        status='Pending'  # حالة الطلب الافتراضية
    )
    return redirect('laptops')  # إعادة التوجيه إلى صفحة اللابتوبات

def delivery_information(request):
    return render(request,'laptopstore/delivery_information.html')



def about_us(request):
    return render(request, 'laptopstore/about_us.html')


@login_required
def our_team(request):
   
    # جلب كل المستخدمين الذين هم في مجموعة "admin"
    admins = User.objects.filter(groups__name='admin')
    context = {'admins': admins}
    return render(request, 'laptopstore/our_team.html', context)
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)  # الحصول على البيانات من النموذج المرسل
        if form.is_valid():  # التحقق من صحة النموذج
            email = form.cleaned_data['email']  # البريد الإلكتروني المدخل
            message = form.cleaned_data['message']  # الرسالة المدخلة
            
            send_mail(
                f"Message from {email}",  # الموضوع
                message,  # النص
                email,  # من البريد الإلكتروني المدخل
                ['ayman32819@gmail.com'],  # إرسال الرسالة إلى بريد الصفحة
                fail_silently=False,
            )
            return HttpResponse("Message sent successfully!")  # عرض رسالة تأكيد

    else:
        form = ContactForm()  # إذا كان الطلب GET، إنشاء نموذج فارغ

    return render(request, 'your_template.html', {'form': form})  # عرض النموذج في القالب

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse

def contact_us(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f"Message from {email}",
            message,
            email,  # البريد الإلكتروني من المستخدم
            ['ayman32819@gmail.com'],  # البريد الذي سيتلقى الرسالة
            fail_silently=False,
        )

        return HttpResponse("Message sent successfully!")

    return render(request, 'laptopstore/contact_us.html')  # عرض القالب الخاص بنموذج الاتصال


def cancel_order(request, order_id):
    try:
        # الحصول على الطلب من قاعدة البيانات
        order = Order.objects.get(id=order_id)
        # حذف الطلب نهائيًا
        order.delete()
    except Order.DoesNotExist:
        # إذا لم يتم العثور على الطلب، يمكن إضافة رسالة خطأ أو التعامل معها كما تشاء
        pass
    return redirect('profile')  # أو الصفحة التي تحتوي على قائمة الأوامر



from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from .decorators import forAdmin  # تأكد من أن لديك ديكوراتور للصلاحيات

@login_required
@forAdmin
def make_admin(request):
    users = User.objects.exclude(groups__name='admin')  # استبعاد الإداريين الحاليين
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        admin_group = Group.objects.get(name="admin")
        customer_group = Group.objects.get(name="customar")

        # إزالة المستخدم من مجموعة العملاء وإضافته إلى مجموعة الأدمن
        user.groups.remove(customer_group)
        user.groups.add(admin_group)
        return redirect("/make_admin")  # استبدلها بعنوان صفحة نجاح أو إعادة توجيه مناسبة

    return render(request, "laptopstore/make_admin.html", {"users": users})


@login_required
@forAdmin
def remove_admin(request):
    admins = User.objects.filter(groups__name="admin")  # جلب جميع الإداريين فقط
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(id=user_id)
        admin_group = Group.objects.get(name="admin")
        customer_group = Group.objects.get(name="customar")

        # إزالة المستخدم من مجموعة الأدمن وإعادته إلى مجموعة العملاء
        user.groups.remove(admin_group)
        user.groups.add(customer_group)
        return redirect("/remove_admin")  # استبدلها بعنوان صفحة نجاح أو إعادة توجيه مناسبة

    return render(request, "laptopstore/remove_admin.html", {"admins": admins})



from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from .models import Order, Favorite, Coustomer

from django.shortcuts import render
from laptopstore.models import Coustomer

def user_behavior_analysis(request):
    top_customers = Coustomer.objects.annotate(order_count=Count('order')).order_by('-order_count')[:10]

    # تجهيز البيانات للمخطط البياني
    customer_names = [customer.name for customer in top_customers]
    order_counts = [customer.order_set.count() for customer in top_customers]

    context = {
        'top_customers': top_customers,
        'customer_names': customer_names,
        'order_counts': order_counts,
    }

    return render(request, 'laptopstore/user_behavior_analysis.html', context)
