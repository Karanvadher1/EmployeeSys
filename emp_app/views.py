import datetime
from flask import abort, render_template, request, redirect, url_for, flash,jsonify,session
from emp_app import emp_app,db
from flask_login import LoginManager, login_required
from emp_app.models import User, UserProfile
from functools import wraps
import jwt
from emp_app.utils import detectUser

login_manager = LoginManager()

def check_role_admin(user):
    pass
def check_role_employee(user):
    pass
def check_role_superuser(user):
    pass


@emp_app.route('/')
def home():
    return render_template('home.html')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, emp_app.config['SECRET_KEY'])
            current_user = User.query\
                .filter_by(username = data['username'])\
                .first()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users context to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated

@emp_app.route('/registerEmployee',methods = ['POST'])
def registerEmployee():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('registerEmployee'))
        if not username or not email or not password:
            flash('Please provide correct information')
        elif password != confirm_password:
            flash('Password did not match')
        else:
            User.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password = password,
            )
            flash('Registration successful! You are now logged in.', 'success')
            return render_template('login.html')
    return render_template('account/registerEmployee.html')
    

@emp_app.route('/registerAdmin',methods = ['POST'])
def registerAdmin():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('registerAdmin'))
        if not username or not email or not password:
            flash('Please provide correct information')
        elif password != confirm_password:
            flash('Password did not match')
        else:
            User.create_admin(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                password = password,
            )
            flash('Registration successful! You are now logged in.', 'success')
            return render_template('login.html')
    return render_template('account/registerAdmin.html')

@emp_app.route('/superuser',methods = ['POST'])
def superuser():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('password')
        
        existing_user = User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first()
        if existing_user:
            flash('Username or email already exists. Please choose another.', 'danger')
            return redirect(url_for('superuser'))
        if not username or not email or not password:
            flash('Please provide correct information')
        elif password != confirm_password:
            flash('Password did not match')
        else:
            User.create_superuser(
                username = username,
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
            )
            flash('Registration successful! You are now logged in.', 'success')
            return render_template('login.html')
    return render_template('account/superAdmin.html')

# @emp_app.route('/', methods =['GET'])
# @token_required
# def get_all_users(current_user):
#     users = User.query.all()
#     output = []
#     for user in users:
#         output.append({
#             'username': user.username,
#             'email' : user.email
#         })
  
#     return jsonify({'users': output})

@emp_app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        # get_user(user)
        if user and user.check_password(password):
            token = jwt.encode(
                {
                    'username':user.username,
                    'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
                },emp_app.config['SECRET_KEY']
            )
            session['token'] = token
            session['user'] = user
            flash('Login successful!', 'success')
            return redirect(url_for('myaccount'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# def get_user(user):
#     user = User.query.get(user)
#     return user

@login_required
@emp_app.route('/myaccount',methods = ['GET','POST'])
def myaccount():
    if 'user' in session:
        user = session['user']
        user = User.query.get(user)        
        redirect_url = detectUser(user)
        return render_template(redirect_url)
    
@login_required
@emp_app.route('/myaccount/profile', methods=['POST'])
def profile():
    if request.method == 'POST':
        profile_picture = request.form.get('profile_picture')
        address = request.form.get('address')
        city = request.form.get('city')
        pin_code = request.form.get('pin_code')
        state = request.form.get('state')
        country = request.form.get('country')                
        UserProfile.update_profile(
            profile_picture = profile_picture,
            address = address,
            city = city,
            pin_code = pin_code,
            state = state,
            country = country,
        )
        flash('Profile updated', 'success')
        return redirect('EMPdashboard')
    else:
        flash('profile not updated')
        return render_template('/account/profile.html')  
    

@emp_app.route('/logout')
@login_required
def logout():
    if 'user' in session:
        user = session['user']
        session.pop(user)
        return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

