from django.shortcuts import render,HttpResponseRedirect,get_object_or_404,redirect
from django.views import View
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.mail import send_mail
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
            posts= Post.objects.filter(author=request.user.id) 
            # draftPost= Post.objects.filter(Q(author=request.user.id) & Q(status='DF'))
            context={
                
                'posts':posts,
                'user':request.user

            }
            print(posts)
            return render(request,"doctorDashboard.html",context)
       else:
           return render(request,"patientDashboard.html",{'user':request.user})
    

# to add blog

def addBlog(request):
    context={'form':AddBlogForm}
    print()
    if request.user.is_authenticated :
        if  request.user.is_doctor:
            try:
                if request.method=='POST':
                    form=AddBlogForm(request.POST,request.FILES)
                    image=request.FILES.get('image')
                    title=request.POST.get('title')
                    body=request.POST.get('body')
                    print(title,body,image)
                    if form.is_valid():
                        body=form.cleaned_data['body']
                        obj=form.save(commit=False)
                        obj.author=request.user
                        obj.image=image
                        obj.save()
                        form.save_m2m()
                        print("created")
                        messages.success(request, "Post Created  Successful!")
                        return render(request,'addBlog.html',context)
                    else:
                        print(form.errors)
                        messages.success(request, "some error occure")
                        return render(request,'addBlog.html',context)
                else:
                     return render(request,'addBlog.html',context)
            except Exception as e:
                print(e)
                return HttpResponseRedirect('/accounts/login')
        else:
             return HttpResponseRedirect('/accounts/login/')
        
    else:  
        # return render(request,'addBlog.html',context)
        return HttpResponseRedirect('/accounts/login/')

# to see all post 
def post_categories(request,slug):
    categories = Category.objects.filter(slug=slug)
    print(categories)
    return render(request, 'allBlogs.html', {'categories': categories})


def post_list(request):
    # category = Category.objects.get(id=id)
    posts_list=Post.published.all()
    return render(request,'allBlogs.html',{"posts":posts_list})

def post_categories(request , id):
    category = Category.objects.get(id=id)
    posts_list=Post.published.filter(category = category)
    return render(request,'allBlogs.html',{"posts":posts_list,'categories':posts_list})

# for post detail 

def post_details(request,year,month,day,post):
    print("hi")
    try:
        post=get_object_or_404(Post,status=Post.Status.PUBLISHED,slug=post,publish__year=year,publish__month=month,publish__day=day)
        print(post)
        return render(request,'postDetail.html',{'post':post})
    except:
        print("An exception occurred")
        return HttpResponseRedirect('/blog')
    


# share post 
def post_share(request,post_id):
    post=get_object_or_404(Post,id=post_id, status=Post.Status.PUBLISHED)
    sent=False
    # return render(request,'share.html')
    if request.method == 'POST':
        form=EmailPostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject=f"{request.user} recommends  you read " f"{post.title}"
            message=f"Read {post.title} at {post_url} \n\n"f"{request.user}\'s comments : {cd['comments']}"
            send_mail(subject,message,'shubhamvr33@gmail.com',[cd['to']])
            sent=True
            print(subject)
            return render(request,'share.html',{'post':post,'form':form,'sent':sent})

    else:
        form=EmailPostForm()
        return render(request,'share.html',{'post':post,'form':form,'sent':sent})