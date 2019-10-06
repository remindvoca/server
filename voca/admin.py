from django.contrib import admin
from voca.models import Word, WordDay, WordBook

# Register your models here.


@admin.register(WordBook)
class WordBookAdmin(admin.ModelAdmin):
    pass


@admin.register(WordDay)
class WordDayAdmin(admin.ModelAdmin):
    pass


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    pass
