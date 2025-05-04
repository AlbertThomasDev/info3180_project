"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from flask import Flask, request, jsonify, render_template, send_file, session, send_from_directory
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from app import app, db
import os
from datetime import datetime
from .models import User, Profile, Favourite 
from .forms import RegistrationForm, LoginForm, ProfileForm
from werkzeug.security import check_password_hash
from flask_wtf.csrf import generate_csrf, validate_csrf, CSRFError

###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.route('/api/register', methods=['POST'])
def register():
    try:
        name = request.form.get('name', '').strip()
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        photo = request.files.get('photo')

        names = name.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ''

        filename = secure_filename(photo.filename)
        upload_folder = app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        photo_path = os.path.join(upload_folder, filename)
        photo.save(photo_path)

        hashed_password = generate_password_hash(password)

        new_user = User(
            name=first_name + " " + last_name,
            username=username,
            password_hash=hashed_password,
            email=email,
            photo=filename
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'error': False,
            'message': 'User registered successfully',
            'user': {
                'id': new_user.id,
                'name': new_user.name,
                'username': new_user.username,
                'email': new_user.email,
                'date_joined': new_user.date_joined
            }
        }), 201

    except Exception as e:
        print("Error during registration:", str(e))
        return jsonify({"error": True, "message": "Server error"}), 500

@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        csrf_token = request.headers.get('X-CSRFToken')

        try:
            validate_csrf(csrf_token)
        except CSRFError:
            return jsonify({'message': 'Invalid CSRF token'}), 400

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_profile(user_id):
    # user_id = session.get('user_id')
    if not user_id:
        return jsonify({'message': 'Not authenticated'}), 401

    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({'message': 'User not found'}), 404
    
#New ---------------------------------------------------------------------------------
@app.route('/api/profiles', methods=['GET'])
def get_all_profiles():
    profiles = Profile.query.all()
    return jsonify([profile.to_dict() for profile in profiles]), 200

@app.route('/api/profiles', methods=['POST'])
def add_profile():
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Missing profile data'}), 400
    
    user_id=session.get('user_id')
    existing_profiles_count = Profile.query.filter_by(user_id_fk=user_id).count()
    if existing_profiles_count >= 3:
        return jsonify({'message': 'Profile limit reached. You can only create up to 3 profiles.'}), 403

    try:
        new_profile = Profile(
            user_id_fk=session.get('user_id'), 
            description=data['description'],
            parish=data['parish'],
            biography=data['biography'],
            sex=data['sex'],
            race=data['race'],
            birth_year=data['birth_year'],
            height=data['height'],
            fav_cuisine=data['fav_cuisine'],
            fav_colour=data['fav_colour'],
            fav_school_subject=data['fav_school_subject'],
            political=data['political'],
            religious=data['religious'],
            family_oriented=data['family_oriented']
        )

        
        db.session.add(new_profile)
        db.session.commit()
        return jsonify(new_profile.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/profiles/<int:user_id>', methods=['GET'])
def get_profiles_by_user(user_id):
    profiles = Profile.query.filter_by(user_id_fk=user_id).all()
    if not profiles:
        return jsonify({'error': 'No profiles found for this user'}), 404
    return jsonify([profile.to_dict() for profile in profiles]), 200

# Implement this
@app.route('/api/search', methods=['GET'])
def search_profiles():
    pass

@app.route('/api/profiles/<int:fav_user_id>/favourite', methods=['POST'])
def add_to_favourites(fav_user_id):
    data = request.get_json()
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    # Check if the profile is already in the favourites
    existing_favourite = Favourite.query.filter_by(user_id_fk=user_id, fav_user_id_fk=fav_user_id).first()
    
    if existing_favourite:
        return jsonify({'message': 'Profile already in favourites'}), 200  # Or 409 Conflict

    # If not, add to favourites
    favourite = Favourite(user_id_fk=user_id, fav_user_id_fk=fav_user_id)
    db.session.add(favourite)
    db.session.commit()

    return jsonify({'message': 'Added to favourites'}), 201

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404