from django.shortcuts import redirect


from django.shortcuts import redirect

def notlogedusers(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


from django.shortcuts import redirect

def allowedusers(allowedgroup=[]):
    def decorators(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            # استخدم exists() بدلاً من is_exists()
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  
            if group in allowedgroup:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('profile/')
        return wrapper_func 
    return decorators

def forAdmin(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            # استخدم exists() بدلاً من is_exists()
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name  
            if group =='admin':
                return view_func(request, *args, **kwargs)
            if group == 'customar':
                return redirect('profile/')
        return wrapper_func 

