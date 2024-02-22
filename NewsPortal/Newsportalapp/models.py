from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce


class Author(models.Model):
    name_author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        a_t_post_rating = Post.objects.filter(post_author_id=self, post_type='ART').aggregate(total_in_p = Coalesce(Sum('post_rating'), 0))['total_in_p']
        a_t_comm_rating = Comment.objects.filter(user_id=self.name_author).aggregate(total_in_с = Coalesce(Sum('comm_rating'), 0))['total_in_с']
        all_comm_rating = Comment.objects.filter(post__post_author=self).aggregate(total_in_ac= Coalesce(Sum('comm_rating'), 0))['total_in_ac']
        self.author_rating = a_t_post_rating * 3 + a_t_comm_rating + all_comm_rating
        print(f"Общий:[{self.author_rating}]! За статьи:[{a_t_post_rating * 3}], комментарии автора:[{a_t_comm_rating}], комментарии пользователей:[{all_comm_rating}]")
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    news_post = 'NEWS'
    article_post = 'ART'
    other = 'OTH'

    TYPEPOST = [
        (news_post,'Новость'),
        (article_post,'Статья'),
        (other, 'Другое')
    ]

    post_type = models.CharField(max_length=4, choices=TYPEPOST, default=other)
    post_add = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def __str__(self):
        return self.post_name

    def like(self):
        self.post_rating += 1
        self.save()
        print(f"Рейтинг поста автора:{self.post_author} повысился! ({self.post_rating})")

    def dislike(self):
        self.post_rating -= 1
        self.save()
        print(f"Рейтинг поста автора:{self.post_author} понизился! ({self.post_rating})")

    def preview(self):
        post_text_preview = self.post_text[0:124]
        if len(self.post_text) > 124:
            post_text_preview = f"{self.post_text[0:121:]}..."
        return post_text_preview

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    comm_add = models.DateTimeField(auto_now_add=True)
    comm_text = models.TextField()
    comm_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comm_text

    def like(self):
        self.comm_rating += 1
        self.save()
        print(f"Рейтинг комментария:{self.user} повысился! ({self.comm_rating})")

    def dislike(self):
        self.comm_rating -= 1
        self.save()
        print(f"Рейтинг комментария:{self.user} понизился! ({self.comm_rating})")