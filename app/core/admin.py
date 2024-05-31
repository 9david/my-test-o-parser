from django.contrib import admin
from core import models
from django.utils.translation import gettext_lazy as _
'''
Django admin customization
'''

admin.site.register(models.Product)
