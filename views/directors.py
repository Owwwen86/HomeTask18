from flask_restx import Resource, Namespace
from container import director_service
from dao.model.director import DirectorSchema

directors_ns = Namespace('directors')
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@directors_ns.route('/')
class DirectorsView(Resource):

    def get(self):
        directors = director_service.get_all()
        return directors_schema.dump(directors), 200


@directors_ns.route('/<int:did>')
class DirectorView(Resource):

    def get(self, did):
        director = director_service.get_one(did)
        return director_schema.dump(director), 200
