# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    # The home page
    path('', views.index, name='home')

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
