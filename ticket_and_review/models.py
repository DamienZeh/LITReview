from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models
from PIL import Image as Picture


class Ticket(models.Model):
    """Model for ticket"""

    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(
        max_length=2048, verbose_name="Description", blank=True
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(
        null=True, blank=True, verbose_name="image", upload_to="./"
    )
    time_created = models.DateTimeField(auto_now_add=True)
    review_existing = models.BooleanField(default=False)
    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        """
        resize image and save
        """
        image = Picture.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        """
        override save() with if image exist
        """
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()
        else:
            self.image = None

    def __str__(self):
        """
        get title for show it, in admin pages
        """
        return self.title


class Review(models.Model):
    """Model for Review"""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class AutoReview(models.Model):
    """Model for autoreview (ticket + review)"""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, verbose_name="Titre")
    description = models.TextField(
        max_length=5000, verbose_name="Description", blank=True
    )
    image = models.ImageField(
        null=True, blank=True, verbose_name="image", upload_to="./"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
    IMAGE_MAX_SIZE = (200, 200)

    def resize_image(self):
        """
        resize image and save
        """
        image = Picture.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            self.resize_image()
        else:
            self.image = None

    def __str__(self):
        """
        get title for admin pages
        """
        return self.title


class UserFollows(models.Model):
    """Model for user and followed user"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        """
        Meta for UserFollows. unique_together = ('user', 'followed_user', )
        """

        unique_together = (
            "user",
            "followed_user",
        )
