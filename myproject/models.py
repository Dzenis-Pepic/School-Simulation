from myproject import db
from flask_login import UserMixin

users_courses= db.Table('users_courses',\
db.Column('user_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),\
db.Column('course_id',db.Integer,db.ForeignKey('courses.id'),primary_key=True)\
)

users_rates= db.Table('users_rates',\
db.Column('user_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),\
db.Column('rate_id',db.Integer,db.ForeignKey('rates.id'),primary_key=True)\
)

courses_rates= db.Table('courses_rates',\
db.Column('course_id',db.Integer,db.ForeignKey('courses.id'),primary_key=True),\
db.Column('rate_id', db.Integer, db.ForeignKey('rates.id'),  primary_key=True)\
)

courses_actives= db.Table('courses_actives',
db.Column('course_id',db.Integer,db.ForeignKey('courses.id'),primary_key=True),\
db.Column('active_id',db.Integer,db.ForeignKey('actives.id'),primary_key=True)\
)

users_actives= db.Table('users_actives',\
db.Column('user_id',db.Integer,db.ForeignKey('users.id'),primary_key=True),\
db.Column('active_id',db.Integer,db.ForeignKey('actives.id'),primary_key=True)\
)


class User(db.Model,UserMixin):
    __tablename__='users'

    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.String(50))
    last_name=db.Column(db.String(50))
    email=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(50))
    role_id=db.Column(db.Integer)
    courses=db.relationship('Course', secondary=users_courses,\
        backref='users', lazy='dynamic')
    ocene=db.relationship('Rate', secondary=users_rates,\
        backref='users', lazy='dynamic')
    is_active=db.relationship('Active', secondary=users_actives,\
        backref='users', lazy='dynamic')
    zahtevi=db.relationship('Zahtev',backref='users', lazy='dynamic')

    def __init__(self,first_name,last_name,email,password, role_id):
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=password
        self.role_id=role_id

    def range_role_id(self,role_id):
        if role_id>3:
            raise ValueError("Role_id ne moze biti veci od 3!")


class Course(db.Model):
    __tablename__='courses'

    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    teacher_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    ocene=db.relationship('Rate', secondary=courses_rates,\
        backref='courses', lazy='dynamic')
    is_active=db.relationship('Active', secondary=courses_actives,\
        backref='courses', lazy='dynamic')
    zahtevi=db.relationship('Zahtev',backref='courses', lazy='dynamic')

    def __init__(self,name,teacher_id):
        self.name=name
        self.teacher_id=teacher_id

class Rate(db.Model):
    __tablename__='rates'

    id=db.Column(db.Integer, primary_key=True)
    ocena=db.Column(db.Integer)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def __init__(self,ocena,course_id,user_id):
        self.ocena=ocena
        self.course_id=course_id
        self.user_id=user_id

    def range_ocena(self,ocena):
        if ocena>5:
            raise ValueError("Ocena ne moze biti veci od 5!")


class Active(db.Model):
    __tablename__='actives'

    id=db.Column(db.Integer, primary_key=True)
    is_active=db.Column(db.Boolean,default=True)
    course_id=db.Column(db.Integer,db.ForeignKey('courses.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def __init__(self,is_active,course_id,user_id):
        self.is_active=is_active
        self.course_id=course_id
        self.user_id=user_id

class Zahtev(db.Model):
    __tablename__='zahtevi'

    id=db.Column(db.Integer, primary_key=True)
    course_id=db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
    prihvacen=db.Column(db.String(50), default="cekanje")

    def __init__(self,course_id,user_id):
        self.course_id=course_id
        self.user_id=user_id
