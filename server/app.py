#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource

from config import app, db, api
from models import User, UserSchema

class Signup(Resource):

    def post(self):
        data = request.get_json()
        user = User(username=data['username'])
        user.password_hash = data['password']

        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id

        return UserSchema().dump(user), 201


class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')
        if user_id is None:
            return '', 204

        user = db.session.get(User, user_id)
        if user is None:
            return '', 204

        return UserSchema().dump(user), 200


class Login(Resource):

    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user is None or not user.authenticate(data['password']):
            return {'message': 'Invalid username or password.'}, 401

        session['user_id'] = user.id
        return UserSchema().dump(user), 200


class Logout(Resource):

    def delete(self):
        session.pop('user_id', None)
        return '', 204


class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(ClearSession, '/clear', endpoint='clear')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
