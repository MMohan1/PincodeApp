from mongoengine import *
# from elasticsearch_dsl import DocType, String, Date, Integer, Nested, Mapping, Boolean, Long, GeoPoint
# from elasticsearch_dsl.connections import connections
# from hirenew import hireconfig
import datetime

connect('pincode')
connections.create_connection(hosts=['localhost'])


class Data(Document):
    officename = StringField(required=True)
    pincode = IntField(required=True, unique=True, primary_key=True))
        officeType=StringField(required = True)
        Deliverystatus=StringField(required = True)
        divisionname=StringField(required = True)
        regionname=StringField(required = True)
        circlename=StringField(required = True)
        Taluk=StringField(required = True)
        Districtname=StringField(required = True)
        statename=StringField(required = True)
        meta={
        'indexes':
            ['pincode']
    }
