from django.db import models

from account.models import UserProfile

class Testimonial(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.user.email
