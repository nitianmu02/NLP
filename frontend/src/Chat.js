// Chat.js
import React, { useState, useEffect } from "react";
import WebSocket from "ws";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [ws, setWs] = useState(null);

  // 创建socket实例
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000");
    setWs(socket);
  }, []);

  // 处理socket消息
  useEffect(() => {
    if (ws) {
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data.message]);
      };
    }
  }, [ws]);

  // 发送socket消息
  const sendMessage = () => {
    if (ws && input) {
      ws.send(JSON.stringify({ message: input }));
      setInput("");
    }
  };

  // 渲染聊天界面
  return (
    <div className="chat">
      <h1>Chat Room</h1>
      <div className="messages">
        {messages.map((message, i) => (
          <p key={i}>{message}</p>
        ))}
      </div>
      <div className="input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
