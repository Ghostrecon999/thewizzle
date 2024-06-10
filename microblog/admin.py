from django.contrib import admin
from .models import Post,Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display=["body","created","tags_list","author"]
    fieldsets = (
        (None, {"fields": ("body", "active",
                "status", "image", "author")}),
    )
    def get_queryset(self,request):
        return super().get_queryset(request).prefetch_related('tags')
    
    def tags_list(self,obj):
        return u','.join(o.name for o in obj.tags.all())

admin.site.register(Comment)