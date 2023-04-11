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
            return make_response(response_body, 404)
        else:
            try:
                db.session.add(newApartment)
                db.session.commit()
            except:
                db.session.rollback()
                response_body = {
                "Message": "Unable to add to Database"
                }
                return make_response(response_body, 404)
            else:
                return make_response(newApartment.to_dict(), 200)
            
# /apartments/<int:id> -> Patch(Update), Delete

# /tenants -> Read, Post(Create) - RESTful
# /tenants/<int:id> -> Patch(Update), Delete -> Non-RESTful

# /leases -> Read, Post(Create) -> RESTful
# /tenants/<int:id> -> Delete -> Non-RESTful


if __name__ == '__main__':
    app.run( port = 3000, debug = True )