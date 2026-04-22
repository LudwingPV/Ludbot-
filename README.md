---
title: LudBot
emoji: 🤖
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: "5.25.0"
app_file: app.py
pinned: false
---

# LudBot — LangChain Weather & Time Agent

![LudBot Demo](https://raw.githubusercontent.com/LudwingPV/Ludbot-/80b98f5/demo.gif.gif)

LudBot is an AI agent built with LangChain and Groq that answers questions about the current time and weather for any city in the world. Ask about San Salvador, Tokyo, New York, Rio de Janeiro — LudBot fetches live data in real time and responds conversationally.

What makes it interesting is the live agent log panel below the chat. Every step the agent takes is visible as it happens — which tool it calls, what input it sends, what result comes back. You're not just talking to a chatbot, you're watching it think.

## How It Works

LudBot uses a LangChain agent loop with two tools wired to a Groq LLM. When a user sends a message, the agent decides which tool to call, executes it, reads the result, and formulates a response. The orchestration happens entirely through LangChain — the LLM is just the brain deciding what to do next.

The two tools are a time tool that resolves any city or timezone to the current local time, and a weather tool that calls wttr.in, a free public weather API that requires no key and covers every city on the planet.

## Screenshots

![LudBot Greeting](https://raw.githubusercontent.com/LudwingPV/Ludbot-/80b98f5/demo1.png)

The first thing LudBot does when you say hello is introduce itself — it knows it was created by Engineer Ludwing Pacas and immediately tells you what it can do. Short, friendly, and to the point. The agent log panel at the bottom is already active, showing every decision the agent makes even for a simple greeting.

![Global Queries — Tokyo](https://raw.githubusercontent.com/LudwingPV/Ludbot-/80b98f5/demo2.png)

This is where the agent really shows its capability. Asked about Tokyo with no specific instruction on whether to get time or weather, the agent decided on its own to call both tools — first resolving Asia/Tokyo timezone for the current local time, then fetching live weather data for the city. Both results came back and were delivered in a single clean response. The live log panel shows exactly which tools were called, what inputs were passed, and what each tool returned.

![Conversational Awareness — Rio de Janeiro](https://raw.githubusercontent.com/LudwingPV/Ludbot-/80b98f5/demo3.png)

After delivering results for Rio de Janeiro, the user simply said "Thank you" — and LudBot responded naturally, staying in character without trying to call any tools. This shows the agent understands conversational context, not just task execution. When no tool is needed, it doesn't use one. The agent log confirms this — thinking, then done, with no unnecessary tool calls in between.

## Tech Stack

- **LangChain** — agent orchestration and tool binding
- **Groq** — LLM inference (Meta Llama 4 Scout)
- **Gradio** — chat UI with live agent log panel
- **wttr.in** — free global weather API
- **Python** — runtime

## Run It Locally

Clone the repo and install dependencies:

```bash
git clone https://github.com/LudwingPV/LudBot.git
cd LudBot
pip install -r requirements.txt
```

Create a `.env` file in the root folder with your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key at [console.groq.com](https://console.groq.com).

Then run:

```bash
python app.py
```

Open `http://127.0.0.1:7860` in your browser and start chatting.

## Live Demo

Live on Hugging Face Spaces: [LudBot](https://huggingface.co/spaces/ludwingpv/LudBot)

---

Built by [Engineer Ludwing Pacas](https://github.com/LudwingPV)
