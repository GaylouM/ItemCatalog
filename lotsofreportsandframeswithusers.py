# coding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Frame, Base, Report, User

engine = create_engine('postgresql://catalog:db-password@localhost/catalog')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

User1 = User(name="Robo Barista", email="tinnyTim@udacity.com", picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

frame = Frame(client_lastname=u'%s' % "MARVILLE", client_firstname=u'%s' % "Gaylord", client_full_adress=u'%s' % "48 rue Raffet, 75016, Paris", client_phone=u'%s' % "06 59 49 78 02", client_mail=u'%s' % "gaylord.marville@gmail.com", editor_lastname=u'%s' % "BAI", editor_firstname=u'%s' % "David", editor_full_adress=u'%s' % "Viry-Chatillon, France", editor_phone=u'%s' % "06 72 27 58 10", editor_mail=u'%s' % "david.bai@hotmail.fr")
session.add(frame)
session.commit()

report = Report(user_id=1, site_name=u'%s' % "Le traiteur du theatre", site_full_adress=u'%s' % "99 rue du theatre , Paris, France", site_adress_number=u'%s' % "99", site_adress_street=u'%s' % "rue du theatre ", site_adress_postcode=u'%s' % "75015", site_adress_city=u'%s' % "Paris", site_administrative_area=u'%s' % "Ile-de-France", site_adress_country=u'%s' % "France", site_ERPcategory=u'%s' % "5", site_ERPtype=u'%s' % "N", client_lastname=u'%s' % "non available", client_firstname=u'%s' % "non available", client_full_adress=u'%s' % "non available", client_adress_number=u'%s' % "non available", client_adress_street=u'%s' % "non available", client_adress_city=u'%s' % "non available", client_adress_postcode=u'%s' % "non available", client_administrative_area=u'%s' % "Ile-de-France", client_adress_country=u'%s' % "France", client_phone=u'%s' % "01 45 75 30 90", client_mail=u'%s' % "non available", report_number='%d' % 6253212, report_visitDate=u'%s' % "2015-08-10", report_redactionDate=u'%s' % "non available", report_picture=u'%s' % "20150810_193845.jpg", report_pictureOrientation=u'%s' % "Rotated 90 CW", editor_lastname=u'%s' % "MARVILLE", editor_firstname=u'%s' % "Gaylord", editor_full_adress=u'%s' % "48 rue Raffet, Paris, France", editor_adress_number=u'%s' % "48", editor_adress_street=u'%s' % "rue Raffet", editor_adress_postcode=u'%s' % "75016", editor_adress_city=u'%s' % "Paris", editor_administrative_area=u'%s' % "Ile-de-France", editor_adress_country=u'%s' % "France", editor_phone=u'%s' % "01 45 25 41 94", editor_mail=u'%s' % "gaylord.marville@gmail.com", frame_choice='%d' % 0)
session.add(report)
session.commit()
report = Report(user_id=1, site_name=u'%s' % "Le Chiquito", site_full_adress=u'%s' % "5 rue des Bas Rogers, Paris, France", site_adress_number=u'%s' % "5", site_adress_street=u'%s' % "rue des Bas Rogers", site_adress_postcode=u'%s' % "92073", site_adress_city=u'%s' % "Suresnes", site_administrative_area=u'%s' % "Ile-de-France", site_adress_country=u'%s' % "France", site_ERPcategory=u'%s' % "5", site_ERPtype=u'%s' % "N", client_lastname=u'%s' % "non available", client_firstname=u'%s' % "non available", client_full_adress=u'%s' % "non available", client_adress_number=u'%s' % "non available", client_adress_street=u'%s' % "non available", client_adress_city=u'%s' % "non available", client_adress_postcode=u'%s' % "non available", client_administrative_area=u'%s' % "Ile-de-France", client_adress_country=u'%s' % "France", client_phone=u'%s' % "01 45 06 11 31", client_mail=u'%s' % "non available", report_number='%d' % 6253213, report_visitDate=u'%s' % "2015-08-11", report_redactionDate=u'%s' % "non available", report_picture=u'%s' % "IMG_3185.JPG", report_pictureOrientation=u'%s' % "non available", editor_lastname=u'%s' % "MARVILLE", editor_firstname=u'%s' % "Gaylord", editor_full_adress=u'%s' % "48 rue Raffet, Paris, France", editor_adress_number=u'%s' % "48", editor_adress_street=u'%s' % "rue Raffet", editor_adress_postcode=u'%s' % "75016", editor_adress_city=u'%s' % "Paris", editor_administrative_area=u'%s' % "Ile-de-France", editor_adress_country=u'%s' % "France", editor_phone=u'%s' % "01 45 25 41 94", editor_mail=u'%s' % "gaylord.marville@gmail.com", frame_choice='%d' % 0)
session.add(report)
session.commit()
report = Report(user_id=1, site_name=u'%s' % "Yanagawa", site_full_adress=u'%s' % "46 rue de villiers, Paris, France", site_adress_number=u'%s' % "46", site_adress_street=u'%s' % "rue de villiers ", site_adress_postcode=u'%s' % "92300", site_adress_city=u'%s' % "Levallois-Perret", site_administrative_area=u'%s' % "Ile-de-France", site_adress_country=u'%s' % "France", site_ERPcategory=u'%s' % "5", site_ERPtype=u'%s' % "N", client_lastname=u'%s' % "non available", client_firstname=u'%s' % "non available", client_full_adress=u'%s' % "non available", client_adress_number=u'%s' % "non available", client_adress_street=u'%s' % "non available", client_adress_city=u'%s' % "non available", client_adress_postcode=u'%s' % "non available", client_administrative_area=u'%s' % "Ile-de-France", client_adress_country=u'%s' % "France", client_phone=u'%s' % "06 29 97 42 05 ", client_mail=u'%s' % "non available", report_number='%d' % 6253214, report_visitDate=u'%s' % "2015-09-01", report_redactionDate=u'%s' % "non available", report_picture=u'%s' % "IMG_3910.JPG", report_pictureOrientation=u'%s' % "non available", editor_lastname=u'%s' % "MARVILLE", editor_firstname=u'%s' % "Gaylord", editor_full_adress=u'%s' % "48 rue Raffet, Paris, France", editor_adress_number=u'%s' % "48", editor_adress_street=u'%s' % "rue Raffet", editor_adress_postcode=u'%s' % "75016", editor_adress_city=u'%s' % "Paris", editor_administrative_area=u'%s' % "Ile-de-France", editor_adress_country=u'%s' % "France", editor_phone=u'%s' % "01 45 25 41 94", editor_mail=u'%s' % "gaylord.marville@gmail.com", frame_choice='%d' % 0)
session.add(report)
session.commit()

print "report added !"
