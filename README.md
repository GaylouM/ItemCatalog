# Report manager

## Section 0: Intro
This app has to objective to help civil ingineers to improve the way they are creating, 
editing and generate reports after a building diagnosis for exemple.
In the future the app will be composed of three modules.

The first module:
This part will manage the import of pictures after the visit in order to 
automatically create the structure of the report (not concerned by the project)

The second module:
The second module will manage the informations that the technician got on the site 
(this part is concerned by the project but the import of the picture is also treated 
even though this part is suppose to be treated in the first module at the end)

The third module
The last module will organize the data and create a pdf file.

## Section 1: Set Up Environment

First we need to run a virtual machine to host our website and then configure it with vagrant. Download and install the last version of VirtualBox first and Vagrant then.
To run vagrant first open gitbash and change directory to fullstack/vagrant, then type vagrant up to launch our virtual machine and vagrant ssh to log into it.

## Section 2: Requirements

sqlalchemy == 1.0.11
werkzeug == 0.11.4
exifread == 2.1.2
flask-bootstrap == 3.2.0.2
flask-login == 0.1.3
flask-sqlalchemy == 2.1
flask == 0.10.1
httplib2 == 0.9.2
jinja2 == 2.8
pip == 8.1.1
psycopg2 == 2.6.1
python-docx == 0.8.5
python-vagrant == 0.5.11

(It is just an example, these modules may not correspond with yours)
This list should be included in a separated file called "requirements.txt" for an easy installation using "pip install -r requirements.txt" 

## Section 3: Installation

Download the package and install it into the vagrant directory

## Section 4: Set Up

First we need to reach the good directory by typing "cd /vagrant" and "cd \website". Then we must populate the base and to do this we need to run lotsofreportsandframeswithusers.py with this command "python lotsofreportsandframeswithusers.py".

## Section 5: How to run

Finally we can run the website by typing "finalProject.py". The website is running locally on the port 5000 so to access the main page we need to open a navigator and type http://localhost:5000/

## Section 6: Usage

The aim of the app is to create report. A report is composed of writen datas and photos.
To simplify the creation of report we can sometimes create frames. The frame is useful when a client asks to diagnosis his buildings and the basics administrative informations of the report are the same (for example 30 reports with always the same client's and editor's informations). We can create reports specifying we want 30 of them based on the frame 1, and then let's imagine that we made a mistake on the client informations we just have to correct it on the frame 1. Really time-saving.