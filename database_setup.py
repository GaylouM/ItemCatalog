import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class Frame(Base):
    __tablename__ = 'frame'

    id = Column(Integer, primary_key=True)
    client_lastname = Column(String(250))
    client_firstname = Column(String(250))
    client_full_adress = Column(String(250))
    client_adress_number = Column(String(250))
    client_adress_street = Column(String(250))
    client_adress_city = Column(String(250))
    client_administrative_area = Column(String(250))
    client_adress_postcode = Column(String(10))
    client_adress_country = Column(String(250))
    client_phone = Column(String(10))
    client_mail = Column(String(250))
    editor_lastname = Column(String(250))
    editor_firstname = Column(String(250))
    editor_full_adress = Column(String(250))
    editor_adress_number = Column(String(250))
    editor_adress_street = Column(String(250))
    editor_adress_city = Column(String(250))
    editor_administrative_area = Column(String(250))
    editor_adress_postcode = Column(String(10))
    editor_adress_country = Column(String(250))
    editor_phone = Column(String(10))
    editor_mail = Column(String(250))
    reports = relationship("Report", cascade="all, delete-orphan")

    
    @property
    def serialize(self):

        return {
            'id': self.id,
            'client_firstname': self.client_firstname,
            'client_lastname': self.client_lastname,
            'client_full_adress': self.client_full_adress,
            'client_phone': self.client_phone,
            'client_mail': self.client_mail,
            'editor_firstname': self.editor_firstname,
            'editor_lastname': self.editor_lastname,
            'editor_full_adress': self.editor_full_adress,
            'editor_phone': self.editor_phone,
            'editor_mail': self.editor_mail,
        }


class Report(Base):
    __tablename__ = 'report'
    
    id = Column(Integer, primary_key=True)
    site_name = Column(String(250))
    site_full_adress = Column(String(250))
    site_adress_number = Column(String(250))
    site_adress_street = Column(String(250))
    site_adress_postcode = Column(String(10))
    site_adress_city = Column(String(250))
    site_administrative_area = Column(String(250))
    site_adress_country = Column(String(250))
    site_ERPcategory = Column(String(10))
    site_ERPtype = Column(String(10))
    client_lastname = Column(String(250))
    client_firstname = Column(String(250))
    client_full_adress = Column(String(250))
    client_adress_number = Column(String(250))
    client_adress_street = Column(String(250))
    client_adress_postcode = Column(String(10))
    client_adress_city = Column(String(250))
    client_administrative_area = Column(String(250))
    client_adress_country = Column(String(250))
    client_phone = Column(String(10))
    client_mail = Column(String(250))
    report_number = Column(Integer)
    report_visitDate = Column(String(10))
    report_redactionDate = Column(String(10))
    report_picture = Column(String(250))
    report_pictureOrientation = Column(String(10))
    editor_lastname = Column(String(250))
    editor_firstname = Column(String(250))
    editor_full_adress = Column(String(250))
    editor_adress_number = Column(String(250))
    editor_adress_street = Column(String(250))
    editor_adress_postcode = Column(String(10))
    editor_adress_city = Column(String(250))
    editor_administrative_area = Column(String(250))
    editor_adress_country = Column(String(250))
    editor_phone = Column(String(10))
    editor_mail = Column(String(250))
    frame_choice = Column(Integer, ForeignKey('frame.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(Frame)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'client_firstname': self.client_firstname,
            'client_lastname': self.client_lastname,
            'client_full_adress': self.client_full_adress,
            'client_phone': self.client_phone,
            'client_mail': self.client_mail,
            'editor_firstname': self.editor_firstname,
            'editor_lastname': self.editor_lastname,
            'editor_full_adress': self.editor_full_adress,
            'editor_phone': self.editor_phone,
            'editor_mail': self.editor_mail,
            'site_name': self.site_name,
            'site_full_adress': self.site_full_adress,
            'site_ERPcategory': self.site_ERPcategory,
            'site_ERPtype': self.site_ERPtype,
            'report_number': self.report_number,
            'report_visitDate': self.report_visitDate,
            'report_redactionDate': self.report_redactionDate,
            'report_picture': self.report_picture,
            'report_pictureOrientation': self.report_pictureOrientation,
        }

#engine = create_engine('sqlite:///affairreport.db')

engine = create_engine('sqlite:///affairreportwithusers.db')


Base.metadata.create_all(engine)