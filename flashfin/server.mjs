//npm install openai
//npm install express
//npm install cors

import express from 'express';
import cors from 'cors';
import { OpenAI } from "openai";
import dotenv from 'dotenv';
dotenv.config();
const app = express();
const port = process.env.PORT || 3005;
const apiKey = process.env.OPEN_AI_KEY;
const openai = new OpenAI({ apiKey: apiKey });

app.use(cors());
app.use(express.json());
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});

let conversationHistory = [];

app.post("/chatbot", async (req, res) => {
    const { question } = req.body;

    // Limit the conversation history to keep the context relevant and concise
    if (conversationHistory.length > 5) {
        conversationHistory.shift();  // Remove the oldest entry if history exceeds 5 messages
    }

    const messages = [
        {
            role: "system",
            content:
                "You are a financial assistant named Flashy. You ONLY answer questions regarding financials. You are responding to college students so base your inputs on the fact that they have the financials of an 18-22 year old college student.",
        },
        ...conversationHistory,
        {
            role: "user",
            content: question,
        },
    ];

    const response = await openai.chat.completions.create({
        messages: messages,
        model: "gpt-3.5-turbo",
        max_tokens: 125,
    });

    const botResponse = response.choices[0].message.content;

    // Add the latest exchange to the conversation history
    conversationHistory.push({ role: "user", content: question });
    conversationHistory.push({ role: "assistant", content: botResponse });

    res.send(botResponse);
});
