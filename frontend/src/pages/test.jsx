import React, { useEffect } from 'react';

export default function Test() {
    useEffect(() => {
        const socket = new WebSocket('ws://localhost:8000/ws/result/');
    
        socket.onopen = () => {
          console.log('WebSocket connection established.');
          sendMessage('Hello from frontend!'); // Example: Sending a message when the connection is opened
        };
    
        socket.onmessage = (event) => {
          console.log('Received message:', event.data);
        };
    
        socket.onclose = () => {
          console.log('WebSocket connection closed.');
        };
    
        const sendMessage = (message) => {
          socket.send(message);
        };
    
        return () => {
          socket.close();
        };
      }, []);
    
      return <div>Your React component</div>;
}