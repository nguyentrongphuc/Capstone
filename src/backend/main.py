from flask import Flask, request, jsonify, abort, render_template
#from sqlalchemy import exc
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, VehicleMake, VehicleModel, db
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    db_drop_and_create_all(app)

    CORS(app)
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # ROUTES
    @app.route('/')
    def home():
        return render_template('home.html')


    @app.route('/makes')
    @requires_auth('get:vehicles')
    def makes(jwt):
        makes = VehicleMake.query.all()
        list = [item.format() for item in makes]
        return jsonify({
            "success": True,
            "makes": list,
            "total": len(list)
        })

    @app.route('/models')
    @requires_auth('get:vehicles')
    def models(jwt):
        models = VehicleModel.query.order_by(VehicleModel.makeId).all()
        list = [item.format_with_make() for item in models]
        return jsonify({
            "success": True,
            "models": list,
            "total": len(list)
        })

    @app.route('/makes/search', methods=['POST'])
    @requires_auth('get:vehicles')
    def search_makes(jwt):
        body = request.get_json()
        search_term = body.get('make_name', '')
        search = "%{}%".format(search_term)
        makes = VehicleMake.query.filter(VehicleMake.name.ilike(search)).all()

        list = [item.format() for item in makes]
        return jsonify({
            "success": True,
            "makes": list,
            "total": len(list)
        })

    @app.route('/makes/<int:id>', methods=['PATCH'])
    @requires_auth('patch:vehicles')
    def update_vehicles(jwt, id):
        body = request.get_json()
        make = VehicleMake.query.get(id) #db.session.get(VehicleMake, id)
        if make == None:    
            abort(404)
        try:
            make.name = body.get('name', None)
            make.update()
        except:
            abort(422)
        
        return jsonify({
            "success": True,
            "makes": [item.format() for item in VehicleMake.query.all()]
        })

    @app.route('/makes', methods=['POST'])
    @requires_auth('post:vehicles')
    def create_makes(jwt):
        body = request.get_json()
        try:
            make_name = body.get('name', None)
            exist_make = VehicleMake.query.filter(VehicleMake.name.like(make_name)).all()

            if len(exist_make) == 0:
                make = VehicleMake(name = make_name)
                make.insert()
            else:
                return jsonify({
                    "success": False, 
                    "error": 422, 
                    "message": "the `" + make_name + "` make already existed"
                })
        except:
            abort(442)
        
        return jsonify({
            "success": True,
            "makes": [item.format() for item in VehicleMake.query.all()]
        })

    @app.route('/models/<int:makeId>', methods=['POST'])
    @requires_auth('post:vehicles')
    def create_models(jwt, makeId):
        body = request.get_json()
        try:
            model_name = body.get('name', None)
            exist_model = VehicleModel.query.filter(VehicleModel.makeId == makeId,
                                                    VehicleModel.name.like(model_name)).all()

            if len(exist_model) == 0:
                model = VehicleModel(
                    name = model_name,
                    makeId = makeId
                )
                model.insert()
            else:
                return jsonify({
                    "success": False, 
                    "error": 422, 
                    "message": "the `" + model_name + "` model already existed"
                })
        except:
            abort(442)
        
        return jsonify({
            "success": True,
            "makes": [item.format() for item in VehicleMake.query.all()]
        })

    @app.route('/makes/<int:id>', methods=['DELETE'])
    @requires_auth('delete:vehicles')
    def delete_makes(jwt, id):
        make = VehicleMake.query.get(id) # db.session.get(VehicleMake, id)
        if make == None:
            abort(404)
        try:
            for model in make.models:
                model.delete()    
            make.delete()
        except:
            abort(422)

        return jsonify({
            "success": True,
            "makes": [item.format() for item in VehicleMake.query.all()]
        })

    # Error Handling
    '''
    Example error handling for unprocessable entity
    '''

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return (
            jsonify({"success": False, "error": 400, "message": "bad request"}),
            400,
        )

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )
    '''
    error handler for AuthError
        error handler should conform to general task above
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return (
            jsonify({"success": False, "error": ex.status_code, "message": ex.error})
        )

    return app

app = create_app()