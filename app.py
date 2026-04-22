import os
import gradio as gr
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from tools import get_current_time, get_weather

# ── Load API key from .env ────────────────────────────────────────────────────
load_dotenv()

# ── LLM — Groq is the brain, LangChain is the orchestrator ───────────────────
llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Tools — what the agent can call ──────────────────────────────────────────
tools = [get_current_time, get_weather]
tools_map = {t.name: t for t in tools}

# ── Bind tools to LLM (modern LangChain approach) ────────────────────────────
llm_with_tools = llm.bind_tools(tools)

# ── Agent loop — LLM thinks, calls tools, thinks again until done ─────────────
def run_agent(message, history):
    logs = []

    # Build message history (Gradio 6.0 uses dicts with role/content)
    messages = [
        SystemMessage(content="""You are LudBot, a friendly assistant created by Engineer Ludwing Pacas.
When the user greets you, introduce yourself as LudBot and mention you were created by Engineer Ludwing Pacas. Briefly explain that your purpose is to assist with two things: providing the current time for any city or timezone worldwide, and current weather for any city in the world.
Keep your introduction short and friendly — no more than 3 sentences.
If the user asks about anything outside of time and weather, politely let them know that falls outside your capabilities and redirect them to what you can help with.
Always be concise and friendly.""")
    ]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))
    messages.append(HumanMessage(content=message))

    # Agent loop
    while True:
        logs.append("🧠 Agent is thinking...")
        response = llm_with_tools.invoke(messages)
        messages.append(response)

        # If no tool calls — agent is done
        if not response.tool_calls:
            logs.append("✅ Done!")
            break

        # Call each tool the agent requested
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]

            logs.append(f"🔧 Calling tool: {tool_name}")
            logs.append(f"   Input: {tool_args}")

            # Execute the tool
            tool_result = tools_map[tool_name].invoke(tool_args)
            logs.append(f"   Result: {tool_result}")

            # Feed result back to agent
            messages.append(ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            ))

    return response.content, "\n".join(logs)

# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(theme=gr.themes.Soft(), title="LangChain Agent Bot") as demo:

    gr.Markdown("# 🤖 LangChain Agent — Weather & Time Bot")
    gr.Markdown("Ask me: **'What time is it?'** or **'What's the weather in San Salvador?'**")

    # Top panel — Chat UI
    chatbot = gr.Chatbot(height=350, label="Chat", type="messages")
    msg = gr.Textbox(placeholder="Type your message here...", label="You")
    send_btn = gr.Button("Send →", variant="primary")

    gr.Markdown("---")
    gr.Markdown("### ⚙️ Live Agent Logs — watch how it works under the hood")

    # Bottom panel — Live logs (the open heart mechanism)
    logs = gr.Textbox(
        label="Agent Steps",
        lines=8,
        interactive=False,
        placeholder="Agent logs will appear here as it processes your request..."
    )

    # Wiring — what happens when user sends a message
    def respond(message, history):
        response, log_output = run_agent(message, history)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": response})
        return "", history, log_output

    send_btn.click(respond, [msg, chatbot], [msg, chatbot, logs])
    msg.submit(respond, [msg, chatbot], [msg, chatbot, logs])

# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    demo.launch()
