import './App.css';
import { useState } from 'react';
import { BrowserRouter, BrowserRouter as Router, Navigate, Route, Routes, Switch } from 'react-router-dom';
//import {useCookies, setCookie, removeCookie } from "react-cookie"
import { useCookies } from 'react-cookie' // const [cookies, setCookie] = useCookies(['sessionId']);

// import home
import Home from './comp.js';

function App() {

  const [cookies, setCookie, deleteCookie] = useCookies(['sessionId']);

  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Home cookies={cookies}/>} exact/>
        <Route path="/login" element={<LoginForm setCookie={setCookie} />} exact/>
        <Route path="/registration" element={<RegisterForm setCookie={setCookie} />} exact/>
        <Route path="/logout" element={<Logout deleteCookie={cookies,deleteCookie} />} exact/>
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>

    </BrowserRouter>
  );
}

function Logout({ cookies, deleteCookie }) {

  // Send a request to the server to log the user out
  console.log(cookies.sessionId);
  fetch('http://localhost:5000/logout',{
    method:'POST',
    headers: {
      'Content-Type': 'application/json',
      'sessionId': cookies.sessionId
    }
  }).then((response) => (response.json())).then((res)=>{

    // Remove the 'name' cookie
    if(res.result){
      deleteCookie('sessionId', { path: '/' });
      console.log('done');
    }
  });


    return <Navigate to="/login" />;
}

// login form function that redirects from login page and sets cookie
function LoginForm({ setCookie }) {

  // Add an event handler for the login form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // Get the form data
    const data = new FormData(event.target);

    // Send a request to the server to log the user in and the redirect to < Home />
    fetch('http://localhost:5000/login', {
      method: 'POST',
      body: data,
    }).then((response) => response.json()).then((res) => {
      console.log(res.result);
      if (res.result) { 
        setCookie('sessionId', res.sessionId, { path: '/' });
      } else {
        console.log('wrong password or username');
      }}
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Login</h1>
      <label htmlFor="username">Username:</label>

      <input type="text" id="username" name="username" />
      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" />
      <button type="submit">Login</button>
    </form>
  );
}


function RegisterForm({ setCookie }) {

  // Add an event handler for the login form submission
  const handleSubmit = (event) => {
    event.preventDefault();

    // Get the form data
    const data = new FormData(event.target);

    // Send a request to the server to log the user in and the redirect to < Home />
    fetch('http://localhost:5000/register', {
      method: 'POST',
      body: data,
    }).then((response) => response.json()).then((res) => {
      console.log(res.result);
      if (res.result) { 
        setCookie('sessionId', res.sessionId, { path: '/' });
      } else {
        console.log('wrong password or username');
      }}
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <h1>Registration</h1>
      <label htmlFor="username">Username:</label>

      <input type="text" id="username" name="username" />
      <label htmlFor="password">Password:</label>
      <input type="password" id="password" name="password" />
      <button type="submit">Login</button>
    </form>
  );

}

function LoggedInView({cookies, deleteCookie}) {

  // Add an event handler for the logout button
  const handleLogout = () => {

    // Send a request to the server to log the user out
    fetch('http://localhost:5000/logout',{
      method:'POST',
      headers: {
        'Content-Type': 'application/json',
        'sessionId': cookies.sessionId
      }
    }).then((response) => (response.json())).then((res)=>{

      // Remove the 'name' cookie
      if(res.result){
        deleteCookie('sessionId');
        console.log('done');
      }
    });
  };

  return (
    <div>
      <p>You are logged in</p>
      <button onClick={handleLogout}>Log out</button>
    </div>
  );
}


  export default App;
