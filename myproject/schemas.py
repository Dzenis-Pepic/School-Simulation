from marshmallow import Schema, fields, post_load,\
 ValidationError, validates, validate

class UserSchema(Schema):
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    role_id=fields.Integer(required=True)

class LoginSchema(Schema):
    password = fields.String(required=True)
    email = fields.Email(required=True)


class CourseSchema(Schema):
    name=fields.String(required=True)
    teacher_id=fields.Integer()

class AddCourseSchema(Schema):
    name=fields.String(required=True)



class RateSchema(Schema):
    ocena=fields.Integer(required=True)
    course_id=fields.Integer(required=True)
    user_id=fields.Integer(required=True)

    @validates('ocena')
    def validate_role_id(self,ocena):
        if ocena>5:
            raise ValidationError("Ocena ne smije biti veca od 5!")
class IdSchema(Schema):
    id=fields.Integer(required=True)

class NameSchema(Schema):
    name=fields.String(required=True)

class URLSchema(NameSchema):
    pass

class AddStudentSchema(Schema):
    user_id=fields.Integer(required=True)
    course_id=fields.Integer(required=True)

class AktivniSchema(Schema):
    course_id=fields.Integer(required=True)

class PromeniStatusSchema(AddStudentSchema):
    pass

class OceniSchema(Schema):
    ocena=fields.Integer(required=True)
    course_id=fields.Integer(required=True)

class CourseIdSchema(AktivniSchema):
    pass

class PrihZahtSchema(Schema):
    user_id=fields.Integer(required=True)
    course_id=fields.Integer(required=True)
    prihvacen=fields.String(required=True)

    @validates('prihvacen')
    def validate_role_id(self,prihvacen):
        lista=["da","ne","cekanje"]
        if prihvacen not in lista:
            raise ValidationError("Mozete upisati samo >da<,>ne< ili >cekanje<")

class ActiveSchema(Schema):

    is_active=fields.Boolean(required=True)
    course_id=fields.Integer(required=True)
    user_id=fields.Integer(required=True)

class ZahtevSchema(Schema):
    course_id=fields.Integer(required=True)
    user_id=fields.Integer(required=True)
    prihvacen=fields.String(required=True)
