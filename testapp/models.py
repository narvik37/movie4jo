from django.db import models

# Create your models here.


class Test(models.Model):
    id = models.CharField(max_length=16, verbose_name="id", primary_key=True)
    title = models.CharField(max_length=16, verbose_name="title")
    plot = models.CharField(max_length=512, verbose_name="plot")
    path = models.CharField(max_length=128, verbose_name="path")
    date = models.CharField(max_length=16, verbose_name="date")
    rating = models.CharField(max_length=8, verbose_name="rating", default='')
    

    created = models.DateTimeField(auto_now_add=True, verbose_name="register_time")
    update = models.DateTimeField(auto_now_add=True, verbose_name="modify_time")

    class Meta:
        db_table = "test"
        verbose_name = "Test"
        verbose_name_plural = "Test"
        
    def __str__(self):
        return self.title