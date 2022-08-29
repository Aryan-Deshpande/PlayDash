from backend import app
from flask import request, jsonify, make_response, render_template, session, redirect 
from backend.midware import checkuser, register, createBooking, pageApi, pageApis
from backend.db import cur

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if register(request.json['username'],request.json['password']):
            session[request.json['username']]
        else:
            make_response({'missing username or password'})
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if checkuser(request.json['username'],request.json['password']):
            session[request.json['username']]
            redirect('/events')
        else:
            make_response({'Wrong password or user does not exist'})
    else:    
        return render_template('login.html')

@app.route('/logout',methods=['POST'])
def logout():
    session[session.get("name")] = None
    redirect('/login')

# create a booking for a particular event
@app.route('/event/Booking', methods=['POST'])
def Booking():
    #payemnt 
    userId = request.json['userId']
#    timeSlot = request.json['timeSlot'] later implementation
    eventId = request.json['eventId']
    eventName = request.json['eventName']
    createBooking(userId,eventId,eventName)
    return jsonify('success')

# list all the events available
@app.route('/events',methods=['GET'])
def events():
    eventObject = {} # JSON object to be appended and returned to the URI call

    eventPages = pageApis() # Queries the postgres database with all the necessary details
    for i,event in enumerate(eventPages): # Creates a new dict key with the following event details
        (eventId,eventName) = event
        eventObject[i] = [eventId,eventName]    
    return jsonify(eventObject)    

# specific event page info
@app.route('/event/{eventName}',methods=['GET'])
def eventPage(eventName):
    (eventId, eventName, usesId) = pageApi
    if usesId is not None:
        usesId = True
    return jsonify(eventId,eventName,usesId)

@app.route('/test',methods=['GET'])
def test():
    return jsonify('success', 403)
