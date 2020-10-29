# search_movie.py
from flask import Blueprint, render_template, url_for, redirect, request, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, HiddenField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError
import movie_web_app.adapters.repository as repo
from movie_web_app.authentication.authentication import login_required
from movie_web_app.domain.model import Review
from sqlalchemy.orm.collections import InstrumentedList
import sqlalchemy

# Configure Blueprint.
search_blueprint = Blueprint('search_bp', __name__)


@search_blueprint.route('/search_by_director', methods=['GET', 'POST'])
def search_by_director():
    form = DirectorForm()
    if form.validate_on_submit():
        director_full_name = form.director_full_name.data
        director = repo.repo_instance.get_director(director_full_name)
        if director is None:
            return render_template('search_movie/lost.html',
                                   title = 'Director',
                                   redirect_url = url_for('search_bp.search_by_director'))
        return redirect(url_for('movies_bp.display_movies', title='Director', name1= director))
    return render_template('search_movie/director.html',
                           form = form,
                           handler_url = url_for('search_bp.search_by_director'))


class DirectorForm(FlaskForm):
    director_full_name = StringField("Director Name",[DataRequired(message='Director name is required')])
    submit = SubmitField('Search by Director')


@search_blueprint.route('/search_by_genre', methods=['GET', 'POST'])
def search_by_genre():
    form = GenreForm()
    if form.validate_on_submit():
        genre1 = form.name1.data
        genre2 = form.name2.data
        genre3 = form.name3.data
        genre1 = repo.repo_instance.get_genre(genre1)
        genre2 = repo.repo_instance.get_genre(genre2)
        genre3 = repo.repo_instance.get_genre(genre3)
        return redirect(url_for('movies_bp.display_movies', title='Genre', name1=genre1,name2 = genre2, name3 = genre3))
    return render_template('search_movie/genre_actor.html',
                           form = form,
                           handler_url = url_for('search_bp.search_by_genre'))


class GenreForm(FlaskForm):
    name1 = StringField("Genre 1",[DataRequired(message='Genre is required')])
    name2 = StringField("Genre 2",[DataRequired(message='Genre is required')])
    name3 = StringField("Genre 3",[DataRequired(message='Genre is required')])
    submit = SubmitField('Search by Genre')


@search_blueprint.route('/search_by_actor', methods=['GET', 'POST'])
def search_by_actor():
    form = ActorForm()
    if form.validate_on_submit():
        actor1 = form.name1.data
        actor2 = form.name2.data
        actor3 = form.name3.data
        actor1 = repo.repo_instance.get_actor(actor1)
        actor2 = repo.repo_instance.get_actor(actor2)
        actor3 = repo.repo_instance.get_actor(actor3)
        return redirect(url_for('movies_bp.display_movies', title='Actor', name1=actor1, name2=actor2, name3=actor3))
    return render_template('search_movie/genre_actor.html',
                           form = form,
                           handler_url = url_for('search_bp.search_by_actor'))


class ActorForm(FlaskForm):
    name1 = StringField("Actor 1",[DataRequired(message='Actor is required')])
    name2 = StringField("Actor 2",[DataRequired(message='Actor is required')])
    name3 = StringField("Actor 3",[DataRequired(message='Actor is required')])
    submit = SubmitField('Search by Actor')


@search_blueprint.route('/comment', methods=['GET', 'POST'])
@login_required
def comment_on_movie():
    username = session['username']
    form = CommentForm()
    if form.validate_on_submit():
        title = form.title.data
        review = Review(username, title, None,None,None,form.comment.data, form.rating.data)
        movie = repo.repo_instance.get_movie(title)
        if isinstance(movie.review, sqlalchemy.orm.collections.InstrumentedList):
            repo.repo_instance.add_review(review)
        else:
            movie.review.append(review)
        movie.add_comment_url = url_for('search_bp.comment_on_movie', title=movie.title)
        return redirect(url_for('movies_bp.display_movies', title = 'Review', movie_title= title))

    if request.method == 'GET':
        title = request.args.get('title')
        form.title.data = title
    else:
        title = form.title.data
    movie = repo.repo_instance.get_movie(title)
    return render_template(
        'search_movie/comment_on_movie.html',
        title='Review',
        movie=movie,
        comment = movie.review,
        form=form,
        handler_url=url_for('search_bp.comment_on_movie'))


@search_blueprint.route('/comment_actor', methods=['GET', 'POST'])
@login_required
def comment_on_actor():
    username = session['username']
    form = CommentForm()
    if form.validate_on_submit():
        title = form.title.data
        review = Review(username, None,None,None, title,form.comment.data, form.rating.data)
        actor = repo.repo_instance.get_actor(title)
        if isinstance(actor,list):
            actor= actor[0]
        if isinstance(actor.review, sqlalchemy.orm.collections.InstrumentedList):
            repo.repo_instance.add_review(review)
        else:
            actor.review.append(review)
        try:
            actor.rating += review.rating
            actor.rating_num += 1
        except:
            pass
        actor.add_comment_url = url_for('search_bp.comment_on_actor', title=actor.actor_full_name)
        return redirect(url_for('movies_bp.display_actor', title = 'Review_Actor', name= title))

    if request.method == 'GET':
        title = request.args.get('title')
        form.title.data = title
    else:
        title = form.title.data
    actor = repo.repo_instance.get_actor(title)
    if isinstance(actor, list):
        actor = actor[0]
    return render_template(
        'search_movie/comment_on_other.html',
        title='Review_Actor',
        name=actor,
        comment = actor.review,
        form=form,
        handler_url=url_for('search_bp.comment_on_actor'))


@search_blueprint.route('/comment_genre', methods=['GET', 'POST'])
@login_required
def comment_on_genre():
    username = session['username']
    form = CommentForm()
    if form.validate_on_submit():
        title = form.title.data
        review = Review(username, None,None,title,None, form.comment.data, form.rating.data)
        genre = repo.repo_instance.get_genre(title)
        if isinstance(genre,list):
            genre = genre[0]
        if isinstance(genre.review, sqlalchemy.orm.collections.InstrumentedList):
            repo.repo_instance.add_review(review)
        else:
            genre.review.append(review)
        try:
            genre.rating += review.rating
            genre.rating_num += 1
        except:
            pass
        genre.add_comment_url = url_for('search_bp.comment_on_genre', title=genre.genre_name)
        return redirect(url_for('movies_bp.display_genre', title = 'Review_Genre', name= title))

    if request.method == 'GET':
        title = request.args.get('title')
        form.title.data = title
    else:
        title = form.title.data
    genre = repo.repo_instance.get_genre(title)
    if isinstance(genre, list):
        genre = genre[0]
    return render_template(
        'search_movie/comment_on_other.html',
        title='Review_Genre',
        name=genre,
        comment = genre.review,
        form=form,
        handler_url=url_for('search_bp.comment_on_genre'))


@search_blueprint.route('/comment_director', methods=['GET', 'POST'])
@login_required
def comment_on_director():
    username = session['username']
    form = CommentForm()
    if form.validate_on_submit():
        title = form.title.data
        review = Review(username, None, title, None, None, form.comment.data, form.rating.data)
        director = repo.repo_instance.get_director(title)
        if isinstance(director,list):
            director = director[0]
        if isinstance(director.review, sqlalchemy.orm.collections.InstrumentedList):
            repo.repo_instance.add_review(review)
        else:
            director.review.append(review)
        try:
            director.rating += review.rating
            director.rating_num += 1
        except:
            pass
        director.add_comment_url = url_for('search_bp.comment_on_director', title=director.director_full_name)
        return redirect(url_for('movies_bp.display_director', title = 'Review_Director', name= title))

    if request.method == 'GET':
        title = request.args.get('title')
        form.title.data = title
    else:
        title = form.title.data
    director = repo.repo_instance.get_director(title)
    if isinstance(director,list):
        director = director[0]
    return render_template(
        'search_movie/comment_on_other.html',
        title='Review_Director',
        name=director,
        comment = director.review,
        form=form,
        handler_url=url_for('search_bp.comment_on_director'))


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short')])
    rating = IntegerField('Rating',[
        DataRequired(message='Rating is required')])
    title = HiddenField("Title")
    submit = SubmitField('Submit')


