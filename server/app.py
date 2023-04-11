from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

api = Api(app)

# /apartments -> Read, Post(Create) -> Non-RESTful

@app.route('/apartments', methods = ['GET', 'POST'])
def apartments():
    if request.method == 'GET':
        try:
            all_apartments = [a.to_dict() for a in Apartment.query.all()]

            # apartment_query = Apartment.query.all()

            # apartment_list = []
            # for a in apartment_query:
            #     apartment_list.append(a.to_dict())

            # apartment_list = []
            # for a in apartment_query:
            #     apartment_list.append(
            #         {
            #         "id": a.id,
            #         "name": a.number
            #         }
            #     )
            
        except:
            response_body = {
                "Message": "Apartments not found"
            }
            return make_response(response_body, 404)
        else:
            response_body = {"sample": "sample"}

            return make_response(all_apartments, 200)

    elif request.method == 'POST':
        try: 
            newApartment = Apartment(
                number = request.get_json()['number']
            )
        except:
            response_body = {
                "Message": "Unable to create Apartment Instance"
            }
            return make_response(response_body, 409)
        else:
            try:
                db.session.add(newApartment)
                db.session.commit()
            except:
                db.session.rollback()
                response_body = {
                "Message": "Unable to add to Database"
                }
                return make_response(response_body, 409)
            else:
                return make_response(newApartment.to_dict(), 201)
            
# /apartments/<int:id> -> Patch(Update), Delete -> RESTful

class Apartment_by_id(Resource):

    def get(self, id):
        try:
            apartment = Apartment.query.filter(Apartment.id == id).one()
        except:
            response_body = {
                "message": "404 - Apartment not found"
            }
            return make_response(response_body,404)
        else:
            return make_response(apartment.to_dict(), 200)

    def patch(self, id):

        try:
            apartment = Apartment.query.filter(Apartment.id == id).one()

            for attr in request.get_json():
                setattr(apartment, attr, request.get_json()[attr] )

        except:
            response_body = {
                "message": "404 - Apartment not found"
            }
            return make_response(response_body,404)
        else:
            db.session.add(apartment)
            db.session.commit()

            return make_response(apartment.to_dict(), 200)

    def delete(self, id):

        try:
            apartment = Apartment.query.filter(Apartment.id == id).one()

        except:
            response_body = {
                "message": "404 - Apartment not found"
            }
            return make_response(response_body,404)
        else:
            db.session.delete(apartment)
            db.session.commit()

            return make_response({}, 200)

api.add_resource(Apartment_by_id, "/apartments/<int:id>")

# /tenants -> Read, Post(Create) - RESTful

class All_Tenants(Resource):
    
    def get(self):

        try:
            all_tenants = [t.to_dict() for t in Tenant.query.all()]
        except:
            response_body = {
                "Message": "Error in locating All_Tenants!"
            }
            return make_response(response_body, 404)
        else:
            
            return make_response(all_tenants, 200)    

    def post(self):
        
        try:

            # This isn't working? May be a Postman Issue
            # newTenant = Tenant(
            #     name = request.form['name'],
            #     age = request.form['age'],
            # )

            newTenant = Tenant(
                name = request.get_json()['name'],
                age = request.get_json()['age']
            )

        except:
            
            response_body = {
                "message": "Unable to create Tenant! Please Check Validations"
            }
            return make_response(response_body, 409)
        
        else:
            try:
                db.session.add(newTenant)
                db.session.commit()
            except:
                db.session.rollback()

                response_body = {
                    "message": "Unable to add to database, please check to match constraints!"
                }

                return make_response(response_body, 409)
            else:
                
                return make_response(newTenant.to_dict(), 201)

api.add_resource(All_Tenants, "/tenants")

# /tenants/<int:id> -> Patch(Update), Delete -> Non-RESTful



# /leases -> Read, Post(Create) -> RESTful
# /tenants/<int:id> -> Delete -> Non-RESTful


if __name__ == '__main__':
    app.run( port = 3000, debug = True )