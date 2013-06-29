# Create your views here.

from django.http import Http404,HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from blog.models import *
import datetime

def signin(request):
	try:
		user = User.objects.get(username=request.POST['username'])
		if user.check_password(request.POST['password']):
			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request,user)
	except User.DoesNotExist:
		user = None
	return redirect('index')

def signout(request):
	logout(request)
	return redirect('index')

def index(request):
	if request.user.is_authenticated():
		blogs=Blog.objects.order_by('-views')
		form = PostForm()
		return render(request,'blog/index.html', {
			'blogs': blogs
			})
	else:
		form = UserForm()
		return render(request, 'index/login.html', {'form': form})

def create_blog(request):
	if request.user.is_authenticated() and not Blog.objects.filter(owner=request.user):
		blog = Blog.objects.create(owner=request.user)
		return redirect('view_blog', blog_id=blog.id)
	else:
		return HttpResponse("<a href='/logout/'>logout</a> <a href='/'>Home</a><h2>You already have a blog and you're only allowed one ... <h2>")
		
def view_blog(request, blog_id):
	try:
		blog=Blog.objects.get(id=blog_id)
		posts=Post.objects.filter(blog=blog)
		if request.user.is_authenticated():
			try:
				view = BlogView.objects.get(viewer=request.user, blog=blog)
			except BlogView.DoesNotExist:
				BlogView.objects.create(viewer=request.user, blog=blog)
				blog.views_count()
			if request.user == blog.owner:
				form = PostForm()
			else:
				form=None
			if Follow.objects.filter(follower=request.user, following=blog.owner):
				follow=True
			else: 
				follow=False
		else: 
			form=None
			form=None
	except Blog.DoesNotExist:
		raise Http404
	except Post.DoesNotExist:
		posts=None
	return render(request,'blog/view.html', {
			'posts': posts,
			'blog': blog,
			'form': form,
			'follow':follow
		})

def edit_blog(request, blog_id):
	try:
		blog =Blog.objects.get(id=blog_id)
		if not request.user.is_authenticated() or request.user != blog.owner:
			raise PermissionDenied
		form = BlogForm(instance=blog)
	except Blog.DoesNotExist:
		raise Http404
	return render(request, 'post/edit.html', {
		'blog_id': post_id,
		'form': form
		})

def delete_blog(request, blog_id):
	try:
		blog = Blog.objects.get(id=blog_id)
		if not request.user.is_authenticated() or request.user != blog.owner:
			raise PermissionDenied
		else:
			blog.delete()
	except Blog.DoesNotExist:
		blog = None
	return redirect('index')

def create_post(request, blog_id):
	try:
		blog = Blog.objects.get(id=blog_id)
		now = datetime.datetime.now()
		if not request.user.is_authenticated():
			raise PermissionDenied
		post = Post.objects.create(blog=blog, title=request.POST['title'], text=request.POST['text'], pub_date=now)
	except Blog.DoesNotExist:
		raise Http404
	return redirect('view_post', post_id=post.id)

def view_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		comments = Comment.objects.filter(post=post)
		if request.user.is_authenticated():
			form = CommentForm()
		else:
			form = None
	except Post.DoesNotExist:
		raise Http404
	return render(request, 'post/view.html', {
		'post': post, 
		'comments': comments, 
		'form': form
		})

def edit_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		if not request.user.is_authenticated():
			raise PermissionDenied
		form = PostForm(instance=post)
	except Post.DoesNotExist:
		raise Http404
	context = {}
	return render(request, 'post/edit.html',{
	 'post_id': post_id, 
	 'form': form
	 })

def update_post(request, post_id):
	try:
		posts = Post.objects.filter(id=post_id)
		if not request.user.is_authenticated():
			raise PermissionDenied
		posts.update(title=request.POST['title'], text=request.POST['text'])
	except Post.DoesNotExist:
		raise Http404
	return redirect('view_post', post_id=post_id)

def delete_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		blog = post.blog.id
		if not request.user.is_authenticated():
			raise PermissionDenied
		post.delete()
	except Post.DoesNotExist:
		raise Http404
	return redirect('view_blog', blog_id=post.blog.id)

def add_comment(request, post_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		post=Post.objects.get(id=post_id)
	except Post.DoesNotExist:
		raise Http404
	now = datetime.datetime.now()
	Comment.objects.create(user=request.user, post=post, comment=request.POST['comment'],comm_date=now)
	return redirect('view_post', post_id=post_id)

def follow(request, blog_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		Follow.objects.create(follower=request.user, following=Blog.objects.get(id=blog_id).owner)
	except Blog.DoesNotExist:
		raise Http404
	return redirect('view_blog', blog_id=blog_id)

def unfollow(request, blog_id):
	if not request.user.is_authenticated():
		raise PermissionDenied
	try:
		Follow.objects.get(follower=request.user, followed=Blog.objects.get(id=blog_id).user).delete()
	except:
		raise Http404
	return redirect('view_blog', blog_id=blog_id)	