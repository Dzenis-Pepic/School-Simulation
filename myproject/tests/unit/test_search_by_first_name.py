import unittest
from flask import jsonify, request
import requests,json
from myproject.__init__ import app,db
from  myproject.models import *
from myproject.schemas import *


class TestAllCourses(unittest.TestCase):




    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/search_by_first_name"
        self.body={
                "name":"teacher2"
            }
        self.izlaz= {
            "Pretraga po imenu": [
                {
                    "email": "teacher2@gmail.com",
                    "first_name": "teacher2",
                    "last_name": "pteacher2",
                    "password": "sifra",
                    "role_id": 1
                }
            ]
        }




    def test_search_by_first_name(self):
        resp=requests.get(self.url, json=self.body)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), self.izlaz)












if __name__=='__main__':
    unittest.main()
