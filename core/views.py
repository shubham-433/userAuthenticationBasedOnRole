from django.shortcuts import render,HttpResponseRedirect,redirect
from django.views import View
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
# Create your views here.
def home(request):
    return render(request,'index.html')

def UserLogin(request):
    # print(request.user.is_authenticated)
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm=LoginForm(request=request,data=request.POST)
            print(fm.is_valid())
            if fm.is_valid():
                uname=fm.cleaned_data["username"]
                upass=fm.cleaned_data["password"]
                print(uname,upass)
                user=authenticate(request=request,username=uname,password=upass)
                # print(user)
                if user is not None:
                    login(request,user)
                    # messages.success(request,f"Congratulation {uname} login succesfully ")
                    return HttpResponseRedirect('/accounts/profile/')
            else:
                messages.warning(request,"Invallid Credientials")
                return HttpResponseRedirect('/accounts/login/')
        else:
            fm=LoginForm()
            return render(request,'account/login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/accounts/profile/')


# for logout 
def UserLogout(request):
    logout(request) 
    messages.success(request,f"logout succesfully")
    return HttpResponseRedirect('/accounts/login') 
    
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            form=RegistrationForm()
            return render(request,"account/register.html",{"form":form})
        else:
            return HttpResponseRedirect('/accounts/profile')
             
    def post(self, request, *args, **kwargs):
        try:
            print('post')
            print(request.POST)
            image = request.FILES.get('profilePic')
            # print(image)
            form=RegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                obj=form.save()
                obj.profilePic=form.cleaned_data['profilePic']
                obj.save()

                messages.success(request, "Congratulations! Registration Successful!")
                return HttpResponseRedirect('/accounts/login')
            return  render(request,"account/register.html",{"form":form})
        except Exception as e:
            print("error")
    


class ProfileView(View):
    @method_decorator(login_required)
    def get(self,request):
       print(request.user)
       if request.user.is_doctor:
            return render(request,"doctorDashboard.html",{'user':request.user})
       else:
           return render(request,"patientDashboard.html",{'user':request.user})
    

