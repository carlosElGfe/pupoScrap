# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User


class producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(default="no name",max_length=400,unique=True)
    medida = models.CharField(default="sin medida",max_length=400)
    precio = models.CharField(default="sin precio",max_length=400)
    class Meta:
        managed = True
        db_table = "producto"
        verbose_name_plural = "productos"
        indexes = [
            models.Index(
                fields=[
                    "id_producto",
                ]
            ),
        ]
    
    def __str__(self):
        return f"datos producto"
# Create your models here.

