# Generated by Django 3.0.3 on 2024-12-02 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, verbose_name='아이디')),
                ('user_group', models.CharField(max_length=64, verbose_name='사용자 그룹')),
                ('password', models.CharField(max_length=64, verbose_name='비밀번호')),
                ('email', models.EmailField(max_length=64, verbose_name='이메일')),
                ('appid', models.CharField(max_length=255, verbose_name='앱 ID')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일자')),
            ],
            options={
                'verbose_name': '사용자',
                'verbose_name_plural': '사용자',
                'db_table': 'user',
                'ordering': ['-registered_at'],
            },
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_group_id', models.CharField(max_length=64, verbose_name='사용자 그룹 아이디')),
                ('user_group', models.CharField(max_length=64, verbose_name='사용자 그룹')),
                ('registered_at', models.DateTimeField(auto_now_add=True, verbose_name='가입일자')),
            ],
            options={
                'verbose_name': '사용자 그룹',
                'verbose_name_plural': '사용자 그룹',
                'db_table': 'user_group',
                'ordering': ['-registered_at'],
            },
        ),
        migrations.CreateModel(
            name='UserLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitcount', models.IntegerField(null=True, verbose_name='방문횟수')),
                ('login_at', models.DateTimeField(auto_now=True, verbose_name='로그인 일시')),
                ('logout_at', models.DateTimeField(auto_now=True, verbose_name='로그아웃 일시')),
                ('username', models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to='account.User', verbose_name='아이디')),
            ],
            options={
                'db_table': 'userlog',
            },
        ),
    ]