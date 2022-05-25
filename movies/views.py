import requests
import re
from django.shortcuts import render, reverse
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

from .models import Movie

from .forms import MovieForm

API_TOKEN = '35dfe886'


class MovieList(LoginRequiredMixin, ListView):
    login_url = 'login'
    model = Movie
    context_object_name = "movies"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['movies'] = context['movies'].filter(user=self.request.user)
        return context


def movie_search(request):
    context = {}
    data = {}
    error_message = ''
    search_input = request.GET.get('search-area') or ''
    if search_input:
        query = f"http://www.omdbapi.com/?apikey={API_TOKEN}&s={search_input}&type=movie"
        response = requests.get(query).json()
        try:
            data = response['Search']

            for movie in data:  # Add field to see if user already has seen the movie
                if not Movie.objects.filter(user=request.user, imdb_id=movie["imdbID"]).exists():
                    movie["is_in_db"] = False
                else:
                    movie["is_in_db"] = True
                    obj = Movie.objects.get(user=request.user, imdb_id=movie["imdbID"])
                    movie["percent_seen"] = obj.percent_seen
                    movie["minutes_seen_formatted"] = obj.minutes_seen_formatted
                    movie["runtime_formatted"] = obj.runtime_formatted
                    movie["release_year"] = obj.release_year

        except KeyError as e:
            error_message = f"No result for '{search_input}'"

    context = {'movies': data, 'search_input': search_input, 'error_message': error_message}
    return render(request, 'movies/movie_search.html', context=context)


def movie_add(request, imdb_id):
    query = f"http://www.omdbapi.com/?apikey={API_TOKEN}&i={imdb_id}"
    data = requests.get(query).json()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            if Movie.objects.filter(user=request.user, imdb_id=data["imdbID"]).exists():
                Movie.objects.filter(user=request.user, imdb_id=data["imdbID"]).update(
                    minutes_seen=form['minutes_seen'].value(),
                    is_fully_seen=form['is_fully_seen'].value())
            else:
                Movie.objects.create(user=request.user,
                                     imdb_id=imdb_id,
                                     title=data['Title'],
                                     release_date=data['Released'],
                                     runtime=int(re.findall(r'\d+', data['Runtime'])[0]),
                                     minutes_seen=form['minutes_seen'].value(),
                                     is_fully_seen=form['is_fully_seen'].value(),
                                     poster_url=data['Poster'])
            return HttpResponseRedirect(reverse('home'))
    else:
        if Movie.objects.filter(user=request.user, imdb_id=data["imdbID"]).exists():
            obj = Movie.objects.get(user=request.user, imdb_id=data["imdbID"])
            form = MovieForm(initial={'minutes_seen': obj.minutes_seen})
            data['exists'] = True
            data['id'] = obj.id
        else:
            form = MovieForm()
            data['exists'] = False
        form.fields['minutes_seen'].max_value = int(re.findall(r'\d+', data['Runtime'])[0])
        form.fields['minutes_seen'].widget.attrs['max'] = int(re.findall(r'\d+', data['Runtime'])[0])
        context = {'movie': data, 'form': form}

    return render(request, 'movies/movie.html', context=context)


class MovieDelete(LoginRequiredMixin, DeleteView):
    model = Movie
    success_url = reverse_lazy('home')

# class MovieUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Movie
#     template_name = 'movies/movie.html'
#     # fields = ['minutes_seen', 'is_fully_seen']
#     success_url = reverse_lazy('home')
#     form_class = MovieForm()
#     form_class.fields['minutes_seen'].max_value = int(re.findall(r'\d+', model['Runtime'])[0])
#     form_class.fields['minutes_seen'].widget.attrs['max'] = int(re.findall(r'\d+', model['Runtime'])[0])
#
#     def test_func(self):
#         if self.request.user == self.get_object().user:
#             return True
#         else:
#             return False
