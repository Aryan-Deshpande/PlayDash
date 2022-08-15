from src import app
from flask import render_template, redirect, url_for, request, flash, jsonify, make_response
from src.midware import checkuser, register, createBooking, pageApi, pageApis
from src.db import cur

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if register(request.json['username'],request.json['password']):
            return jsonify("success")
    else:
        return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        checkuser(request.json['username'],request.json['password'])
    else:    
        return render_template('login.html')

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


