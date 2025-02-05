from django.db import models
from django.urls import reverse
from django.conf import settings





# class Contact(models.Model):
#     last_name = models.CharField(max_length=60)
#     first_name = models.CharField(max_length=60)
#     phone = models.CharField(max_length=14)
#     email = models.EmailField()
#     company = models.CharField(max_length=120, blank=True, null=True)
#     subject = models.CharField(max_length=120)
#     message = models.TextField()
#     updated = models.DateTimeField(auto_now=True, auto_now_add=False)
#     timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

#     # objects = ContactManager()

#     class Meta:
#         ordering = ["-timestamp", "last_name"]
#         verbose_name = "Contact"
#         verbose_name_plural = "Contacts"

#     def __str__(self):
#         return "%s - %s" %(self.last_name, self.first_name)

#     def get_absolute_url(self):
#         return reverse("contact:detail", kwargs={"pk": self.pk})






class HelpCenter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subject = models.CharField(max_length=120)
    message = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    # objects = ContactManager()

    class Meta:
        ordering = ["-timestamp",]
        verbose_name = "Help Center"
        verbose_name_plural = "Help Center"

    def __str__(self):
        return "%s - %s" %(self.user, self.subject)

    def get_absolute_url(self):
        return reverse("contact:detail", kwargs={"pk": self.pk})
