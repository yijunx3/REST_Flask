from db import db

### the previous(last section) 'item' has direct method with API like GET/POST/DEL/PUT & helpers like 'find','insert'
### these 'find','save','del' are helpers, not resources, so belong to models
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))   ### foreignKey
    store = db.relationship('StoreModel')   ### no need to do 'join'

    def __init__(self, name, price, store_id):   ### store_id is another property
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price}

    ### no need for connecting, cursor..
    @classmethod
    def find_by_name(cls, name):   ### will return the obj
        return cls.query.filter_by(name=name).first()  ## meaning: SELECT * FROM items WHERE name = name

    ### for both 'insert' and 'update'
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    ### for 'delete'
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
