from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Project, Volunteer
from flask_migrate import Migrate
from auth.auth import AuthError, requires_auth
from config import app, db

CORS(app)
migrate = Migrate(app, db)

RESULTS_PER_PAGE = 10


def paginate_results(results):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    return results[start:end]


@app.route('/projects', methods=['GET'])
@requires_auth('get:projects')
def get_projects(payload):
    projects = Project.query.all()
    return jsonify({
        'success': True,
        'projects': [project.format() for project in
                     paginate_results(projects)],
        'count_projects': len(projects)
    })


@app.route('/volunteers', methods=['GET'])
@requires_auth('get:volunteers')
def get_volunteers(payload):
    volunteers = Volunteer.query.all()
    return jsonify({
        'success': True,
        'volunteers': [volunteer.format() for volunteer in
                       paginate_results(volunteers)],
        'count_volunteers': len(volunteers)
    })


@app.route('/projects', methods=['POST'])
@requires_auth('post:projects')
def post_project(payload):
    try:
        body = request.get_json()
        name = body['name']
        description = body['description']
        email = body['email']
        phone = body['phone']
    except Exception as e:
        print(e)
        abort(400)

    try:
        project = Project(name=name, description=description, email=email,
                          phone=phone)
        db.session.add(project)
        db.session.commit()
        return jsonify({
            'success': True,
            'project': project.format()
        })
    except Exception as e:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/volunteers', methods=['POST'])
@requires_auth('post:volunteers')
def post_volunteer(payload):
    try:
        body = request.get_json()
        name = body['name']
        email = body['email']
        phone = body['phone']
    except Exception as e:
        print(e)
        abort(400)

    try:
        volunteer = Volunteer(name=name, email=email, phone=phone)
        db.session.add(volunteer)
        db.session.commit()
        return jsonify({
            'success': True,
            'volunteer': volunteer.format()
        })
    except Exception as e:
        db.session.rollback()
        abort(422)
    finally:
        db.session.close()


@app.route('/projects/<int:project_id>', methods=['PATCH'])
@requires_auth('patch:projects')
def patch_project(payload, project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()
    if not project:
        abort(404)

    if request.data == b'':
        abort(400)
    body = request.get_json()

    try:
        project.name = body.get('name', project.name)
        project.description = body.get('name', project.description)
        project.email = body.get('email', project.email)
        project.phone = body.get('phone', project.phone)
        db.session.commit()
        return jsonify({
            'success': True,
            'project': project.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)
    finally:
        db.session.close()


@app.route('/volunteers/<int:volunteer_id>', methods=['PATCH'])
@requires_auth('patch:volunteers')
def patch_volunteer(payload, volunteer_id):
    volunteer = Volunteer.query.filter(
        Volunteer.id == volunteer_id).one_or_none()
    if not volunteer:
        abort(404)

    if request.data == b'':
        abort(400)
    body = request.get_json()

    try:
        volunteer.name = body.get('name', volunteer.name)
        volunteer.email = body.get('email', volunteer.email)
        volunteer.phone = body.get('phone', volunteer.phone)
        db.session.commit()
        return jsonify({
            'success': True,
            'volunteer': volunteer.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)
    finally:
        db.session.close()


@app.route('/projects/<int:project_id>', methods=['DELETE'])
@requires_auth('delete:projects')
def delete_project(payload, project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()
    if not project:
        abort(404)

    try:
        db.session.delete(project)
        db.session.commit()
        return jsonify({
            'success': True,
            'project': project.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)
    finally:
        db.session.close()


@app.route('/volunteers/<int:volunteer_id>', methods=['DELETE'])
@requires_auth('delete:volunteers')
def delete_volunteer(payload, volunteer_id):
    volunteer = Volunteer.query.filter(
        Volunteer.id == volunteer_id).one_or_none()
    if not volunteer:
        abort(404)

    try:
        db.session.delete(volunteer)
        db.session.commit()
        return jsonify({
            'success': True,
            'volunteer': volunteer.format()
        })
    except Exception as e:
        db.session.rollback()
        print(e)
        abort(422)
    finally:
        db.session.close()


@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
        'success': False,
        'code': ex.error['code'],
        'message': ex.error['description'],
        'status_code': ex.status_code
    }), ex.status_code


@app.errorhandler(400)
def bad_request(ex):
    return jsonify({
        'success': False,
        'status_code': 400,
        'message': 'Bad request',
    }), 400


@app.errorhandler(404)
def not_found(ex):
    return jsonify({
        'success': False,
        'status_code': 404,
        'message': 'Not found',
    }), 404


@app.errorhandler(422)
def unprocessable(ex):
    return jsonify({
        'success': False,
        'status_code': 422,
        'message': 'Unprocessable',
    }), 422


@app.errorhandler(405)
def method_not_allowed(ex):
    return jsonify({
        'success': False,
        'status_code': 405,
        'message': 'Method not allowed',
    }), 405


@app.errorhandler(401)
def unauthorized(ex):
    return jsonify({
        'success': False,
        'status_code': 401,
        'message': 'Unauthorized',
    }), 401


@app.errorhandler(403)
def forbidden(ex):
    return jsonify({
        'success': False,
        'status_code': 403,
        'message': 'Forbidden',
    }), 403


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
