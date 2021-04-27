from django.shortcuts import render, redirect, HttpResponse, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .form import *
from django.core.mail import EmailMessage
from django.template.loader import get_template

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class BlogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Blog.objects.all().order_by('-Date')
    serializer_class = BlogSerializer

# home blog view
def BlogViews(request):
    posts = Blog.objects.all()
    return render(request, 'blog/index.html', { 'post': posts })

# redirect success page
def Success(request):
    return render(request, 'blog/success.html')

# blog post detail view
def BlogDetail(request, slug):
    post = get_object_or_404(Blog, Slug = slug)
    comments = post.comments.filter(Active=True, Parent__isnull=True)
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid:
            Parent_obj = None
            try:
                Parent_id = int(request.POST.get('Parent_id'))
            except:
                Parent_id = None
            if Parent_id:
                Parent_obj = Comment.objects.get(id=Parent_id)
                if Parent_obj:
                    reply_comment = comment_form.save(commit=False)
                    reply_comment.Parent = Parent_obj
            new_comment = comment_form.save(commit=False)
            new_comment.Post = post
            new_comment.save()
            return redirect('blog:detail', slug)
    else:
        comment_form = CommentForm()

    return render(request, 'blog/blogdetail.html', {'blog':post, 'comments':comments, 'comment_form':comment_form})


# sign up form
def SignUp(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('blog:success')
    else:
        form = UserRegisterForm()
    return render(request, "registration/signup.html", {'form': form})


# Contact form view

def Contact(request):
    Contact_Form = ContactForm
    if request.method == 'POST':
        form = Contact_Form(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_content = request.POST.get('content')

            template = get_template('blog/contact_form.txt')
            context = {
                'contact_name' : contact_name,
                'contact_email' : contact_email,
                'contact_content' : contact_content,
            }
            
            content = template.render(context)

            email = EmailMessage(
                "New contact form email",
                content,
                "Creative web" + '',
                ['myfriendkhendelwal@gmail.com'],
                headers = { 'Reply To': contact_email }
            )

            email.send()

            return redirect('blog:success')
    return render(request, 'blog/contact.html', {'form':Contact_Form })