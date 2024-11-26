from django.contrib import admin

# Register your models here.
from cats.models import Cat, Breed


admin.site.register(Cat)
admin.site.register(Breed)