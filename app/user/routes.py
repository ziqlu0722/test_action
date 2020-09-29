from flask import redirect, url_for, request, abort, jsonify
from flask_httpauth import HTTPBasicAuth
from app.user import user_bp
from app.models import User
from app import db, auth
from datetime import datetime
from collections import OrderedDict

@user_bp.route('/user', methods=['POST'])
def register():
    body = request.get_json()
    #return 400 if account_created/account_updated provided
    if 'account_created' in body.keys() or 'account_updated' in body.keys():
        abort(400, 'Wrong data fields are provided.')

    #if password is too weak:
    password_input = body['password']
    if not User.valid_passord(password_input):
        abort(400, 'Please use strong password that has at least 9 characters, at least a special character, and at least a digit.')

    #if email format is not valid, return 400
    email_input = body['email_address']
    if not User.valid_email(email_input):
        abort(400, 'The email address is not valid.')

    #if email address already exists, return 400
    email = User.query.filter_by(email_address=email_input).first()
    if email is not None:
        abort(400, 'The email address already exists.')

    user = User(email_address=body['email_address'], 
                first_name=body['first_name'],
                last_name=body['last_name'], 
                )
    
    user.set_password(body['password'])

    user.account_created = user.account_updated = datetime.utcnow()
    db.session.add(user)
    db.session.commit()

    response = {
                'id': str(user.id),
                'first_name': str(user.first_name),
                'last_name': str(user.last_name),
                'email_address': str(user.email_address),
                'account_created': str(user.account_created),
                'account_updated': str(user.account_updated)
                }
    return jsonify(response), 201

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(email_address=username).first()
    if not user or not user.check_password(password):
        abort(401, 'Wrong user or password.')
    return user

@user_bp.route('user/self', methods=['GET', 'PUT'])
@auth.login_required
def account_info():
    user = auth.current_user()
    # view user information
    if request.method == 'GET':
        print('info of user:{}'.format(user))
        response = {
                    'id': str(user.id),
                    'first_name': str(user.first_name),
                    'last_name': str(user.last_name),
                    'email_address': str(user.email_address),
                    'account_created': str(user.account_created),
                    'account_updated': str(user.account_updated)
                    }
        return jsonify(response), 200

    # update user information
    elif request.method == 'PUT':
        body = request.get_json()
        #return 400 for attempt to update account_created, account_updated or email fields
        for field in ['account_created', 'account_updated', 'email_address']:
            if field in body.keys():
                abort(400, 'Data for email_address, account_created and account_updated cannot be updated.')

        ln = body.get('last_name', None)
        fn = body.get('first_name', None)
        pw = body.get('password', None)

        #return 400 if no content for update
        if not ln and not fn and not pw:
            abort(400, 'No value is provided for update')

        else:
            if ln:
                user.last_name = body['last_name'] 

            if fn:
                user.first_name = body['first_name']  

            if pw:
                user.set_password(body['password'])

            user.account_updated = datetime.utcnow()
            db.session.commit()
            return 'Your information has been updated.', 204
