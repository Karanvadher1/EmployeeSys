from datetime import datetime
from flask_login import UserMixin,login_manager
from emp_app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    password = db.Column(db.String(), nullable=False)
    username = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_employee = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)
    is_superadmin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def create_user(cls, username, first_name, last_name, email, password=None):
        if not email:
            raise ValueError('user must have an E-mail address')

        if not username:
            raise ValueError('user must have an username')

        user = cls(
            email = email.lower(),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password) 
        user.role_id = 1
        user.is_admin = False
        user.is_active = True
        user.is_employee = True
        user.is_superadmin = False
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def create_admin(cls, username, first_name, last_name, email, password=None):
        user = cls.create_user(
            email = email.lower(),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )   
        user.role_id = 2
        user.is_admin = True
        user.is_active = True
        user.is_employee = True
        user.is_superadmin = False
        db.session.add(user)
        db.session.commit()
        return user
   
    @classmethod
    def create_superuser(cls, username, first_name, last_name,email, password=None):
        user = cls.create_user(
            email = email.lower(),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )   
        user.role_id = 3
        user.is_admin = True
        user.is_active = True
        user.is_employee = True
        user.is_superadmin = True
        db.session.add(user)
        db.session.commit()
        return user


class role(db.Model, UserMixin):
    
    id = db.Column(db.Integer,primary_key = True)
    role = db.Column(db.String(50), unique = True, nullable = False)
    
class UserProfile(db.Model, UserMixin):
    
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
    profile_picture =  db.Column(db.String(50), nullable=False)#url for photo
    address =  db.Column(db.String(50), nullable=False)
    city =  db.Column(db.String(50), nullable=False)
    pin_code =  db.Column(db.Integer(), nullable=False)
    state =  db.Column(db.String(50), nullable=False)
    country =  db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    modified_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def update_profile(cls, user,profile_picture, address, city, pin_code, state, country):
        profile = cls.update_profile(
            user = user,
            profile_picture= profile_picture,
            address = address,
            city = city,
            pin_code = pin_code,
            state = state,
            country = country,
        )
        db.session.add(profile)
        db.session.commit()
        return profile
    