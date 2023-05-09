from django.db import models

from account.models import UserProfile

class Testimonial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.full_name
