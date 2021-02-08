from django.db import models
from django.conf import settings
from django.db.models.aggregates import Sum
from uuid import uuid4



# Create your models here.




# Person manager 

class PersonManager(models.Manager):
    def all_with_prefetch_movies(self):
        qs = self.get_queryset()
        return qs.prefetch_related('directed','writing_credits','role_set__movie')





# Movie Manager 

class MovieManager(models.Manager):
    def all_with_prefetch_persons(self):
        qs = self.get_queryset()
        qs = qs.select_related('director')

        qs = qs.prefetch_related('writers','actors')
        return qs 
        
    
    def all_with_related_persons_and_score(self):
        qs = self.all_with_prefetch_persons()
        qs = qs.annotate(score=Sum('vote_value'))
        return qs

    
    def top_movies(self,limit=10):
        qs = self.get_queryset()
        qs = qs.annotate(vote_sum=Sum('vote__value'))

        qs = qs.exclude(vote_sum=None)
        qs = qs.order_by('-vote_sum')
        qs = qs[:limit]
        
        return qs








# VoteManager
class VoteManager(models.Manager):
    
    def get_vote_or_unsaved_blank_vote(self,movie,user):
        
        try:
            return Vote.objects.get(
                movie=movie,
                user=user
            )
        
        except Vote.DoesNotExist:
            return Vote(
                movie=movie,
                user=user
            )











# Movie models class
class Movie(models.Model):

    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3

    RATINGS = (

        (NOT_RATED , 'NR - not rated'),
        (RATED_G , 'G - General Audience'),
        (RATED_PG , 'PG - Parential Guidance''Suggested'),
        (RATED_R , 'R - Restricted'),
        )

    title = models.CharField(max_length=140)
    plot = models.TextField()
    director = models.ForeignKey(to='Person',on_delete=models.SET_NULL,related_name='directed',null=True,blank=True)
    writers = models.ManyToManyField(to='Person',related_name='writing_credits',blank=True)
    actors = models.ManyToManyField(to='Person',through='Role',related_name='acting_credits',blank=True)

    year = models.PositiveIntegerField()
    rating = models.IntegerField(default=NOT_RATED,choices=RATINGS)
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)

    objects = MovieManager()

    def __str__(self):
        return '{} ({})'.format(self.title,self.year)


    class Meta:
        ordering = ('-year',)
 























#  person class

class Person(models.Model):

    first_name = models.CharField(max_length=140)
    last_name = models.CharField(max_length=140)

    born = models.DateField()
    died = models.DateField(null=True,blank=True)



    objects = PersonManager()


    def __str__(self):
        if self.died:
            return '{} , {} ({} -{})'.format(
                self.last_name,
                self.first_name,
                self.born,
                self.died
            )
        return '{}, {} ({}-{})'.format(

            self.last_name,
            self.first_name,
            self.born
        )

    class Meta:
        ordering = ('last_name','first_name')
        





# Role Class

class Role(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person,on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)



    def __str__(self):
        return " {} {}  {} ".format(self.movie.id,self.person.id,self.name)
        
    
    class Meta:
        unique_together =('movie','person','name')







# VOTE MODELS  

class Vote(models.Model):



    UP = 1
    DOWN = 1

    VALUE_CHOICES =  (


        (UP,"Up",),
        (DOWN,"Down",),
    )


    value = models.SmallIntegerField(choices=VALUE_CHOICES,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    voted_on = models.DateTimeField(auto_now=True)




    objects = VoteManager()

    def __str__(self):
        pass


    class Meta:
        unique_together = ('user','movie')





# File upload 

def movie_directory_path_with_uuid(instance,filename):
    return '{}/ {} '.format(instance.movie.id,uuid4())




# File Upload  model 
class MovieImage(models.Model):
    image = models.ImageField(upload_to=movie_directory_path_with_uuid)
    uploaded = models.DateField(auto_now_add=True)
    movie = models.ForeignKey('Movie',on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)