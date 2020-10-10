import uuid

from django.db import models
from book.utils import sendTransaction
import hashlib

# Create your models here.


class Room(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    hotelName = models.CharField(max_length=30, default='Hotel')
    location = models.CharField(max_length=30, default='')
    people = models.IntegerField(default=None)
    pricePerNight = models.FloatField(default=None)
    averageRatings = models.FloatField(default=None)
    stars = models.FloatField(default=None)
    booked = models.BooleanField(default=False)
    days = models.IntegerField(blank=True, default=1)
    whoBooked = models.CharField(max_length=30, default='', blank=True)

    # function to validate bookings on blockchain
    def writeOnChain(self):
        self.hash = hashlib.sha256(self.content.encode('utf-8')).hexdigest()
        self.txId = sendTransaction(self.hash)
        self.save()


# model for the home page form
class Holiday(models.Model):
    startDate = models.DateField()
    endDate = models.DateField()
    city = models.CharField(max_length=30, default='', blank=True)




