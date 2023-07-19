import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # add one demo row which is helping in POSTMAN test
    
    acura = VehicleMake( name='Acura')
    alfa_romeo = VehicleMake(name='Alfa Romeo')
    acura.insert()
    alfa_romeo.insert()

    model_integra = VehicleModel(name='Integra', makeId=1)
    model_mdx = VehicleModel(name='MDX', makeId=1)
    model_zdx = VehicleModel(name='ZDX', makeId=1)

    model_giulia = VehicleModel(name='Giulia', makeId=2)
    model_tonale = VehicleModel(name='Tonale', makeId=2)
    
    model_integra.insert()
    model_mdx.insert()
    model_zdx.insert()

    model_giulia.insert()
    model_tonale.insert()

class VehicleMake(db.Model):
    __tablename__ = 'VehicleMake'
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=True)
    models = db.relationship('VehicleModel', backref='list', lazy=True)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'models': [item.format() for item in self.models]
        }

class VehicleModel(db.Model):
    __tablename__ = 'VehicleModel'
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(80), unique=True)
    makeId = Column(db.Integer, db.ForeignKey('VehicleMake.id'), nullable=False)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }
    def format_with_make(self):
        return {
            'id': self.id,
            'name': self.name,
            'makeName': VehicleMake.query.get(self.makeId).name #db.session.get(VehicleMake, self.makeId).name
        }