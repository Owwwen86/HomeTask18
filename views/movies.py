from flask import request
from flask_restx import Resource, Namespace
from container import movie_service
from dao.model.movie import MovieSchema
from setup_db import db

movies_ns = Namespace('movies')
movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


@movies_ns.route('/')
class MoviesView(Resource):

    def get(self):
        director_id = request.args.get("director_id")
        genre_id = request.args.get("genre_id")
        year = request.args.get("year")
        movies = movie_service.get_all()
        if director_id:
            movies = movie_service.get_by_director(director_id)

        if genre_id:
            movies = movie_service.get_by_genre(genre_id)

        if year:
            movies = movie_service.get_by_year(year)

        return movies_schema.dump(movies), 200

    def post(self):
        movie = request.json
        try:
            movie_service.create(movie)
            return "Данные добавлены", 201, {"location": f"/movies/{movie.id}"}
        except Exception:
            return 405


@movies_ns.route('/<int:mid>')
class MovieView(Resource):

    def get(self, mid):
        movie = movie_service.get_one(mid)
        return movie_schema.dump(movie), 200

    def put(self, mid):
        data = request.json
        try:
            movie_service.update(data, mid)
            return "Данные обновлены", 201
        except Exception:
            db.session.rollback()
            return 404

    def delete(self, mid):
        try:
            movie_service.delete(mid)
            return "Данные удалены", 204
        except Exception:
            db.session.rollback()
            return 404
