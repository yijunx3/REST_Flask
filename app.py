import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister   ### resource has __init__.py, meaning its a package and you can look up files in it
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'   ### tell alchemy where to find data.db
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')   ### if using heroku's db, note os is heroku's. if no postgres, use default sqlite locally
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   ### not use flasksqlalchemy to track(too much resource), use sqlalchemy to track
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

### postman setting:
### 1. in endpoints , replace http... by url, and set url = http... in env
### 2. in secure needed endpoints, set up var: jwt_token
### 3. in authen endpoint, code js tests to get token, view in env
### 4. in other endpoints, can do tests such as time > 200 milisec, status = 200, etc


### no manual run 'create_table.db' before run app.py
### comment this if deploying to heroku since is using run.py to deploy both app.py & db.py
#@app.before_first_request
#def create_tables():
#    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db   ## why here? b/c model also import db, if bring this up, cause circular import
    db.init_app(app)
    app.run(port=5000, debug=True)
