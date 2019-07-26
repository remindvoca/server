from django.db import models
import uuid

# Create your models here.


# Word Info DB
class WordModel(models.Model):
    cleanword = models.CharField(max_length=45, primary_key=True)
    meaning = models.CharField(max_length=200)
    pron = models.FileField(upload_to='pron/')



# Voca Info DB
class CardModel(models.Model):
    WordModel_cleanword = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    example_text1 = models.CharField(max_length=500)
    example_text2 = models.CharField(max_length=500, null=True)
    DailyBookModel_id = models.UUIDField(editable=False)
    VocaBookModel_id = models.UUIDField(editable=False)

class DailyBookModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_reminded = models.IntegerField(default=0)
    VocaBookModel_id = models.UUIDField(editable=False)

class VocaBookModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    num_expected_day = models.IntegerField()
    FolderModel_id = models.UUIDField(editable=False)

class FolderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Account_userID = models.CharField(max_length=45)




# user DB
class Account(models.Model):
    userID = models.CharField(primary_key=True, max_length=45)
    userPW = models.CharField(max_length=200)
    email = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    birthday = models.DateField()
    num_accumulated_words = models.IntegerField(default=0)
    num_ongoing_words = models.IntegerField(default=0)

