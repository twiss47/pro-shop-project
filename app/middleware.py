import time
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout  
from django.urls import resolve 


#---------- User Ip Logger -----------
class IpLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    
    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        print('user ip :', ip)
        return self.get_response(request)
    



#---------- Login Required-----------

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_names = ['login', 'register']

    def __call__(self, request):
        # request.user bo‘sh bo‘lishi mumkin emas, AuthenticationMiddleware dan keyin ishlashi kerak
        if not hasattr(request, 'user'):
            return self.get_response(request)

        resolved = resolve(request.path_info)
        url_name = resolved.url_name

        if url_name in self.exempt_names:
            return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('login')

        return self.get_response(request)
    

#---------- Logout -----------

class LogoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.timeout = 120
    
    def __call__(self, request):
        if request.user.is_authenticated:
            current_time = time.time()
            last_activity = request.session.get('last_activity')
            
            if last_activity:
                elapsed = current_time - last_activity


                if elapsed > self.timeout:
                    logout(request)
                    request.session.flush()

        
            request.session['last_activity'] = current_time

        return self.get_response(request)
