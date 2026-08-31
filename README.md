# 🌍 City Intelligence AI Agent

An AI-powered city intelligence chatbot built with **Mistral AI, LangChain, Tavily, OpenWeather API, and Streamlit**.

The application allows users to ask questions about a city and intelligently uses the appropriate tool to retrieve **current weather information** or **latest news**. Before executing a tool, the agent asks the user for approval, implementing a human-in-the-loop workflow.

## 🚀 Features

* 🤖 AI agent powered by **Mistral AI**
* 🌤️ Current weather information using **OpenWeather API**
* 📰 Latest city news using **Tavily Search**
* 🔧 LangChain tool calling
* 👤 Human-in-the-loop tool approval
* 💬 Interactive conversational interface
* 🎨 Streamlit-based web UI

## 🏗️ Architecture
```text

                 User
                  │
                  ▼
          ┌───────────────┐
          │   Streamlit   │
          │      UI       │
          └───────┬───────┘
                  │
                  ▼
          ┌───────────────┐
          │ Mistral AI    │
          │     Agent     │
          └───────┬───────┘
                  │
          ┌───────┴────────┐
          │                │
          ▼                ▼
   Get Weather          Get News
          │                │
          ▼                ▼
   OpenWeather           Tavily
          │                │
          └───────┬────────┘
                  │
                  ▼
             Final Answer
```

## 🔧 Technologies Used

| Technology      | Purpose                         |
| --------------- | ------------------------------- |
| Python          | Application development         |
| LangChain       | Agent and tool orchestration    |
| Mistral AI      | Large Language Model            |
| OpenWeather API | Current weather data            |
| Tavily          | Latest news search              |
| Streamlit       | Interactive web interface       |
| python-dotenv   | Environment variable management |

## 🔄 How It Works

1. The user enters a question through the Streamlit interface.
2. The Mistral-powered agent analyzes the request.
3. The agent determines whether a tool is required.
4. If a tool is required, the application asks the user for approval.
5. After approval, the selected tool is executed.
6. The retrieved information is returned to the agent.
7. The agent generates the final response for the user.

### Example

```text
User:
What is the weather in Delhi?

Agent:
The agent wants to call get_weather.

User:
Approve

Tool:
Weather in Delhi: Clear sky, 31°C

Agent:
The current weather in Delhi is clear with a temperature of 31°C.
```

## 📁 Project Structure

```text
City-Intelligence-Agent/
│
├── agent.py
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

> `.env` should not be committed to GitHub. Store API keys securely using environment variables or the deployment platform's secrets manager.

## 🔐 Environment Variables

Create a `.env` file locally:

```text
MISTRAL_API_KEY=your_mistral_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

Never commit the `.env` file containing actual API keys.

## ▶️ Run Locally

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project:

```bash
cd City-Intelligence-Agent
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
python -m streamlit run app.py
```

The application will open at:

```text
http://localhost:8502
```

## 🎯 Skills Demonstrated

**Generative AI • AI Agents • LLM Tool Calling • LangChain • Mistral AI • API Integration • Human-in-the-Loop • Prompt Engineering • Streamlit • Python**

## 👩‍💻 Author

**Megha Thakur**

Built as a Generative AI project demonstrating practical implementation of an LLM-powered tool-using agent with an interactive web interface.
