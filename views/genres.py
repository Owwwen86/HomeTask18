from flask_restx import Resource, Namespace
from container import genre_service
from dao.model.genre import GenreSchema

genres_ns = Namespace('genres')
genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


@genres_ns.route('/')
class GenresView(Resource):

    def get(self):
        genres = genre_service.get_all()
        return genres_schema.dump(genres), 200


@genres_ns.route('/<int:gid>')
class GenreView(Resource):

    def get(self, gid):
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except Exception:
            return 404
