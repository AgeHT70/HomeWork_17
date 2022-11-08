# app.py
from flask import request
from flask_restx import Resource, Api

from config import app, db
from models import Movie, MovieSchema, Director, DirectorSchema, GenreSchema, \
    Genre

api = Api(app)

movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')

movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)


# ===========Movies================================
@movie_ns.route('/')
class MoviesViews(Resource):
    def get(self):
        page = int(request.args.get('page', 1))
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        # устанавливаем количество элементов на пагинацию
        items_per_page = 5
        # Вычисляем начало и конец выборки
        pagination_from = (page - 1) * items_per_page
        pagination_to = page * items_per_page

        movies_query = db.session.query(Movie)

        if director_id:
            movies_query = movies_query.filter(
                Movie.director_id == int(director_id))
        if genre_id:
            movies_query = movies_query.filter(
                Movie.genre_id == int(genre_id))

        result = movies_schema.dump(movies_query.all())

        return result[pagination_from:pagination_to], 200

    def post(self):
        request_json = request.json
        insert_row = Movie(**request_json)
        with db.session.begin():
            db.session.add(insert_row)
        return "", 201


@movie_ns.route('/<int:uid>')
class MovieViews(Resource):
    def get(self, uid: int):
        movie = db.session.query(Movie).get(uid)
        if not movie:
            return "", 404

        return movie_schema.dump(movie), 200

    def put(self, uid: int):
        updated_row = db.session.query(Movie).filter(Movie.id ==
                                                     uid).update(request.json)
        if updated_row != 1:
            return "", 400

        db.session.commit()

        return "", 204

    def delete(self, uid: int):
        delete_row = db.session.query(Movie).get(uid)

        if not delete_row:
            return "", 400

        db.session.delete(delete_row)
        db.session.commit()
        return "", 204


# =========Directors================================

@director_ns.route('/')
class DirectorsViews(Resource):
    def get(self):
        directors = db.session.query(Director)
        return directors_schema.dump(directors), 200

    def post(self):
        request_json = request.json
        insert_row = Director(**request_json)

        with db.session.begin():
            db.session.add(insert_row)

        return "", 201


@director_ns.route('/<int:uid>')
class DirectorViews(Resource):
    def get(self, uid: int):
        director = db.session.query(Director).get(uid)
        if not director:
            return "", 404

        return director_schema.dump(director), 200

    def put(self, uid: int):
        updated_row = db.session.query(Director).filter(Director.id ==
                                                        uid).update(
            request.json)
        if updated_row != 1:
            return "", 400

        db.session.commit()

        return "", 204

    def delete(self, uid: int):
        delete_row = db.session.query(Director).get(uid)

        if not delete_row:
            return "", 400

        db.session.delete(delete_row)
        db.session.commit()
        return "", 204


# ============Genres================================

@genre_ns.route('/')
class GenresViews(Resource):
    def get(self):
        genres = db.session.query(Genre)
        return genres_schema.dump(genres), 200

    def post(self):
        request_json = request.json
        insert_row = Genre(**request_json)

        with db.session.begin():
            db.session.add(insert_row)

        return "", 201


@genre_ns.route('/<int:uid>')
class GenreViews(Resource):
    def get(self, uid: int):
        genre = db.session.query(Genre).get(uid)
        if not genre:
            return "", 404

        return genre_schema.dump(genre), 200

    def put(self, uid: int):
        updated_row = db.session.query(Genre).filter(Genre.id == uid).update(
            request.json)
        if updated_row != 1:
            return "", 400

        db.session.commit()

        return "", 204

    def delete(self, uid: int):
        delete_row = db.session.query(Genre).get(uid)

        if not delete_row:
            return "", 400

        db.session.delete(delete_row)
        db.session.commit()
        return "", 204


if __name__ == '__main__':
    app.run(debug=True)
