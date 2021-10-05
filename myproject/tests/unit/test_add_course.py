import unittest
from flask import jsonify, request
import requests,json
from myproject.__init__ import app,db
from  myproject.models import *
from myproject.schemas import *
from flask import session
from flask import jsonify, request, make_response, Response
import requests,json
import jwt
import datetime
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


class TestAddCourse(unittest.TestCase):




    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/add_course"
        self.body= {
        "name":"algebra"
        }
        self.izlaz={
            "Uspesno ste dodali kurs": {
                "name": "algebra",
                "teacher_id": 1
            }
        }

    @jwt_required()
    def test_add_course(self):
        resp=requests.post(self.url, json=self.body)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json().self.izlaz)








if __name__=='__main__':
    unittest.main()
