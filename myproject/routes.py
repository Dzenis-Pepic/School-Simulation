from myproject import app, db
from myproject.schemas import *
from myproject.models import User,Course,Rate,Active,Zahtev
from flask_login import current_user
from flask import session
from flask import jsonify, request, make_response, Response
import requests,json
from sqlalchemy import func
import jwt
import datetime
from functools import wraps
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app.route('/',methods=['POST'])
def index():
    return "KAKO SI"

@app.route("/login", methods=["POST"])
def login():
    body = request.get_json()

    try:
        result = LoginSchema().load(body)
    except ValidationError as err:
        return jsonify(err.messages)

    user = User.query.filter_by(email=body['email']).first()


    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=user.id, expires_delta=expires)

    return jsonify({'token': access_token}, 200)

@app.route('/register', methods=['POST'])
def register():
    #if current_user.role_id==3:
        body=request.get_json()
        try:
            user_schema=UserSchema()
            result = user_schema.load(body)
            user= User(first_name=body['first_name'],\
             last_name=body['last_name'],email=body['email'],\
             password=body['password'],role_id=body['role_id'])
            db.session.add(user)
            db.session.commit()
            user_s=user_schema.dump(user)
            if user.role_id==1:
                return jsonify({"Uspesno ste registrovali nastavnika!":user_s})
            elif user.role_id==2:
                return jsonify({"Uspesno ste registrovali studenta!":user_s})
            return  jsonify({"Uspesno ste registrovali admina!":user_s})
        #return "Samo admin ima pristup ovoj stranici!"
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)

@app.route('/add_course', methods=['POST'])
@jwt_required()
def add_course():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            add_course_schema=AddCourseSchema()
            result = add_course_schema.load(body)
            name=body['name']
            teacher_id= current_user.id
            kurs=Course(name=name,teacher_id=teacher_id)
            db.session.add(kurs)
            current_user.courses.append(kurs)
            db.session.commit()
            course_schema=CourseSchema()
            k= course_schema.dump(kurs)
            return jsonify({"Uspesno ste dodali kurs":k})
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/all_courses',methods=['GET'])
def all_courses():
    kursevi=Course.query.all()
    course_schema=CourseSchema(many=True)
    kursevi= course_schema.dump(kursevi)
    return jsonify({"Svi dostupni kursevi su": kursevi})

@app.route('/teacher_courses', methods=['GET'])
@jwt_required()
def teacher_courses():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        course_schema=CourseSchema(many=True)
        moji=Course.query.filter_by(teacher_id=current_user.id)
        moji=course_schema.dump(moji)
        return jsonify({"Kursevi koje ja predajem su": moji})
    return "Nemate pristup ovoj stranici!"

@app.route('/update_course/<id>', methods=['PUT'])
@jwt_required()
def update_course(id):
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            par={"id":id}
            try:

                id_schema=IdSchema()
                result=id_schema.load(par)
            except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
            if not  int(id)<=len(Course.query.all()) :
                return "Ovaj kurs ne postoji!!!!"
            course_schema=CourseSchema()
            result = course_schema.load(body)
            stari=Course.query.get(id)
            stari_s=course_schema.dump(stari)
            if stari.teacher_id!=current_user.id:
                return 'Nemate dozvolu da updejtujete tudj predmet!'
            ime= stari.name
            body=request.get_json()
            name=body['name']
            stari.name=name
            db.session.commit()
            stari_n=course_schema.dump(stari)
            if stari_n!=stari_s:
                return jsonify({"Prethodno stanje":stari_s,"Izmenjeno stanje":stari_n})
            return "Niste napravili nikakvu izmenu!"
        except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
    return "Nemate pravo pristupa ovoj stranici!"

@app.route('/delete_course/<id>',methods=['DELETE'])
@jwt_required()
def delete_course(id):
    id_c= get_jwt_identity()
    current_user=User.query.get(id_c)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            try:
                par={"id":id}
                id_schema=IdSchema()
                result=id_schema.load(par)
            except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
            #if not int(id)<=len(Course.query.all()):
#            course_schema=CourseSchema()
            kurs=Course.query.get(id)
            course_schema=CourseSchema()
            kurs_s=course_schema.dump(kurs)
            #if kurs.teacher_id!=current_user.id:
        #        return "Nemate dozvolu da brisete tudj predmet!"
                #izbrisi sve studente sa ovog kursa iz tabele ACTIVE
            db.session.delete(kurs)
            db.session.commit()
            return jsonify({"Kurs koji ste izbrisali je":kurs_s})
        except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/add_student',methods=['POST'])
@jwt_required()
def add_student():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            add_student_schema= AddStudentSchema()
            result= add_student_schema.load(body)
            course_id=body['course_id']
            user_id=body['user_id']
            if user_id>len(User.query.all()):
                return "Ne mozete dodati ucenika koji ne postoji!"
            kurs= Course.query.filter_by(id=course_id).first()
            user= User.query.filter_by(id=user_id).first()
            user_schema=UserSchema()
            if user!=current_user:
                if not user in kurs.users:
                    akt=Active(is_active=True, course_id=kurs.id,\
                     user_id=user.id)
                    kurs.users.append(user)
                    db.session.add(akt)
                    db.session.commit()
                    user=user_schema.dump(user)
                    return ({"Uspesno ste dodali novog studenta":user})
                return "Ne mozete dodati istog studenta vise puta!"
            return "Ne mozete dodati sebe na kurs!"
        except ValidationError as err:
                return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/aktivni',methods=['GET'])
@jwt_required()
def aktivni():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            aktivni_schema=AktivniSchema()
            body=request.get_json()
            result=aktivni_schema.load(body)
            course_id=body['course_id']
            if not course_id<=len(Course.query.all()):
                return "Ovaj kurs ne postoji!"
            kurs=Course.query.filter_by(id=course_id).first()
            ucenici=[]
            akt= Active.query.filter_by(course_id=course_id).\
            filter_by(is_active=True).all()
            for x in akt:
                if x.user_id!=current_user.id:
                    ucenici.append(User.query.filter_by(id=x.user_id).first())
            user_schema=UserSchema(many=True)
            ucenici=user_schema.dump(ucenici)
            return jsonify({"Moji aktivni studenti su": ucenici})
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/neaktivni',methods=['GET'])
@jwt_required()
def neaktivni():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            aktivni_schema=AktivniSchema()
            result=aktivni_schema.load(body)
            course_id=body['course_id']
            if not course_id<=len(Course.query.all()):
                return "Ovaj kurs ne postoji!"
            kurs=Course.query.filter_by(id=course_id).first()
            ucenici=[]
            neakt= Active.query.filter_by(course_id=course_id).\
            filter_by(is_active=False).all()
            for x in neakt:
                if x.user_id!=current_user.id:
                    ucenici.append(User.query.filter_by(id=x.user_id).first())
            user_schema=UserSchema(many=True)
            ucenici=user_schema.dump(ucenici)
            return jsonify({"Moji neaktivni studenti su": ucenici})
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/promena_statusa',methods=['PUT'])
@jwt_required()
def promena_statusa():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            promeni_status_schema= PromeniStatusSchema()
            result=promeni_status_schema.load(body)
            user_id=body['user_id']
            course_id=body['course_id']
            if not user_id <= len(User.query.all()):
                return "Ovaj student ne postoji"
            if not course_id <= len(Course.query.all()):
                return "Ovaj kurs ne postoji"
            user=User.query.filter_by(id=user_id).first()
            akt=Active.query.filter_by(user_id=user_id).\
            filter_by(course_id=course_id).first()
            if akt.is_active==True:
                akt.is_active=False
                db.session.commit()
                user_schema=UserSchema()
                user=user_schema.dump(user)
                return jsonify({"Navedenom studentu je promenjen status iz\
                 aktivnog u neaktivan":user})
            else:
                return "Ovaj student je vec zavrsio kurs,\
                 i ne moze opet biti aktivan!"
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/student_courses',methods=['GET'])
@jwt_required()
def student_courses():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    course_schema=CourseSchema(many=True)
    lista=course_schema.dump(current_user.courses)
    return jsonify({"Svi moji kursevi su ":lista})

@app.route('/not_student_courses',methods=['GET'])
@jwt_required()
def not_student_courses():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    course_schema=CourseSchema(many=True)
    lista=[]
    for x in Course.query.all():
        if x not in current_user.courses:
            lista.append(x)
    lista=course_schema.dump(lista)
    return jsonify({"Svi kursevi koje ne pohadjam su":lista})

@app.route('/oceni', methods=['POST'])
@jwt_required()
def oceni():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        oceni_schema=OceniSchema()
        result=oceni_schema.load(body)
        course_id=body['course_id']
        ocena=body['ocena']
        if not course_id <= len(Course.query.all()):
            return "Ovaj kurs ne postoji"
        course=Course.query.filter_by(id=course_id).first()
        aktiv=Active.query.filter_by(course_id=course_id).\
        filter_by(user_id=current_user.id).first()
        if aktiv != None:
            if aktiv.is_active == False:
                if ocena >=1 and ocena <=5:
                    rate=Rate(ocena=ocena, course_id=course.id,
                     user_id=current_user.id)
                    db.session.add(rate)
                    db.session.commit()
                    course_schema=CourseSchema()
                    course=course_schema.dump(course)
                    return jsonify({"Vase ocenjivanje": course})
                return 'Ocena mora biti izmedju 1 i 5!'
            return 'Ne mozete oceniti kurs koji jos uvek pohadjate!'
        return 'Ne mozete oceniti kurs koji niste ni upisali!'
    except ValidationError as err:
        return jsonify(err.messages,err.valid_data)

@app.route('/sve_ocene',methods=['GET'])
def sve_ocene():
    sve= Rate.query.all()
    rate_schema=RateSchema(many=True)
    sve=rate_schema.dump(sve)
    return jsonify({"Sve ocene":sve})

@app.route('/pos_zahtev',methods=['POST'])
@jwt_required()
def pos_zahtev():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    try:
        body=request.get_json()
        course_id_schema=CourseIdSchema()
        result=course_id_schema.load(body)
        zahtev= Zahtev(course_id=body['course_id'], user_id=current_user.id)
        if zahtev.course_id<= len(Course.query.all()):
            moji=Zahtev.query.filter_by(user_id=current_user.id).\
            filter_by(course_id=body['course_id']).all()
        else:
            return "Ovaj kurs ne postoji!"
        if len(moji)==0:
            db.session.add(zahtev)
            db.session.commit()
            zahtev_schema=ZahtevSchema()
            poslat=zahtev_schema.dump(zahtev)
            return jsonify({f"Vas zahtev za je uspesno poslat!": poslat})
        elif moji[len(moji)-1].prihvacen=="da":
            return "Vas prethodni zahtev je prihvacen!"
        elif moji[len(moji)-1].prihvacen=="ne":
            db.session.add(zahtev)
            db.session.commit()
            return "Vas prethodni zahtev je odbijen!"
        else:
            return "Vas prethodni zahtev je na cekanju!"
    except ValidationError as err:
        return jsonify(err.messages,err.valid_data)

@app.route('/prist_zaht',methods=['GET'])
@jwt_required()
def prist_zaht():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            course_id_schema=CourseIdSchema()
            result=course_id_schema.load(body)
            course_id=body['course_id']
            kurs= Course.query.get(course_id)
            if course_id<= len(Course.query.all()) and\
                kurs.teacher_id==current_user.id:
                stigli = Zahtev.query.filter_by(course_id=course_id)\
                .filter_by(prihvacen="cekanje").all()
                if len(stigli)>0:
                    zahtev_schema=ZahtevSchema(many=True)
                    stigli=zahtev_schema.dump(stigli)
                    return jsonify({"Pristigli zahtevi": stigli})
                else:
                    return "Nemate pristiglih zahteva!"
            return "Ne mozete proveriti zahteve za kurs\
                    koji ne postoji ili nije vas!"
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"

@app.route('/prih_zaht',methods=['POST'])
@jwt_required()
def prih_zaht():
    id= get_jwt_identity()
    current_user=User.query.get(id)
    if current_user.role_id==1 or current_user.role_id==3:
        try:
            body=request.get_json()
            prih_zaht_schema=PrihZahtSchema()
            result= prih_zaht_schema.load(body)
            course_id=body['course_id']
            user_id=body['user_id']
            prihvacen=body['prihvacen']
            user_schema=UserSchema()
            kurs= Course.query.get(course_id)
            if course_id<= len(Course.query.all()) and \
            kurs.teacher_id==current_user.id and\
            user_id<=len(User.query.all()):
                zahtevi=Zahtev.query.filter_by(course_id=course_id)\
                .filter_by(prihvacen="cekanje")\
                .filter_by(user_id=user_id).all()
                user=User.query.get(user_id)
                user=user_schema.dump(user)
                if prihvacen=="da" and len(zahtevi)!=0:
                    zahtevi[-1].prihvacen="da"
                    akt=Active(is_active=True, user_id=user_id,\
                     course_id=course_id)
                    db.session.add(akt)
                    User.query.get(user_id).courses.append(kurs)
                    db.session.commit()
                    return ({"Uspesno ste prihvatili studenta":user})
                elif prihvacen=="ne" and len(zahtevi)!=0:
                    zahtevi[-1].prihvacen="ne"
                    db.session.commit()
                    return ({"Odbili ste studenta":user})
                elif  len(zahtevi)!=0:
                    return ({"Student je i dalje na cekanju!":user})
                else:
                    return "Student kojeg ste izabrali vam nije poslao zahtev!"
            return "Ne mozete prihvatiti studenta koji ne postoji \
                    ili predmet koji ne postoji!"
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
    return "Nemate pristup ovoj stranici!"



@app.route('/search_by_first_name',methods=['GET'])
def search_by_first_name():
        try:
            body=request.get_json()
            name_schema=NameSchema()
            result= name_schema.load(body)
            first_name=body['name']
            svi=User.query.filter(User.first_name.like(f"%{first_name}%")).all()


            user_schema=UserSchema(many=True)
            svi=user_schema.dump(svi)
            return jsonify({"Pretraga po imenu":svi})
        except ValidationError as err:
            return jsonify(err.messages,err.valid_data)
