from flask import Flask, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )

# /apartments -> Read, Post(Create) -> Non-RESTful
# /apartments/<int:id> -> Patch(Update), Delete

# /tenants -> Read, Post(Create) - RESTful
# /tenants/<int:id> -> Patch(Update), Delete -> Non-RESTful

# /leases -> Read, Post(Create) -> RESTful
# /tenants/<int:id> -> Delete -> Non-RESTful


if __name__ == '__main__':
    app.run( port = 3000, debug = True )