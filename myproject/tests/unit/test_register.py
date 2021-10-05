import unittest
from flask import jsonify, request
import requests,json
from myproject.__init__ import app,db
from  myproject.models import *
from myproject.schemas import *


class TestRegister(unittest.TestCase):




    @classmethod
    def tearDownClass(cls):
        print('teardownClass')

    def setUp(self):
        print('setUp')
        self.url="http://127.0.0.1:5000/register"
        self.body={
            "first_name":"teacher1001",
            "last_name":"pteacher1001",
            "email":"teacher1001@gmail.com",
            "password":"sifra",
            "role_id": 1}
        self.izlaz={
            "Uspesno ste registrovali nastavnika!": {
                "email": "teacher1001@gmail.com",
                "first_name": "teacher1001",
                "last_name": "pteacher1001",
                "password": "sifra",
                "role_id": 1
            }
    }


    def test_register(self):
        resp=requests.post(self.url, json=self.body)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.izlaz)







if __name__=='__main__':
    unittest.main()
