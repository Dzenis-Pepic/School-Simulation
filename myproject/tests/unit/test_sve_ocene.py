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
        self.url="http://127.0.0.1:5000/sve_ocene"
        self.izlaz={
            "Sve ocene": []
    }


    def test_course_all(self):
        resp=requests.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(resp.json(), self.izlaz)







if __name__=='__main__':
    unittest.main()
