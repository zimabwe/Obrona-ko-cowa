
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Wizyta(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.TextField()


class Diet(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='diet_pdfs/')
    feedback = models.OneToOneField('Feedback', on_delete=models.SET_NULL, null=True, blank=True)

class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)