from django.shortcuts import render,redirect
from .forms import SignupForm,LoginForm,PostForm
from .models import Post
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group


def Home(request):
    posts = Post.objects.all()
    return render(request,'home.html',{'posts':posts})

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')

def addPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False) 
                post.user = Post(request.POST) 
                post.save() 
                return redirect('dashboard')  
        else:
            form = PostForm() 
        return render(request, 'addpost.html', {'form': form})
    else:
        return redirect('login') 
    
def update_post(request,id):
    if request.user.is_authenticated :
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            fm = PostForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
            return redirect('dashboard')
        else:
            pi = Post.objects.get(pk=id)
            fm = PostForm(instance=pi)
        return render(request,'updatepost.html',{'form':fm})
    else :
        return render(request,'login.html')
    
def delete_post(request,id):
    if request.user.is_authenticated :
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return redirect('dashboard')
    else :
        return render(request,'login.html')

def Dashboard(request):
    if request.user.is_authenticated :
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request,'dashboard.html',{'posts': posts,'full_name': full_name,'gps':gps})
    else:
        return render(request,'login.html')

def Login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request,data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=uname, password=password)
                if user is not None:
                    login(request,user)
                return redirect('dashboard')
        else:
            form = LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        return redirect('dashboard')

def SignUp(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            group, created = Group.objects.get_or_create(name='Author')
            user.groups.add(group)
            
            return redirect('login')
    else:
        form = SignupForm()
    
    return render(request, 'signup.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('home')

