from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#custome imports
from .models import Post
from .forms import PostForm



# Create your views here.
def posts_list(request):
    queryset_list = Post.objects.all()
    paginator = Paginator(queryset_list, 2) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
        "object_list" : queryset,
        "title":"PostsList",
        "page_request_var":page_request_var,
    }
    return render(request, "post_list.html", context)

def posts_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit= False)
        instance.save()
        messages.success(request, "Post Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title" : "Create Blog Post",
        "form":form,
    }
    return render(request,"post_form.html",context)

def posts_detail(request, id = None):
    instance = get_object_or_404(Post, id = id )
    context = {
        "title" : instance.title,
        "instance" : instance
    }
    return render(request,"post_detail.html",context)

def posts_update(request, id = None):
    instance = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None,request.FILES or None,instance = instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": instance.title,
        "instance": instance,
        "form":form,

    }
    return render(request, "post_form.html", context)
def posts_delete(request, id = None):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.success(request,"Post Deleted")
    return redirect("posts:list")