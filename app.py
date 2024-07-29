from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError


class Config:                                        
    SECRET_KEY = 'mysecret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'jwtsecret'


app = Flask(__name__)                                 
app.config.from_object(Config)


db = SQLAlchemy(app)                                  
api = Api(app)
jwt = JWTManager(app)


class User(db.Model):                                  
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))


with app.app_context():                              
    db.create_all()


class UserRegistration(Resource):                    
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify(message="Username and password are required!"), 400
        
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify(message="Username already exists!"), 400

        new_user = User(username=username)
        new_user.set_password(password)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return jsonify(message="User registered successfully.")
        except IntegrityError:
            db.session.rollback() 
            return jsonify(message="Failed to register user due to an integrity error!"), 500

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify(message="Username and password are required!"), 400
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=user.username)
            return jsonify(access_token=access_token)
        return jsonify(message="Invalid credentials"), 401

class ItemResource(Resource):
    @jwt_required()
    def get(self, item_id):
        item = Item.query.get_or_404(item_id)
        return jsonify(id=item.id, name=item.name, description=item.description)
    
    @jwt_required()
    def put(self, item_id):
        data = request.get_json()
        item = Item.query.get_or_404(item_id)
        item.name = data.get('name')
        item.description = data.get('description')
        db.session.commit()
        return jsonify(message="Item updated successfully.")
    
    @jwt_required()
    def delete(self, item_id):
        item = Item.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return jsonify(message="Item deleted successfully.")

class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        items = Item.query.all()
        return jsonify(items=[{'id': item.id, 'name': item.name, 'description': item.description} for item in items])
    
    @jwt_required()
    def post(self):
        data = request.get_json()
        new_item = Item(name=data.get('name'), description=data.get('description'))
        db.session.add(new_item)
        db.session.commit()
        return jsonify(message="Item created successfully.")


api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(ItemResource, '/items/<int:item_id>')
api.add_resource(ItemListResource, '/items')

if __name__ == '__main__':
    app.run(debug=True)

