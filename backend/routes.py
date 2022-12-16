from backend import app
from backend.midware import checkuser, createBooking, pageFunc, pageFuncs, checkbooking
from backend.midware import register as registering

from flask import request, jsonify, make_response, render_template, redirect, session
from flask_session import Session

# Tested, it should register following user, and create session for that user
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        register_status = registering(request.json['username'],request.json['password'])
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
    return redirect('/login')

# Tested, create a booking for a particular event
@app.route('/event/Booking',methods=['GET','POST'])
def booking():

    if request.method == "POST":
        print('hey1')
        if session.get('name'): # checks if a user exists in the session 
            print('in session')
            print('hey2')
            eventId, eventName, usesId = request.json['eventId'], request.json['eventName'], session['name']
            #    timeSlot = request.json['timeSlot'] later implementation
            print(eventId,eventName,usesId)

            if request.json['booking'] == True and session["name"] == request.json['usesid']:
                print('hey3')
                return jsonify({"Your booking"})

            elif request.json['booking'] == True and session.get("name") and session["name"] != request.json['usesid']:
                print('hey4')
                return jsonify({"Already booked"})

            elif request.json['booking'] == True and not session.get("name"):
                print('he5')
                return jsonify({"Already booked"})

            else:
                try:
                    print('hey')
                    if createBooking(usesId,eventId,eventName):
                        return redirect(f'/event/{eventName}')
                    else:
                        return 'error in the backend'

                except:
                    return redirect(f'/event/{eventName}')

        #print('outside session')
        
        return redirect('/events')

    return render_template('events.html')


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

    return jsonify({'events':eventObject}) 

# Tested, specific event page info
@app.route('/event/<string:eventName>', methods=['GET'])
def eventPage(eventName):

    #print(session['name'])
    if session.get('name'):

        userId = session["name"]

        event_content = pageFunc(eventName) # if uses id exists then remove booking functionality from webpage

        if event_content is not None:
            print(event_content)
            eventId,eventName,usesId = event_content[0],event_content[1],event_content[2]

            if usesId == None:
                return jsonify({"eventId": eventId, "eventName": eventName, "usesId": usesId, "booked":False,"recipient":False})
            elif usesId == session["name"]:
                return jsonify({"eventId": eventId, "eventName": eventName, "usesId": usesId, "booked":True,"recipient":True})
            else:
                return jsonify({"eventId": eventId, "eventName": eventName, "usesId": usesId, "booked":True,"recipient":False})
        
        return jsonify({'error':'Page Does Not Exist Yet :( '})

    return redirect('/login')    

# Only for testing 
@app.route('/',methods=['GET'])
def test():
    return jsonify('this works right here')

