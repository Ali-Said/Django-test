from django.conf.urls import patterns, include, url
from blog import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.create_blog, name='create_blog'),
	url(r'^(?P<blog_id>\d+)/$', views.view_blog, name='view_blog'),
	url(r'^(?P<blog_id>\d+)/edit/$', views.edit_blog, name='edit_blog'),
    url(r'^(?P<blog_id>\d+)/delete/$', views.delete_blog, name='delete_blog'),
    
    url(r'^(?P<blog_id>\d+)/post/create/$', views.create_post, name='create_post'),
	url(r'^post/(?P<post_id>\d+)/$', views.view_post, name='view_post'),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
    url(r'^post/(?P<post_id>\d+)/update/$', views.update_post, name='update_post'),
    url(r'^post/(?P<post_id>\d+)/delete/$', views.delete_post, name='delete_post'),
    
    url(r'^(?P<blog_id>\d+)/follow/$', views.follow, name='follow'),
    url(r'^(?P<blog_id>\d+)/unfollow/$', views.unfollow, name='unfollow'),

    url(r'^login/$', views.signin, name='login'),
	url(r'^logout/$', views.signout, name='logout'),

    url(r'^post/(?P<post_id>\d+)/comment/add/$', views.add_comment, name='add_comment'),

    url(r'^admin/', include(admin.site.urls))
)