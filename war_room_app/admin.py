from django.contrib import admin

# Register your models here.
from .models import War,Comment,Base,Dib,Member,Clan

admin.site.register(Clan)
admin.site.register(War)
admin.site.register(Comment)
admin.site.register(Base)
admin.site.register(Dib)
admin.site.register(Member)