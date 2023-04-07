from django.db import models
from django.contrib.auth.models import User




class Author(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    author_rating = models.IntegerField(default = 0)
    def update_rating(self):
        # берем рейтинг всех постов автора.Получаем queryset и в цикле перебираем все посты
        list_ = self.aposts.all().values('post_rating')
        sum = 0
        for i in range(len(list_)):
            sum = sum + list_[i]['post_rating']

        # берем все комментарии оставленные автором и в цикле перебираем queryset
        list_ = self.user.usercomment.all().values('comment_rating')
        sum1 = 0
        for i in range(len(list_)):
            sum1 = sum1 + list_[i]['comment_rating']

        list_id = Post.objects.filter(author = self).values('id') # queryset всех статей автора(по id)
        sum2 = 0
        # перебираем все посты автора и все коментарии к каждому посту
        for j in range(len(list_id)):
            list_ = Comment.objects.filter(post_id=self.aposts.values('id')[j]['id']).values('comment_rating')
            for i in range(len(list_)):
                sum2 = sum2 + list_[i]['comment_rating']

        self.author_rating = sum*3 + sum1 + sum2
        self.save()



class Category(models.Model):
    category_name = models.CharField(max_length=100 ,unique=True)

news = 'NW'
post = 'PT'
CHOISE = [(news, 'новость'), (post, 'статья')]

class Post(models.Model):


    time_in = models.DateTimeField(auto_now_add=True)
    news_post = models.CharField(max_length=2 , choices=CHOISE )
    title = models.CharField(max_length=200 , default= 'без заголовка')
    text = models.TextField()
    post_rating = models.IntegerField(default=0)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='aposts')
    category = models.ManyToManyField(Category, through= 'PostCategory')
    def like(self):
        self.post_rating = self.post_rating + 1
        self.save()
    def dislike(self):
        self.post_rating = self.post_rating - 1
        self.save()
    def preview(self):

        if len(self.text) > 124:
            return self.text[0:125] + '...'
        else:
            return self.text

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)

class Comment(models.Model):
    text = models.TextField()
    time_in = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete= models.CASCADE ,related_name='postcomment')
    user = models.ForeignKey(User, on_delete= models.CASCADE, related_name= 'usercomment')
    def like(self):
        self.comment_rating = self.comment_rating + 1
        self.save()
    def dislike(self):
        self.comment_rating = self.comment_rating - 1
        self.save()
