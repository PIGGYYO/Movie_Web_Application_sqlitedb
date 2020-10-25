# movies.py
from flask import Blueprint, render_template, url_for, redirect, request, session
from movie_web_app.domain.model import Genre, Actor, Director

import movie_web_app.adapters.repository as repo

# Configure Blueprint.
movies_blueprint = Blueprint('movies_bp', __name__)


@movies_blueprint.route('/display', methods=['GET'])
def display_movies():
    movie_list = []
    movie_title = request.args.get('movie_title')
    name1 = request.args.get('name1')
    name2 = request.args.get('name2')
    name3 = request.args.get('name3')

    title = request.args.get('title')
    if title is None:
        title = 'Movies'

    if title == 'Movies':
        movie_list = repo.repo_instance.dataset_of_movies

    if title == 'Genre':
        try:
            name1 = Genre(name1.strip().strip('<').strip('>'))
        except:
            pass
        try:
            name2 = Genre(name2.strip().strip('<').strip('>'))
        except:
            pass
        try:
            name3 = Genre(name3.strip().strip('<').strip('>'))
        except:
            pass

        for movie in repo.repo_instance.dataset_of_movies:
            if name1 is None and name2 is None and name3 is None:
                return render_template('search_movie/lost.html',
                                       title = 'genres',
                                       redirect_url = url_for('search_bp.search_by_genre'))
            if name1 in movie.genres and name2 in movie.genres and name3 in movie.genres:
                movie_list.append(movie)

    if title == 'Actor':
        try:
            name1 = Actor(name1.strip().strip('<').strip('>'))
        except:
            pass
        try:
            name2 = Actor(name2.strip().strip('<').strip('>'))
        except:
            pass
        try:
            name3 = Actor(name3.strip().strip('<').strip('>'))
        except:
            pass

        for movie in repo.repo_instance.dataset_of_movies:
            if name1 is None and name2 is None and name3 is None:
                return render_template('search_movie/lost.html',
                                   title='actors',
                                   redirect_url=url_for('search_bp.search_by_actor'))
            if name1 in movie.actors and name2 in movie.actors and name3 in movie.actors:
                movie_list.append(movie)

    if title == 'Review':
        movie_list.append(repo.repo_instance.get_movie(movie_title))

    if title == 'Director':
        try:
            name1 = Director(name1.strip().strip('<').strip('>'))
        except:
            pass
        for movie in repo.repo_instance.dataset_of_movies:
            if movie.director == name1:
                movie_list.append(movie)


    per_page = 6
    cursor = request.args.get('cursor')
    if cursor is None:
        cursor = 0
    else:
        cursor = int(cursor)

    movie_ids = []
    for i in range(cursor, cursor + per_page):
        movie_ids += [i]
    movies = []
    for id in movie_ids:
        try:
            movies += [movie_list[id]]
        except:
            pass
    first_movie_url = None
    last_movie_url = None
    prev_movie_url = None
    next_movie_url = None
    if cursor > 0:
        prev_movie_url = url_for('movies_bp.display_movies', cursor = cursor - per_page, title = title, name1 = name1,name2 = name2,name3 = name3)
        first_movie_url = url_for('movies_bp.display_movies', movie_list = movie_list, title = title,name1 = name1,name2 = name2,name3 = name3)

    if cursor + per_page < len(movie_list):
        next_movie_url = url_for('movies_bp.display_movies', cursor = cursor + per_page,title = title,name1 = name1,name2 = name2,name3 = name3)

        last_cursor = per_page * int(len(movie_list) / per_page)
        if len(movie_list) % per_page == 0:
            last_cursor -= per_page
        last_movie_url = url_for('movies_bp.display_movies', cursor=last_cursor,title = title,name1 = name1,name2 = name2,name3 = name3)


    for movie in movie_list:
            movie.add_comment_url = url_for('search_bp.comment_on_movie', title=movie.title)
            for actor in movie.actors:
                actor.add_comment_url = url_for('search_bp.comment_on_actor', title = actor.actor_full_name)
            for genre in movie.genres:
                genre.add_comment_url = url_for('search_bp.comment_on_genre', title = genre.genre_name)
            movie.director.add_comment_url = url_for('search_bp.comment_on_director', title = movie.director.director_full_name)
    return render_template('movies/display_movies.html',
                           title= title,
                           movies=movies,
                           space1 = name1,
                           space2 = name2,
                           space3 = name3,
                           first_movie_url=first_movie_url,
                           last_movie_url=last_movie_url,
                           prev_movie_url=prev_movie_url,
                           next_movie_url=next_movie_url)



@movies_blueprint.route('/display_actor', methods=['GET'])
def display_actor():
    name = request.args.get('name')
    actor = repo.repo_instance.get_actor(name)
    return render_template('movies/display_other.html',
                           name = actor)


@movies_blueprint.route('/display_genre', methods=['GET'])
def display_genre():
    name = request.args.get('name')
    genre = repo.repo_instance.get_genre(name)
    return render_template('movies/display_other.html',
                           name = genre)


@movies_blueprint.route('/display_director', methods=['GET'])
def display_director():
    name = request.args.get('name')
    director = repo.repo_instance.get_director(name)
    return render_template('movies/display_other.html',
                           name = director)
