from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.
def register(response):
    form=UserCreationForm()
    return render(response,'register/register.html',{'form':form})
    

def loginPage(request):
    if(request.method=="POST"):
        username=request.POST.get('username')
        password=request.POST.get('password')
        remember_me=request.POST.get('remember_me')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            print(remember_me)
            if(remember_me): 
                response=redirect('home')
                response.set_cookie("cid",username)
                response.set_cookie("cid2",password)
                return response
            return redirect('home')
        else:
            messages.info(request,"Username OR Password is incorrect")
    print(request.COOKIES.get("cid"))
    context={}
    if(request.COOKIES.get('cid')):
        context={'cookie1':request.COOKIES.get('cid'),'cookie2':request.COOKIES.get('cid2')}
    return render(request,'registration/login.html',context)
    
        #remember_me = form.cleaned_data['remember_me']
        #login(self.request, form.get_user())
        #if remember_me:
         #   self.request.session.set_expiry(1209600)
        #return super(LoginView, self).form_valid(form)
