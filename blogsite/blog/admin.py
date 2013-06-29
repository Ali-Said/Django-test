from django.contrib import admin
from blog.models import Blog, Post, Comment, Follow

admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Follow)

class BlogAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super(MyModelAdmin, self).save_model(request, obj, form, change)
    def queryset(self, request):
        qs = super(MyModelAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)
