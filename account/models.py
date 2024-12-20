from django.db import models
import pytz
from django.utils.timezone import now

class AppUsers(models.Model):
    username = models.CharField(max_length=64, verbose_name='아이디')
    user_group = models.CharField(max_length=64, verbose_name='사용자 그룹')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    email = models.EmailField(max_length=64, verbose_name='이메일')
    appid = models.CharField(max_length=255, verbose_name='앱 ID')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')

    class Meta:
        db_table = 'app_users'
        ordering = ['-registered_at']
        verbose_name = '사용자'
        verbose_name_plural = '사용자'

    def __str__(self):
        return self.username
    
    def get_appid_list(self):
        return self.appid.split(',')
    
    def set_appid_list(self, appid_list):
        self.appid = ','.join(appid_list)

    appid_list = property(get_appid_list, set_appid_list)

class UserGroup(models.Model):
    user_group_id = models.CharField(max_length=64, verbose_name='사용자 그룹 아이디')
    user_group = models.CharField(max_length=64, verbose_name='사용자 그룹')
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name='가입일자')

    class Meta:
        db_table = 'user_group'
        ordering = ['-registered_at']
        verbose_name = '사용자 그룹'
        verbose_name_plural = '사용자 그룹'

    def __str__(self):
        return self.username

class UserLog(models.Model):
    username = models.ForeignKey("AppUsers", on_delete=models.CASCADE, db_column="username", verbose_name='아이디')
    visitcount = models.IntegerField(null=True, verbose_name='방문횟수')                  # 방문횟수
    login_at = models.CharField(max_length=50, verbose_name='로그인 일시')  # Store as string
    logout_at = models.CharField(max_length=50, verbose_name='로그아웃 일시')  # Store as string
    
    class Meta:
        db_table = 'userlog'
       
    