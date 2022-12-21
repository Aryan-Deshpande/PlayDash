import React from 'react';
import { useEffect, useState } from 'react';
import {Cookies} from 'react-cookie'
import { useCookies } from 'react-cookie'

function Home({ cookies }){
    
    // no auth functionality, page is supposed to render if logged in

    const [data, setData] = React.useState([]);

    const sessionId = cookies['sessionId'];

    useEffect(() => {
        console.log('hey there')
        function fetchData(){
            try{
                console.log(sessionId)
        
                fetch('http://localhost:5000/events',{

                    method:'GET',
                    headers:{
                        'Content-Type':'application/json',
                        'sessionId': sessionId

                    }
                }).then((response)=>response.json()).then((res)=>{
                    console.log(res);
                    setData(data);
                });                
                console.log('hey there3')

            }catch(error){
                console.log(error);
            }
        }
        fetchData();
    }, );

    const book = (event)=>{
        fetch('http://localhost:5000/event/Booking',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'sessionId': Cookies.get('sessionId')
            },
            body: JSON.stringify({
                eventId: event
            }).then((response)=> response.json()).then((res)=>{
                console.log(res);

            })
        })
    }

    return(
        <div>
            <h1>Home</h1>
            <div>

            {Array.isArray(data) ? data.map(event => (

                <div>
        
                    <h1>id {event.eventId} name {event.eventName} date {event.eventDate}</h1>
        
                </div>

        )) : <div>Error: data is not an array</div>}
            
            </div>
            
        </div>
    )
}

export default Home;