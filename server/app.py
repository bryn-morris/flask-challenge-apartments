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

@app.route('/tenants/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def tenant_by_id(id):    
    try:
        selected_tenant = Tenant.query.filter(Tenant.id == id).one()
    except:
        response_body = {
            'message': '404, tenant not found '
        }
        return make_response(response_body, 404)
    else:
        if request.method == "GET":
            
            return make_response(selected_tenant.to_dict(), 200)

        elif request.method == "PATCH":
            try:
                for key in request.get_json():
                    setattr(selected_tenant, key, request.get_json()[key])
                db.session.add(selected_tenant)
                db.session.commit()
            except:
                response_body = {
                    "message": "Unable to add to Database, please check constraints! :]"
                }
                return make_response(response_body, 304)
            else:
                return make_response(selected_tenant.to_dict(), 200)

        elif request.method == 'DELETE':
            
            db.session.delete(selected_tenant)
            db.session.commit()

            return make_response({}, 200)
    


# /leases -> Read, Post(Create) RESTFUL

class All_Leases(Resource):
    
    def get(self):
        try:
            all_leases = [l.to_dict() for l in Lease.query.all()]
        except:
            response_body = {
                "message": "404 - Unable to Locate any leases!"
            }
            return make_response(response_body, 404)
        else:
            return make_response(all_leases, 200)
    def post(self):
        try:
            newLease = Lease(
                rent = request.get_json()['rent'],
                apartment_id = request.get_json()['apartment_id'],
                tenant_id = request.get_json()['tenant_id']
            )
        except:
            response_body = {
                "message":"Unable to make Lease Instance, please check validations"
            }
            return make_response(response_body, 409)
        else:
            try:
                db.session.add(newLease)
                db.session.commit()
            except:
                db.session.rollback()
                response_body = {
                    "message": "Unable to add to Database, please check constraints"
                }
                return make_response(response_body, 409)
            else:
                return make_response(newLease.to_dict(), 201)                


api.add_resource(All_Leases, "/leases")

# /leases/<int:id> -> DELETE -> non-RESTful

@app.route('/leases/<int:id>', methods = ["GET","DELETE"])
def leases_by_id(id):
    try:
        selected_lease = Lease.query.filter(Lease.id == id).one()
    except:
        response_body = {
            "message":"404 - Lease not found"
        }
        return make_response(response_body, 404)
    else:
        if request.method == "DELETE":
            
            db.session.delete(selected_lease)
            db.session.commit()

            return make_response({}, 200)
        elif request.method == "GET":
            
            return make_response(selected_lease.to_dict(), 200)



if __name__ == '__main__':
    app.run( port = 3000, debug = True )