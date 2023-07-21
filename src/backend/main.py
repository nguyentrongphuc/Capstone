from flask import Flask, request, jsonify, abort, render_template
from flask_cors import CORS
from database.models import setup_db, db_drop_and_create_all, VehicleMake, VehicleModel, db
from auth.auth import AuthError, requires_auth, build_login_link, build_logout_link

def create_app(test_config=None): 
    app = Flask(__name__)
    app.app_context().push()

    if test_config is None:
        app.config.from_object('config.prod')
    else:
        app.config.from_object(test_config)

    setup_db(app)
    db_drop_and_create_all()
    
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
    '''
        GET /
            it should be a public UI endpoint
            it build out an simple fontend to interact with APIs below
        retuns frontend page
    '''
    @app.route('/')
    def home():
        return render_template('home.html', 
                                loginUrl = build_login_link(),
                                logoutUrl = build_logout_link('#logout'))
    
    '''
        GET /resetdata
            it should require the 'admin' permission
            it should reset to default vehicle data
    '''
    @app.route('/resetdata')
    @requires_auth('admin')
    def reset_date():
        db_drop_and_create_all()
        makes = VehicleMake.query.all()
        list = [item.format() for item in makes]

        return jsonify({
            "success": True,
            "makes": list,
            "total": len(list)
        })

    '''
        GET /makes
            it should require the 'get:vehicles' permission
            it should contain the makes.long() data representation
        returns status code 200 and json {"success": True, "makes": makes} where makes is the list
            or appropriate status code indicating reason for failure
    '''
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

    '''
        GET /models
            it should require the 'get:vehicles' permission
            it should contain the models.long() data representation
        returns status code 200 and json {"success": True, "models": models} where models is the list
            or appropriate status code indicating reason for failure
    '''
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

    '''
        GET /makes/search
            it should require the 'get:vehicles' permission
            it should contain the makes.long() data representation
        returns status code 200 and json {"success": True, "makes": makes} where makes is the list and match with search_term
            or appropriate status code indicating reason for failure
    '''
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
            exist_make = VehicleMake.query.get(makeId)
            exist_model = VehicleModel.query.filter(VehicleModel.makeId == makeId,
                                                    VehicleModel.name.like(model_name)).all()
            if exist_make is None:
                return jsonify({
                    "success": False, 
                    "error": 422, 
                    "message": "makeId=`" + str(makeId) + "` NOT existed"
                })
            
            elif len(exist_model) == 0:
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

    '''
        DELETE /makes/<id>
            where <id> is the existing make id
            it should respond with a 404 error if <id> is not found
            it should delete the corresponding row for <id>
            it should require the 'delete:vehicles' permission
        returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
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


