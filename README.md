# AI-First CRM – HCP Interaction Module

This project implements the "Log Interaction Screen" for an AI-first CRM system designed for Life Sciences field representatives.

## Tech Stack
- Frontend: React + Redux
- Backend: FastAPI (Python)
- AI Agent Framework: LangGraph
- LLM: Groq (gemma2-9b-it)
- Database: SQLite (Demo) | Postgres (Production)
- Font: Google Inter

## Architecture
React UI → FastAPI → LangGraph Router → Tool → LLM → Structured JSON → Redux Store → UI

## LangGraph Tools Implemented
1. Log Interaction Tool  
2. Edit Interaction Tool  
3. Suggest Followups Tool  
4. Fetch HCP History Tool  
5. Compliance Check Tool  

## How It Works
- Users describe HCP interactions in natural language.
- LangGraph routes the request to the correct tool.
- LLM extracts structured data.
- The left panel auto-fills using Redux state.
- Edits happen only via chat.

## Run Locally

### Backend
```bash
pip install fastapi uvicorn langgraph langchain-groq sqlalchemy python-dotenv
uvicorn main:app --reload
