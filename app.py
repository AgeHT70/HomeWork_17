# app.py
from flask_restx import Resource, Api

from config import app
from models import Movie, MovieSchema

api = Api(app)
movie_ns = api.namespace('movies')
movies_schema = MovieSchema(many=True)

@movie_ns.route('/', methods=['GET', 'POST'])
class MoviesViews(Resource):
    def get(self):
        result = movies_schema.dump(Movie.query.all())
        return result


if __name__ == '__main__':
    app.run(debug=True)
