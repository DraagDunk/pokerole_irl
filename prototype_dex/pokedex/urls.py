#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:16:05 2022

@author: jellymancer
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
