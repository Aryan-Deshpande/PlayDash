from backend import app
from flask import request, jsonify, make_response, render_template, session, redirect 
from backend.midware import checkuser, createBooking, pageFunc, pageFuncs, checkbooking
from backend.midware import register as registering
from backend.db import cur


# Tested, it should register following user, and create session for that user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':

        if registering(request.json['Username'],request.json['Password']):
            session[request.json['Username']] = request.json['Username'] 
            return redirect('/events')
        else:
            return 'wrong'
    else:
        return 'html page for registering,/ not needed because of React'

# Tested, it should login a user and redirect to a url
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':

        if not session.get('name'):
            return redirect('/events')
        username = request.json['Username']

        if checkuser(username,request.json['Password']):
            session[username] = username
            return redirect('/events')
        else:
            return redirect('login')
    return render_template('login.html') # not needed due to React

# Tested, should logout user / set user value in session to be None, then redirect user
@app.route('/logout',methods=['POST'])
def logout():
    session[session.get("name")] = None
    redirect('/login')

# Tested, create a booking for a particular event
@app.route('/event/Booking',methods=['POST'])
def Booking():
    userId = session.get('name')
    #    timeSlot = request.json['timeSlot'] later implementation
    eventId = request.json['eventId']
    eventName = request.json['eventName']

    """if session.get("name") is None and request.json['Booked'] == True:
        return jsonify({"Already booked"})"""
    try:
        createBooking(userId,eventId,eventName)
    except:
        return jsonify({"Error in booking"})

    return jsonify('success')


# Tested, list all the events available
@app.route('/events',methods=['GET'])
def events():
    eventObject = {} # JSON object to be appended and returned to the URI call

    eventPages = pageFuncs() # Queries the postgres database with all the necessary details
    for i,event in enumerate(eventPages): # Creates a new dict key with the following event details
        (eventId,eventName) = event
        eventObject[i] = [eventId,eventName]    
    return jsonify(eventObject)    

# Tested, specific event page info
@app.route('/event/{eventName}',methods=['GET'])
def eventPage(eventName):
    userId = session.get("name")

    (eventId, eventName, usesId) = pageFunc() # if uses id exists then remove booking functionality from webpage

    res = checkbooking(userId,eventId) 
    if res is True:
        return jsonify({eventId,eventName,usesId},{"booked":True,"recipient":True})
    elif res["recipient"] == False:
        return jsonify({eventId,eventName,usesId},{"booked":True,"recipient":res["recipient"]})
    else:   
        return jsonify({eventId,eventName,usesId},{"booked":False,"recipient":False})

""" Only for testing """
@app.route('/test',methods=['GET'])
def test():
    return jsonify('success', 403)
