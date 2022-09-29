import json
from yaml import load
from backend import app
from flask import request, jsonify, make_response, render_template, session, redirect 
from backend.midware import checkuser, createBooking, pageFunc, pageFuncs, checkbooking
from backend.midware import register as registering
from backend.db import cur

# Tested, it should register following user, and create session for that user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        register_status = registering(request.form['username'],request.form['password'])
        print(register_status)

        if register_status != None or register_status != False:
            session['name'] = register_status
            print('aloha')
            return redirect('/events')
        else:
            return 'make sure to enter another username or enter username/password'
            
    else:
        return render_template('register.html')

# Tested, it should login a user and redirect to a url
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #if not session.get('name'):
            #return redirect('/events')

        username = request.form['username']
        print(username, request.form['password'])
        login_status = checkuser(username,request.form['password'])

        if login_status !=None or login_status !=False:
            session["name"] = login_status
            return redirect('/events')
        else:
            return redirect('/login')
    return render_template('login.html') # not needed due to React

# Tested, should logout user / set user value in session to be None, then redirect user
@app.route('/logout',methods=['POST'])
def logout():
    session["name"] = None
    redirect('/login')

# Tested, create a booking for a particular event
@app.route('/event/Booking',methods=['POST'])
def Booking():
    if session.get('name'): # checks if a user exists in the session 
    
        eventId, eventName, userId = request.json['eventId'], request.json['eventName'], session['name']
        #    timeSlot = request.json['timeSlot'] later implementation

        if not session.get("name") and request.json['usesid'] != None:
            return jsonify({"Already booked"})
        elif session.get("name") == request.json['usesid'] != None:
            return jsonify({"Already booked"})
        elif session.get("name") and request.json['usesid'] != None:
            return jsonify({"Already booked"})
        else:
            try:
                createBooking(userId,eventId,eventName)
                return redirect('/events')

            except:
                return jsonify({"Error in booking"})

    return redirect('/events')



# Tested, list all the events available
@app.route('/events',methods=['GET'])
def events():

    #return jsonify(session['name'])

    if not session.get('name'):
        return redirect('/login')

    eventObject = {} # JSON object to be appended and returned to the URI call

    eventPages = pageFuncs() # Queries the postgres database with all the necessary details
    for i,event in enumerate(eventPages): # Creates a new dict key with the following event details
        (eventId,eventName) = event
        eventObject[i] = [eventId,eventName]    
    return jsonify(eventObject) 

# Tested, specific event page info
@app.route('/event/<string:eventName>',methods=['GET'])
def eventPage(eventName):
    userId = session["name"]

    # (eventId, eventName, usesId)
    event_content = pageFunc(eventName) # if uses id exists then remove booking functionality from webpage
    eventId,eventName,usesId = event_content[0],event_content[1],event_content[2]

    if usesId == None:
        return 'available'
    elif usesId == session.get("name"):
        return 'your booking'
    else:
        return jsonify(session.get("name"), usesId)


    """res = checkbooking(userId,eventId) 
    if res is True:
        return jsonify({eventId,eventName,usesId},{"booked":True,"recipient":True})
    elif res["recipient"] == False:
        return jsonify({eventId,eventName,usesId},{"booked":True,"recipient":res["recipient"]})
    else:   
        return jsonify({eventId,eventName,usesId},{"booked":False,"recipient":False})"""

### SERVING HTML PAGES ###
@app.route('/allevents', methods=['GET'])
def allevents():
    pass
    return render_template('landing')

@app.route('/event/{eventName}', methods=['GET'])
def event():
#    pass
    return render_template('event')

# Only for testing 
@app.route('/',methods=['GET'])
def test():
    return jsonify('this works right here')


