from django.contrib import admin
from .models.teacher import Teacher
from .models.samplepaper import Samplepaper
from .models.generatedpaper import GeneratedPaper
# Register your models here.

admin.site.register(Teacher)
admin.site.register(Samplepaper)
admin.site.register(GeneratedPaper)