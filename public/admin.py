from django.contrib import admin
from .models import Public,User,Compliant,Police,Criminal,UnidentifiedBodies,MissingPerson

# Register your models here.
admin.site.register(Public)
admin.site.register(User)
admin.site.register(Compliant)
admin.site.register(Police)
admin.site.register(Criminal)
admin.site.register(UnidentifiedBodies)
admin.site.register(MissingPerson)