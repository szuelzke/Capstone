import React, { useState } from 'react';
import axios from 'axios';
import '../style/Chatbox.css';

function Chatbox() {
    const [messages, setMessages] = useState([{ text: "Hi there! How can I assist you?", sender: "chatbot" }]);
    const [value, setValue] = useState("");

    const onChange = (e) => setValue(e.target.value);

    const handleSubmit = async () => {
        if (value.trim() === "") return;  // Prevent empty submissions
        const userMessage = { text: value, sender: "user" };
        setMessages([...messages, userMessage]);
        setValue("");
        const response = await axios.post("http://localhost:3005/chatbot", { question: value });
        const chatbotMessage = { text: response.data, sender: "chatbot" };
        setMessages(messages => [...messages, chatbotMessage]);

        setValue("");  // Clear input after sending
    };

    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            handleSubmit();
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-window">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender}`}>
                        {message.sender === 'user' ? `You: ${message.text}` : `Flashy: ${message.text}`}
                    </div>
                ))}
            </div>
            <div className="message-input">
                <input
                    type="text"
                    value={value}
                    onChange={onChange}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message here..."
                />
                <button onClick={handleSubmit}>Send</button>
            </div>
        </div>
    );
}

export default Chatbox;
