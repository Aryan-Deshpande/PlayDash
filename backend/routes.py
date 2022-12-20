# doesnt have central storage for session, each route has its own checking

from backend import app
from backend.midware import checkuser, createBooking, pageFunc, pageFuncs, checkbooking
from backend.midware import register as registering

from flask_session import SessionInterface
from flask import request, jsonify, make_response, render_template, redirect, session


# gets the session data from the session store
def get_session_data(session_id):
  # Get the session interface
  session_interface = SessionInterface()

  # Get the session data from the session store
  session_data = session_interface.get_session_data(session_id)

  return session_data

# Tested, it should register following user, and create session for that user
@app.route('/register',methods=['POST'])
def register():

    if request.method == 'POST':
        register_status = registering(request.json['username'],request.json['password'])
        print(register_status)

        if register_status != None or register_status != False:
            session['name'] = register_status

            sessionId = request.cookies.get('session')

            return jsonify({'result':True, 'sessionId':sessionId})
        else:
            return jsonify({'result':False})
            
        # return render_template('register.html') // not needed, since implementing react

# Tested, it should login a user and redirect to a url
@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
                                    
        login_status = checkuser(request.form.get('username'),request.form.get('password'))
        print(login_status, "login status")

        if login_status !=False:
            print(login_status, 'in check')
            session["name"] = login_status

            sessionId = request.cookies.get('session')

            return jsonify({'result':True, 'sessionId':sessionId})
        else:
            return jsonify({'result':False})

# Tested, should logout user / set user value in session to be None, then redirect user
@app.route('/logout',methods=['POST'])
def logout():

    session.clear()
    return jsonify({'result':True})

# Tested, create a booking for a particular event
@app.route('/event/Booking',methods=['POST'])
def booking():

    if request.method == "POST":
        
        sessionId = request.headers.get('sessionId')
        sessiondata = get_session_data(sessiondata)

        if not sessiondata:
            return jsonify({'error':'Unauthorized'}), 400
        else:
            eventId, eventName, usesId = request.json['eventId'], request.json['eventName'], session['name']
            #    timeSlot = request.json['timeSlot'] later implementation
            #print(eventId,eventName,usesId)

            if request.json['booking'] == True and session["name"] == request.json['usesid']:
                #print('hey3')
                return jsonify({"Your booking"})

            elif request.json['booking'] == True and session.get("name") and session["name"] != request.json['usesid']:
                #print('hey4')
                return jsonify({"Already booked"})

            elif request.json['booking'] == True and not session.get("name"):
                #print('he5')
                return jsonify({"Already booked"})

            else:
                try:
                    #print('hey')
                    if createBooking(usesId,eventId,eventName):
                        return redirect(f'/event/{eventName}')
                    else:
                        return 'error in the backend'

                except:
                    return redirect(f'/event/{eventName}')

        #print('outside session')
        #return redirect('/events')
        return jsonify({'res':False})

# Tested, list all the events available
@app.route('/events',methods=['GET'])
def events():

    # retrival of sessionId through the request headers
    sessionId = request.headers.get('sessionId')

    # Retrieve the session data from the session store
    sessiondata = get_session_data(sessionId)

    if not sessiondata:
        return jsonify({'error':'Unauthorized'}), 400

    # JSON object to be appended and returned to the URI call
    eventObject = [] 

    # Queries the postgres database with all the necessary details
    eventPages = pageFuncs()

    # Creates a new dict key with the following event details
    for i,event in enumerate(eventPages): 

        (eventId,eventName,eventDate) = event
        eventObject.append({'eventId':eventId,'eventName':eventName,'eventDate':eventDate})    
    print({'events':f'{eventObject}'})
    return eventObject  

# Tested, specific event page info
@app.route('/event/<string:eventName>', methods=['GET'])
def eventPage(eventName):

    session_id = request.headers.get('sessionId')
    session_data = get_session_data(session_id)

    # if uses id exists then remove booking functionality from webpage
    event_content = pageFunc(eventName) 

    if event_content is not None:
        print(event_content)
        eventId,eventName,eventDate = event_content[0],event_content[1],event_content[2]

        return jsonify({"eventId": eventId, "eventName": eventName, "eventDate": eventDate})
    
    """if usesId == None:
                return jsonify({"eventId": eventId, "eventName": eventName, "booked":False,"recipient":False})
            elif usesId == session["name"]:
                return jsonify({"eventId": eventId, "eventName": eventName, "booked":True,"recipient":True})
            else:
                return jsonify({"eventId": eventId, "eventName": eventName, "booked":True,"recipient":False})
        
    return jsonify({'error':'Page Does Not Exist Yet :( '})"""


    #return redirect('/login')    

# Only for testing 
@app.route('/',methods=['GET'])
def test():
    return jsonify('this works right here')

