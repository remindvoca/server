from django.db import models
import uuid
# from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
'''

$$$$$ 데이터베이스에 사용 시 주의사항 $$$$$ 

1. WordModel은 크롤링한 단어를 저장하는 모델

2. CardModel ~ FolderModel은 단어장을 위한 모델 - Folder 모델부터 생성해야 FK 조건을 만족하면서 생성가능.

# 3. Account 는 Custom User Model

'''

# Word Info DB
class WordModel(models.Model):
    '''
    cleanword(PK):
    meaning:
    pron:
    '''
    cleanword = models.CharField(max_length=45, primary_key=True)
    meaning = models.CharField(max_length=200)
    pron = models.FileField(upload_to='pron/')


# Voca Info DB
class CardModel(models.Model):
    '''
    id(PK):
    WordModel_cleanword(FK):
    example_text1:
    example_text2:
    DailyBookModel_id(FK):
    VocaBookModel_id(FK):
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    WordModel_cleanword = models.ForeignKey('WordModel', on_delete=models.CASCADE)
    example_text1 = models.CharField(max_length=500)
    example_text2 = models.CharField(max_length=500, null=True)
    completed = models.BooleanField(default=False)
    # DailyBookModel_id = models.UUIDField(editable=False)
    # VocaBookModel_id = models.UUIDField(editable=False)
    DailyBookModel_id = models.ForeignKey('DailyBookModel', on_delete=models.CASCADE)
    VocaBookModel_id = models.ForeignKey('VocaBookModel', on_delete=models.CASCADE)


    def getUncompletedCards(self):
        cardList = CardModel.objects.filter(completed=False)
        return cardList



class DailyBookModel(models.Model):
    '''
    id(PK)
    num_reminded:
    VocaBookModel_id(FK):
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    daily_num = models.IntegerField()
    num_reminded = models.IntegerField(default=0)
    VocaBookModel_id = models.ForeignKey('VocaBookModel', on_delete=models.CASCADE)


class VocaBookModel(models.Model):
    '''
    id:
    num_expected_day:
    FolderModel_id(FK):
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bookname = models.CharField(max_length=100, default='RemindVoca Foler')
    num_expected_day = models.IntegerField()
    FolderModel_id = models.ForeignKey('FolderModel', on_delete=models.CASCADE)


class FolderModel(models.Model):
    '''
    id:
    Account_userID(FK):
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    foldername = models.CharField(max_length=100, default='RemindVoca Foler')
    Account_userID = models.ForeignKey('accounts.User', on_delete=models.CASCADE)


class PDFModel(models.Model):
    '''
    filePath:
    Account_userID(FK):
    '''
    filePath = models.FileField(upload_to="")
    Account_userID = models.ForeignKey('accounts.User', on_delete=models.CASCADE)


#
#
# class AccountManager(BaseUserManager):
#     '''
#     커스텀 유저 모델(Custom User Model)를 만들기 위해서는
#     두 클래스(BaseUserManager, AbstractBaseUser)를 구현해야 합니다.
#     BaseUserManager 클래스는 유저를 생성할 때 사용하는 헬퍼(Helper) 클래스이며,
#     실제 모델(Model)은 AbstractBaseUser을 상속받아 생성하는 클래스입니다.
#
#     헬퍼(Helper) 클래스인 class UserManager(BaseUserManager):는 두 가지 함수를 가지고 있습니다.
#
#     create_user(*username_field*, password=None, **other_fields)
#     create_superuser(*username_field*, password, **other_fields)
#
#     여기서 알 수 있듯이 첫번째 파라메터가 username 파라메터입니다.
#     우리는 username 대신 email을 사용할 예정이므로 이 파라메터에 username이 아닌 email을 전달합니다.
#     나머지 부분은 데이터를 생성하는 부분이므로 자세한 설명은 생략하도록 하겠습니다.
#     '''
#
#     # 일반 유저 생성
#     def create_user(self, userID, email, name, date_of_birth, password=None):
#         if not userID or not email or not name or not date_of_birth:
#             raise ValueError('Users must input all information we provide')
#
#         account = self.model(
#             userID=userID,
#             email=self.normalize_email(email),
#             name=name,
#             date_of_birth=date_of_birth,
#         )
#
#         account.set_password(password)
#         account.save(using=self._db)
#         return account
#
#     # 관리자 생성
#     def create_superuser(self, userID, email, name, date_of_birth, password):
#         account = self.create_user(
#             userID=userID,
#             email=email,
#             name=name,
#             password=password,
#             date_of_birth=date_of_birth,
#         )
#         account.is_admin = True
#         account.save(using=self._db)
#         return account
#
#
# class Account(AbstractBaseUser):
#     '''
#     이 모델은 email, date_of_birth, is_active, is_admin 필드를 가지고 있습니다.
#     is_active, is_admin 필드는 장고(django)의 유저 모델(User Model)의 필수 필드입니다.
#     '''
#     userID = models.CharField(primary_key=True, max_length=45)
#     email = models.EmailField(
#         verbose_name='email',
#         max_length=255,
#         unique=True,
#     )
#     name = models.CharField(max_length=45)
#     date_of_birth = models.DateField()
#     num_accumulated_words = models.IntegerField(default=0)
#     num_ongoing_words = models.IntegerField(default=0)
#
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#
#
#     '''
#     User 모델을 생성하기 위해 꼭 필요한 부분입니다.
#     우리가 만든 헬퍼 클래스를 사용하도록 설정하였으며(objects = UserManage()),
#     username 필드를 email로 사용하도록 설정하였습니다.(USERNAME_FIELD = 'email')
#     '''
#     objects = AccountManager()
#
#     USERNAME_FIELD = 'userID'
#     REQUIRED_FIELDS = ['email', 'name', 'date_of_birth']
#
#
#
#
#     '''
#     커스텀 유저 모델(Custom User Model)을 기본 유저 모델(Model)로 사용하기 위해서 구현 해야하는 부분입니다.
#
#     def has_perm(self, perm, obj=None):: True를 반환하여 권한이 있음을 알립니다. Ojbect를 반환하는 경우 해당 Object로 사용 권한을 확인하는 절차가 필요합니다.
#     def has_module_perms(self, app_label):: True를 반환하여 주어진 앱(App)의 모델(Model)에 접근 가능하도록 합니다.
#     def is_staff(self):: True가 반환되면 장고(django)의 관리자 화면에 로그인 할 수 있습니다.
#     '''
#
#     # 이름을 리턴하기로 함
#     def __str__(self):
#         return self.name
#
#     def has_perm(self, perm, obj=None):
#         return True
#
#     def has_module_perms(self, app_label):
#         return True
#
#     @property
#     def is_staff(self):
#         return self.is_admin


