from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Track(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)   #blank=True allows for description to be null
    url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)

# By using on_delete=models.CASCADE, if a User that created a Track is deleted, then the Track is also deleted!

class Like(models.Model):
    user = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    track = models.ForeignKey('tracks.Track', related_name='likes', on_delete=models.CASCADE)

#If add a new class must run makemigrations and migrate*************************************

# {
#   likes {
#     user {
#       username
#     }
#     track {
#       title
#     }
#   }
# }





