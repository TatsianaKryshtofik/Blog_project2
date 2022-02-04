from django.contrib import admin

from .models import *

admin.site.register(User)
admin.site.register(UserInfo)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(PostRating)
admin.site.register(Image)
