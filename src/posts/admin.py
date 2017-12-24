from django.contrib import admin

# Register your models here.

from .models import post



class PostModelAdmin(admin.ModelAdmin):
	list_display=("title","update","timestamp")
	list_display_links=("update","timestamp")
	list_filter=("update","timestamp")
	search_fields=["title","content"]
	class Meta:
		model=post


admin.site.register(post,PostModelAdmin)
