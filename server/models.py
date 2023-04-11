from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()

class Apartment( db.Model, SerializerMixin ):
    __tablename__ = 'apartments'

    serialize_rules = ('-leases.apartment',)

    id = db.Column( db.Integer, primary_key=True )
    number = db.Column( db.Integer )

    leases = db.relationship( 'Lease', backref='apartment' )


class Tenant( db.Model, SerializerMixin ):
    __tablename__ = 'tenants'

    serialize_rules = ('-leases.tenant',)

    id = db.Column( db.Integer, primary_key=True )
    name = db.Column( db.String, nullable=False )
    age = db.Column( db.Integer)

    leases = db.relationship( 'Lease', backref='tenant' )

    @validates('name')
    def name_validation(self, key, attr):
        if not attr:
            raise NameError('A Name must exist!')
        else:
            return attr
    
    @validates('age')
    def age_validation(self, key, attr):
        if attr >= 18:
            return attr
        else:
            raise ValueError('Please enter an age above 17!')
        

class Lease( db.Model, SerializerMixin ):
    __tablename__ = 'leases'

    serialize_rules = ('-tenant.leases','-apartment.leases')

    id = db.Column( db.Integer, primary_key=True )
    rent = db.Column( db.Integer )

    apartment_id = db.Column( db.Integer, db.ForeignKey( 'apartments.id' ) )
    tenant_id = db.Column( db.Integer, db.ForeignKey( 'tenants.id' ) )

