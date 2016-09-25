import os
import sys
import exifread
from functools import wraps
from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash, send_from_directory
from database_setup import Base, User, Frame, Report
from werkzeug import secure_filename
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
import random
import string
# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True

upload_folder = '/var/www/ItemCatalog/static/uploads/'

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = '/var/www/ItemCatalog/static/uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(
    ['png', 'jpg', 'JPG', 'jpeg'])
# The size of the uploaded files is limited to 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

CLIENT_ID = json.loads(
    open('var/www/ItemCatalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Report creator"

engine = create_engine('postgresql://catalog:db-password@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/ajax', methods=['POST'])
def ajax():
    """This function is reach from the Ajax code
    linked to the files editsinglereport.html and
    createsingereport.html to return data from the database
    """
    # Validate state token
    state = request.data
    if state:
        frame = session.query(Frame).filter_by(id=state).one()
        return jsonify(frame=frame.serialize)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in login_session:
            flash("You are not allowed to access there")
            return redirect(url_for('showLogin', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


#--------------------------------------------------------
#--------------------Manage login------------------------
#--------------------------------------------------------


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, user=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('var/www/ItemCatalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session['access_token']
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401
            )
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash('Successfully disconnected.')
        return redirect(url_for('showAllReports'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400)
            )
        response.headers['Content-Type'] = 'application/json'
        return response


#--------------------------------------------------------
#--------------------Manage upload-----------------------
#--------------------------------------------------------


def uploads(uploaded_files):
    """Save the picture in the UPLOAD_FOLDER
    and return its filename and metadatas with exifread
    """
    filenames = []
    valueX = []
    valueXInter = []
    meta = {}
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Open image file for reading (binary mode)
            f = open("%s%s" % (upload_folder, filename), 'rb')

            # Read Exif tags
            tags = exifread.process_file(f, details=False, strict=True)
            valueXInter.append([])
            # Loop on the tags
            for tag in tags.keys():
                # Stop and save the value if true
                if tag in (
                    'EXIF DateTimeOriginal',
                    'Image Orientation',
                    'GPS GPSAltitude',
                    'GPS GPSLongitude',
                    'GPS GPSLatitudeRef',
                    'GPS GPSLatitude'
                ):
                    valueXInter[0].append(str(tags[tag]))
                    # Save the filename into a dictionnary, we'll use it later
                    meta[str(tag)] = str(tags[tag])
            valueX.append(valueXInter.pop())
            filenames.append(filename)
    return meta, filename


#--------------------------------------------------------
#--------------------Manage users------------------------
#--------------------------------------------------------


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


#--------------------------------------------------------
#--------------------Manage frames-----------------------
#--------------------------------------------------------


@app.route('/frames/')
def showAllFrames():
    frames = session.query(Frame)
    return render_template('frames.html', frames=frames, user=login_session)


@app.route('/frames/JSON', methods=['GET', 'POST'])
def showAllFramesJSON():
    frames = session.query(Frame)
    return jsonify(FramesList=[i.serialize for i in frames])


@app.route('/frames/<int:frame_id>')
@app.route('/frames/<int:frame_id>/frame')
def showSingleFrame(frame_id):
    frame = session.query(Frame).filter_by(id=frame_id).one()
    return render_template('showsingleframe.html',
                           frame=frame,
                           user=login_session)


@app.route('/frames/<int:frame_id>/JSON')
@app.route('/frames/<int:frame_id>/frame/JSON')
def showSingleFrameJSON(frame_id):
    frame = session.query(Frame).filter_by(id=frame_id).one()
    return jsonify(SingleFrame=frame.serialize)


@app.route('/frames/new', methods=['GET', 'POST'])
@login_required
def newSingleFrame():
    if request.method == 'POST':
        newFrame = Frame(client_lastname=request.form['client_firstname'],
                         client_firstname=request.form['client_lastname'],
                         client_full_adress=request.form['client_full_adress'],
                         client_phone=request.form['client_phone'],
                         client_mail=request.form['client_mail'],
                         editor_lastname=request.form['editor_lastname'],
                         editor_firstname=request.form['editor_firstname'],
                         editor_full_adress=request.form['editor_full_adress'],
                         editor_phone=request.form['editor_phone'],
                         editor_mail=request.form['editor_mail'])
        session.add(newFrame)
        session.commit()
        flash("new frame created !")
        return redirect(url_for('showAllFrames'))

    return render_template('createsingleframe.html', user=login_session)


@app.route('/frames/<int:frame_id>/edit', methods=['GET', 'POST'])
@login_required
def editSingleFrame(frame_id):
    editedFrame = session.query(Frame).filter_by(id=frame_id).one()
    if request.method == 'POST':
        if request.form['client_lastname']:
            editedFrame.client_lastname = request.form['client_lastname']
        if request.form['client_firstname']:
            editedFrame.client_firstname = request.form['client_firstname']
        if request.form['client_full_adress']:
            editedFrame.client_full_adress = request.form['client_full_adress']
        if request.form['client_phone']:
            editedFrame.client_phone = request.form['client_phone']
        if request.form['client_mail']:
            editedFrame.client_mail = request.form['client_mail']
        if request.form['editor_lastname']:
            editedFrame.editor_lastname = request.form['editor_lastname']
        if request.form['editor_firstname']:
            editedFrame.editor_firstname = request.form['editor_firstname']
        if request.form['editor_full_adress']:
            editedFrame.editor_full_adress = request.form['editor_full_adress']
        if request.form['editor_phone']:
            editedFrame.editor_phone = request.form['editor_phone']
        if request.form['editor_mail']:
            editedFrame.editor_mail = request.form['editor_mail']
        session.add(editedFrame)
        session.commit()
        flash("frame was edited !")
        return redirect(url_for('showAllFrames'))

    frame = session.query(Frame).filter_by(id=frame_id).one()
    return render_template('editsingleframe.html',
                           frame=frame,
                           user=login_session)


@app.route('/frames/<int:frame_id>/delete', methods=['GET', 'POST'])
@login_required
def deleteSingleFrame(frame_id):
    frameToDelete = session.query(Frame).filter_by(id=frame_id).one()
    if request.method == 'POST':
        session.delete(frameToDelete)
        session.commit()
        flash("frame was deleted !")
        return redirect(url_for('showAllFrames'))

    frame = session.query(Frame).filter_by(id=frame_id).one()
    return render_template('deletesingleframe.html',
                           frame=frame,
                           user=login_session)


#--------------------------------------------------------
#--------------------Manage reports----------------------
#--------------------------------------------------------


@app.route('/')
@app.route('/reports/', methods=['GET', 'POST'])
def showAllReports():
    reports = session.query(Report)
    frames = session.query(Frame)
    return render_template('reports.html',
                           reports=reports,
                           frames=frames,
                           user=login_session,
                           customised=reports)


@app.route('/reports/JSON', methods=['GET', 'POST'])
def showAllReportsJSON():
    reports = session.query(Report)
    return jsonify(ReportsList=[i.serialize for i in reports])


@app.route('/reports/<int:report_id>')
@app.route('/reports/<int:report_id>/report')
def showSingleReport(report_id):
    report = session.query(Report).filter_by(id=report_id).one()
    if report.frame_choice:
        frame = session.query(Frame).filter_by(id=report.frame_choice).one()
        return render_template('showsinglereport.html',
                               report=frame,
                               report_id=report_id,
                               user=login_session,
                               customised=report,
                               userReportInfos=getUserInfo(report.user_id))
    else:
        return render_template('showsinglereport.html',
                               report=report,
                               report_id=report_id,
                               user=login_session,
                               customised=report,
                               userReportInfos=getUserInfo(report.user_id))


@app.route('/reports/<int:report_id>/JSON')
@app.route('/reports/<int:report_id>/report/JSON')
def showSingleReportJSON(report_id):
    report = session.query(Report).filter_by(id=report_id).one()
    if report.frame_choice is not 0:
        frame = session.query(Frame).filter_by(id=report.frame_choice).one()
        return jsonify(SingleReport=frame.serialize)
    else:
        return jsonify(SingleReport=report.serialize)


@app.route('/reports/new', methods=['GET', 'POST'])
@login_required
def newSingleReport():
    if request.method == 'POST':
        if request.form['frame'] == "Customised":
            if request.files.getlist('file[]')[0].filename != "":
                uploaded_files = request.files.getlist('file[]')
                meta, filename = uploads(uploaded_files)
                choosenPicture = filename
                meta_orientation = meta['Image Orientation']
            else:
                choosenPicture = "undefined.jpg"
                meta_orientation = "None"
            newReport = Report(
                client_firstname=request.form['client_firstname'],
                client_lastname=request.form['client_lastname'],
                client_full_adress=request.form['client_full_adress'],
                client_adress_number=request.form['client_adress_number'],
                client_adress_street=request.form['client_adress_street'],
                client_adress_postcode=request.form['client_adress_postcode'],
                client_adress_city=request.form['client_adress_city'],
                client_administrative_area=request.form[
                    'client_administrative_area'],
                client_adress_country=request.form['client_adress_country'],
                client_phone=request.form['client_phone'],
                client_mail=request.form['client_mail'],
                editor_firstname=request.form['editor_firstname'],
                editor_lastname=request.form['editor_lastname'],
                editor_full_adress=request.form['editor_full_adress'],
                editor_adress_number=request.form['editor_adress_number'],
                editor_adress_street=request.form['editor_adress_street'],
                editor_adress_postcode=request.form['editor_adress_postcode'],
                editor_adress_city=request.form['editor_adress_city'],
                editor_administrative_area=request.form[
                    'editor_administrative_area'],
                editor_adress_country=request.form['editor_adress_country'],
                editor_phone=request.form['editor_phone'],
                editor_mail=request.form['editor_mail'],
                site_name=request.form['site_name'],
                site_full_adress=request.form['site_full_adress'],
                site_adress_number=request.form['site_adress_number'],
                site_adress_street=request.form['site_adress_street'],
                site_adress_postcode=request.form['site_adress_postcode'],
                site_adress_city=request.form['site_adress_city'],
                site_administrative_area=request.form[
                    'site_administrative_area'],
                site_adress_country=request.form['site_adress_country'],
                site_ERPcategory=request.form['site_ERPcategory'],
                site_ERPtype=request.form['site_ERPtype'],
                report_number=request.form['report_number'],
                report_visitDate=request.form['report_visitDate'],
                report_redactionDate=request.form['report_redactionDate'],
                report_picture=choosenPicture,
                report_pictureOrientation=meta_orientation,
                user_id=login_session['user_id']
            )
            session.add(newReport)
            session.commit()
            flash("new report(s) created !")
            return redirect(url_for('showAllReports'))
        else:
            targetFrame = session.query(Frame).filter_by(
                id=request.form['frame']).one()
            numRapp = int(str(request.form['nombre']))
            while numRapp != 0:
                newReport = Report(
                    frame_choice=targetFrame.id,
                    user_id=login_session['user_id'],
                    report_picture="undefined.jpg"
                )
                numRapp -= 1
                session.add(newReport)
                session.commit()
                flash("new report(s) created !")
            return redirect(url_for('showAllReports'))
    frames = session.query(Frame)
    return render_template('createsinglereport.html',
                           frames=frames,
                           user=login_session)


@app.route('/reports/<int:report_id>/edit', methods=['GET', 'POST'])
@login_required
def editSingleReport(report_id):
    editedReport = session.query(Report).filter_by(id=report_id).one()
    frames = session.query(Frame)
    if request.method == 'POST':
        if request.form['frame'] == "Customised":
            if request.files.getlist('file[]')[0].filename != "":
                uploaded_files = request.files.getlist('file[]')
                meta, filename = uploads(uploaded_files)
                editedReport.report_picture = filename
                editedReport.report_pictureOrientation = meta[
                    'Image Orientation']
            if request.form['client_firstname']:
                editedReport.client_firstname = request.form[
                    'client_firstname']
            if request.form['client_lastname']:
                editedReport.client_lastname = request.form['client_lastname']
            if request.form['client_full_adress']:
                editedReport.client_full_adress = request.form[
                    'client_full_adress']
            if request.form['client_adress_number']:
                editedReport.client_adress_number = request.form[
                    'client_adress_number']
            if request.form['client_adress_street']:
                editedReport.client_adress_street = request.form[
                    'client_adress_street']
            if request.form['client_adress_city']:
                editedReport.client_adress_city = request.form[
                    'client_adress_city']
            if request.form['client_administrative_area']:
                editedReport.client_administrative_area = request.form[
                    'client_administrative_area']
            if request.form['client_adress_postcode']:
                editedReport.client_adress_postcode = request.form[
                    'client_adress_postcode']
            if request.form['client_adress_country']:
                editedReport.client_adress_country = request.form[
                    'client_adress_country']
            if request.form['client_phone']:
                editedReport.client_phone = request.form['client_phone']
            if request.form['client_mail']:
                editedReport.client_mail = request.form['client_mail']
            if request.form['editor_firstname']:
                editedReport.editor_firstname = request.form[
                    'editor_firstname']
            if request.form['editor_lastname']:
                editedReport.editor_lastname = request.form['editor_lastname']
            if request.form['editor_full_adress']:
                editedReport.editor_full_adress = request.form[
                    'editor_full_adress']
            if request.form['editor_adress_number']:
                editedReport.editor_adress_number = request.form[
                    'editor_adress_number']
            if request.form['editor_adress_street']:
                editedReport.editor_adress_street = request.form[
                    'editor_adress_street']
            if request.form['editor_adress_city']:
                editedReport.editor_adress_city = request.form[
                    'editor_adress_city']
            if request.form['editor_administrative_area']:
                editedReport.editor_administrative_area = request.form[
                    'editor_administrative_area']
            if request.form['editor_adress_postcode']:
                editedReport.editor_adress_postcode = request.form[
                    'editor_adress_postcode']
            if request.form['editor_adress_country']:
                editedReport.editor_adress_country = request.form[
                    'editor_adress_country']
            if request.form['editor_phone']:
                editedReport.editor_phone = request.form['editor_phone']
            if request.form['editor_mail']:
                editedReport.editor_mail = request.form['editor_mail']
            if request.form['site_name']:
                editedReport.site_name = request.form['site_name']
            if request.form['site_full_adress']:
                editedReport.site_full_adress = request.form[
                    'site_full_adress']
            if request.form['site_adress_number']:
                editedReport.site_adress_number = request.form[
                    'site_adress_number']
            if request.form['site_adress_street']:
                editedReport.site_adress_street = request.form[
                    'site_adress_street']
            if request.form['site_adress_postcode']:
                editedReport.site_adress_postcode = request.form[
                    'site_adress_postcode']
            if request.form['site_adress_city']:
                editedReport.site_adress_city = request.form[
                    'site_adress_city']
            if request.form['site_administrative_area']:
                editedReport.site_administrative_area = request.form[
                    'site_administrative_area']
            if request.form['site_adress_country']:
                editedReport.site_adress_country = request.form[
                    'site_adress_country']
            if request.form['site_ERPcategory']:
                editedReport.site_ERPcategory = request.form[
                    'site_ERPcategory']
            if request.form['site_ERPtype']:
                editedReport.site_ERPtype = request.form['site_ERPtype']
            if request.form['report_number']:
                editedReport.report_number = request.form['report_number']
            if request.form['report_visitDate']:
                editedReport.report_visitDate = request.form[
                    'report_visitDate']
            if request.form['report_redactionDate']:
                editedReport.report_redactionDate = request.form[
                    'report_redactionDate']
            editedReport.frame_choice = 0
            session.add(editedReport)
            session.commit()
            flash("report was edited !")
            return redirect(url_for('showAllReports'))
        else:
            targetFrame = session.query(Frame).filter_by(
                id=request.form['frame']).one()
            if request.files.getlist('file[]')[0].filename != "":
                uploaded_files = request.files.getlist('file[]')
                meta, filename = uploads(uploaded_files)
                editedReport.report_picture = filename
                editedReport.report_pictureOrientation = meta[
                    'Image Orientation']
            if request.form['site_name']:
                editedReport.site_name = request.form['site_name']
            if request.form['site_full_adress']:
                editedReport.site_full_adress = request.form[
                    'site_full_adress']
            if request.form['site_adress_number']:
                editedReport.site_adress_number = request.form[
                    'site_adress_number']
            if request.form['site_adress_street']:
                editedReport.site_adress_street = request.form[
                    'site_adress_street']
            if request.form['site_adress_postcode']:
                editedReport.site_adress_postcode = request.form[
                    'site_adress_postcode']
            if request.form['site_adress_city']:
                editedReport.site_adress_city = request.form[
                    'site_adress_city']
            if request.form['site_administrative_area']:
                editedReport.site_administrative_area = request.form[
                    'site_administrative_area']
            if request.form['site_adress_country']:
                editedReport.site_adress_country = request.form[
                    'site_adress_country']
            if request.form['site_ERPcategory']:
                editedReport.site_ERPcategory = request.form[
                    'site_ERPcategory']
            if request.form['site_ERPtype']:
                editedReport.site_ERPtype = request.form['site_ERPtype']
            if request.form['report_number']:
                editedReport.report_number = request.form['report_number']
            if request.form['report_visitDate']:
                editedReport.report_visitDate = request.form[
                    'report_visitDate']
            if request.form['report_redactionDate']:
                editedReport.report_redactionDate = request.form[
                    'report_redactionDate']
            editedReport.frame_choice = targetFrame.id
            session.add(editedReport)
            session.commit()
            flash("report was edited !")
            return redirect(url_for('showAllReports'))

    if editedReport.frame_choice is not 0:
        frame = session.query(Frame).filter_by(
            id=editedReport.frame_choice).one()
        return render_template('editsinglereport.html',
                               report=frame,
                               frames=frames,
                               report_id=report_id,
                               frame_choice=editedReport.frame_choice,
                               customised=editedReport,
                               user=login_session,
                               userReportInfos=getUserInfo(
                                editedReport.user_id))
    else:
        return render_template('editsinglereport.html',
                               report=editedReport,
                               frames=frames,
                               report_id=report_id,
                               frame_choice=editedReport.frame_choice,
                               customised=editedReport,
                               user=login_session,
                               userReportInfos=getUserInfo(
                                editedReport.user_id))


@app.route('/reports/<int:report_id>/delete', methods=['GET', 'POST'])
def deleteSingleReport(report_id):
    reportToDelete = session.query(Report).filter_by(id=report_id).one()
    filename = reportToDelete.report_picture
    if request.method == 'POST':
        os.remove("%s%s" % (upload_folder, filename))
        session.delete(reportToDelete)
        session.commit()
        flash("report was deleted !")
        return redirect(url_for('showAllReports'))

    return render_template('deletesinglereport.html',
                           report=reportToDelete,
                           user=login_session,
                           userReportInfos=getUserInfo(reportToDelete.user_id))


#--------------------------------------------------------
#--------------------Manage app settings-----------------
#--------------------------------------------------------


if __name__ == '__main__':

    app.run()

#--------------------------------------------------------
#--------------------End of app--------------------------
#--------------------------------------------------------
