from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=30)

    # 길이가 지정되지 않는 경우에 사용
    content = models.TextField()

    # 게시글 생성시간이 자동으로 입력
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 숫자필드
    # num_stars = models.IntegerField()