from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User

class StreamingPlatforms(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField(max_length=150)
    website_link = models.URLField(max_length=200)

    def __str__(self):
        return self.name   


# Create your models here.
class Movies(models.Model):
    # id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    platform = models.ForeignKey(StreamingPlatforms, on_delete=models.CASCADE,blank=True,default=None, null=True,related_name='Movies')
    active = models.BooleanField(default=False)
    avg_review = models.FloatField(default=0)
    no_of_reviews = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
 

class Reviews(models.Model):
    review_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])
    movies = models.ForeignKey(Movies, on_delete=models.CASCADE,related_name="movies")
    active = models.BooleanField(default=True)
    description = models.CharField(max_length=200,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.ratings) + "| Stars on " + self.movies.title

