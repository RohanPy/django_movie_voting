from django.shortcuts import render,reverse,redirect
from django.views.generic import ListView,DetailView,CreateView,UpdateView
from core.models import Movie, Person,Vote
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from core.forms import VoteForm, MovieImageForm
# Create your views here.


# Movie list
class MovieList(ListView):
    model = Movie
    # paginate_by = 1
    template_name = 'pages/movie_list.html'



# Movie Detail view 
class MovieDetail(DetailView):
    queryset = (
        Movie.objects.all_with_related_persons_and_score()
    )


    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_form'] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user = self.request.user
            )

            if vote.id:
                vote_form_url = reverse(

                    'core:UpdateVote',

                    kwargs={

                        'movie_id':vote.movie.id,
                        'pk':vote.id
                    }
                )


            else:

                vote_form_url = (

                    reverse(

                        'core:CreateVote',
                        kwargs={
                            'movie_id':self.object.id
                        }
                    )
                )

        
            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url

        return ctx

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None






    template_name = 'pages/movie_detail.html'
    # page pending on 50 



# PersonDetailView 
class PersonDetail(DetailView):
    queryset = Person.objects.all_with_prefetch_movies()






# create vote 
class CreateVote(LoginRequiredMixin,CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs[

            'movie_id'
        ]
        return initial

    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
            'core:MovieDetail',
            kwargs={
                'pk':movie_id
            }
        )
        return redirect(
            to=movie_detail_url
        )

    
    def render_to_response(self,context,**response_kwargs):
        movie_id =  context['object'].id
        movie_detail_url = reverse(
            'core:MovieDetail',
            kwargs={'pk':movie_id}
        )
        return redirect(to=movie_detail_url)



    

# Update vote 
class UpdateVote(LoginRequiredMixin,UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self,queryset=None):
        vote  = super().get_object(queryset)

        user = self.request.user

        if vote.user != user:
            raise PermissionDenied('Cannot Change another users vote')
        return vote

    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail',kwargs={'pk':movie_id})

    

    def render_to_response(self,context,**response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return redirect(to=movie_detail_url)




# MovieImageUpload 

class MovieImageUpload(LoginRequiredMixin,CreateView):
    form_class = MovieImageForm


    def get_initial(self):
        initial = super().get_initial()
        initial['user'] =  self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial


    def render_to_response(self,context,**response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return redirect(to=movie_detail_url)
    
    def get_success_url(self):
        movie_id  = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return movie_detail_url





# Top Movies

class TopMovies(ListView):
    template_name = 'pages/top_movie_list.html'
    queryset = Movie.objects.top_movies(limit=10)