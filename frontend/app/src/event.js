import React from 'react';
import { useEffect, useState } from 'react';
import axios from 'axios';
import { Cookies } from 'react-cookie'

function Event(){
    
    // no auth functionality, page is supposed to render if logged in

    const [data, setData] = React.useState([]);

    useEffect(() => {
        async function fetchData(){
            try{
                const response = await fetch('http://localhost:5000/events',{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'sessionId': Cookies.get('session')
                    }
                });
                console.log(response);
                const data = await response.json();
                setData(data);
                
            }catch(error){
                console.log(error);
            }
        }
        fetchData();
    }, []);

    return(
        <div>
            <h1>Home</h1>
            <div>
            {Array.isArray(data) ? data.map(event => (
        <h1>id {event.eventId} name {event.eventName}</h1>
      )) : <div>Error: data is not an array</div>}
            </div>
            
        </div>
    )
}

export default Event;