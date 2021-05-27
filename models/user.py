from db import db

### the previous(last section) 'user' is not resource, its a helper defining some methods. so now its called: model(internal)
### while 'registerUser' is resource that API interacts with, now resource(external) will use the model to get data
class UserModel(db.Model):   ### use db's model
    __tablename__ = 'users'    ### table name
    
    ### what cols the table contains
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))   ## 80 chars limitation
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username    ### properties must match with db's cols. 
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
