"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from flask import Flask, request, jsonify, render_template, send_file, session
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

        # CSRF validation (if you're using Flask-WTF)
        try:
            validate_csrf(csrf_token)
        except CSRFError:
            return jsonify({'message': 'Invalid CSRF token'}), 400

        # Fetch user from database
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            # Store user ID in the session (or you can store a session token)
            session['user_id'] = user.id
            return jsonify({'message': 'Login successful', 'user': user.to_dict()}), 200
        else:
            return jsonify({'message': 'Invalid username or password'}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({'message': 'Internal server error'}), 500
    
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