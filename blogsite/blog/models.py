from django.db import models
from django import forms
from django.contrib.auth.models import User

class Blog(models.Model):
	owner = models.ForeignKey(User)
	views = models.IntegerField(default=0)

	def views_count(self):
		self.views +=1
		self.save()

class BlogView(models.Model):
	viewer = models.ForeignKey(User)
	blog = models.ForeignKey(Blog)

class Post(models.Model):
	blog = models.ForeignKey(Blog)
	title = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')
	text = models.TextField()

class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		exclude = ('blog', 'pub_date')

class Comment(models.Model):
	post = models.ForeignKey(Post)
	user = models.ForeignKey(User)
	comment = models.CharField(max_length=200)
	comm_date = models.DateTimeField('date commented')
	
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('post', 'user', 'comm_date')

class Follow(models.Model):
	follower = models.ForeignKey(User, related_name='follower')
	following = models.ForeignKey(User, related_name='following')

	class Meta:
		unique_together = ('follower','following')

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']		