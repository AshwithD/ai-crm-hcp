# import os
# import json
# from typing import TypedDict
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph, END

# # ----------------- ENV -----------------
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # ----------------- APP -----------------
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------------- LLM -----------------
# llm = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model="llama-3.3-70b-versatile",
#     temperature=0.2
# )

# # ----------------- MODELS -----------------
# class ChatInput(BaseModel):
#     message: str

# class GraphState(TypedDict, total=False):
#     message: str
#     tool: str
#     result: dict

# # ----------------- HELPERS -----------------
# def safe_json(text: str):
#     try:
#         return json.loads(text)
#     except Exception:
#         start = text.find("{")
#         end = text.rfind("}")
#         if start != -1 and end != -1:
#             try:
#                 return json.loads(text[start:end+1])
#             except Exception:
#                 pass
#     return {}

# # ----------------- TOOLS -----------------
# def log_interaction_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# Extract structured fields from the interaction below.
# Return ONLY valid JSON.

# Fields:
# hcp_name
# date (YYYY-MM-DD, use today if not mentioned)
# sentiment (positive | neutral | negative)
# materials_shared (list of strings)
# samples_distributed (list of strings)
# topics_discussed (list of strings)
# attendees (string)
# outcomes (string)
# followups (list of strings)

# Text:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def edit_interaction_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# The user is correcting a previously logged interaction.

# STRICT RULES:
# - Return ONLY the fields explicitly corrected.
# - DO NOT return other fields.
# - DO NOT return null or empty arrays.
# - Return ONLY valid JSON.

# Possible fields:
# hcp_name
# date
# sentiment
# materials_shared
# samples_distributed
# topics_discussed
# attendees
# outcomes
# followups

# Correction:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def suggest_followups_tool(state: GraphState) -> GraphState:
#     prompt = """
# Suggest 3 follow-up actions for a pharma sales interaction.
# Return ONLY valid JSON:
# { "followups": [ "action 1", "action 2", "action 3" ] }
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def fetch_hcp_history_tool(state: GraphState) -> GraphState:
#     return {
#         "result": {
#             "last_interaction": "2026-01-21",
#             "last_topic": "OncoBoost Phase III",
#             "last_sentiment": "neutral"
#         }
#     }

# def compliance_check_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# Check the following text for compliance issues (claims, consent, regulations).
# Return ONLY valid JSON in this format:
# {{ "issues": ["issue 1", "issue 2"] }}

# Text:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# # ----------------- ROUTER -----------------
# def router(state: GraphState) -> GraphState:
#     prompt = f"""
# You are a strict intent router for a CRM AI assistant.

# Choose exactly one tool:
# - "log" → user is describing a meeting/interaction
# - "edit" → user is correcting a previous interaction
# - "followup" → user asks for follow-up actions
# - "history" → user asks for previous interaction/history
# - "compliance" → user asks to check compliance or regulations

# Return ONLY valid JSON:
# {{ "tool": "log" | "edit" | "followup" | "history" | "compliance" }}

# User message:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     route = safe_json(res.content)
#     return {"tool": route.get("tool", "log")}

# # ----------------- LANGGRAPH -----------------
# graph = StateGraph(GraphState)

# graph.add_node("router", router)
# graph.add_node("log", log_interaction_tool)
# graph.add_node("edit", edit_interaction_tool)
# graph.add_node("followup", suggest_followups_tool)
# graph.add_node("history", fetch_hcp_history_tool)
# graph.add_node("compliance", compliance_check_tool)

# graph.set_entry_point("router")

# graph.add_conditional_edges(
#     "router",
#     lambda s: s["tool"],
#     {
#         "log": "log",
#         "edit": "edit",
#         "followup": "followup",
#         "history": "history",
#         "compliance": "compliance",
#     }
# )

# for node in ["log", "edit", "followup", "history", "compliance"]:
#     graph.add_edge(node, END)

# app_graph = graph.compile()

# # ----------------- API -----------------
# @app.get("/")
# def home():
#     return {"status": "AI CRM Backend running"}

# @app.post("/chat")
# def chat(data: ChatInput):
#     result = app_graph.invoke({"message": data.message})
#     return result.get("result", {})




# import os
# import json
# from typing import TypedDict
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv

# from langchain_groq import ChatGroq
# from langgraph.graph import StateGraph, END

# # ----------------- ENV -----------------
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # ----------------- APP -----------------
# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------------- LLM -----------------
# llm = ChatGroq(
#     api_key=GROQ_API_KEY,
#     model="llama-3.3-70b-versatile",
#     temperature=0.2
# )

# # ----------------- MODELS -----------------
# class ChatInput(BaseModel):
#     message: str

# class GraphState(TypedDict, total=False):
#     message: str
#     tool: str
#     result: dict

# # ----------------- HELPERS -----------------
# def safe_json(text: str):
#     try:
#         return json.loads(text)
#     except Exception:
#         start = text.find("{")
#         end = text.rfind("}")
#         if start != -1 and end != -1:
#             try:
#                 return json.loads(text[start:end+1])
#             except Exception:
#                 pass
#     return {}

# # ----------------- TOOLS -----------------
# def log_interaction_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# Extract structured fields from the interaction below.
# Return ONLY valid JSON.

# Fields:
# hcp_name
# date (YYYY-MM-DD, use today if not mentioned)
# sentiment (positive | neutral | negative)
# materials_shared (list of strings)
# samples_distributed (list of strings)
# topics_discussed (list of strings)
# attendees (string)
# outcomes (string)
# followups (list of strings)

# Text:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def edit_interaction_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# The user is correcting a previously logged interaction.

# STRICT RULES:
# - Return ONLY the fields explicitly corrected.
# - DO NOT return other fields.
# - DO NOT return null or empty arrays.
# - Return ONLY valid JSON.

# Possible fields:
# hcp_name
# date
# sentiment
# materials_shared
# samples_distributed
# topics_discussed
# attendees
# outcomes
# followups

# Correction:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def suggest_followups_tool(state: GraphState) -> GraphState:
#     prompt = """
# Suggest 3 follow-up actions for a pharma sales interaction.
# Return ONLY valid JSON:
# { "followups": [ "action 1", "action 2", "action 3" ] }
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# def fetch_hcp_history_tool(state: GraphState) -> GraphState:
#     return {
#         "result": {
#             "last_interaction": "2026-01-21",
#             "last_topic": "OncoBoost Phase III",
#             "last_sentiment": "neutral"
#         }
#     }

# def compliance_check_tool(state: GraphState) -> GraphState:
#     prompt = f"""
# Check the following text for compliance issues (claims, consent, regulations).
# Return ONLY valid JSON in this format:
# {{ "issues": ["issue 1", "issue 2"] }}

# Text:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     return {"result": safe_json(res.content)}

# # ----------------- ROUTER (FIXED) -----------------
# def router(state: GraphState) -> GraphState:
#     text = state["message"].lower()

#     # Deterministic guards for demo reliability
#     if "previous" in text or "history" in text or "last interaction" in text:
#         return {"tool": "history"}

#     if "compliance" in text or "regulation" in text or "compliant" in text:
#         return {"tool": "compliance"}

#     if "follow" in text:
#         return {"tool": "followup"}

#     if "sorry" in text or "actually" in text or "wrong" in text:
#         return {"tool": "edit"}

#     # Fallback to LLM router for natural descriptions
#     prompt = f"""
# You are a strict intent router for a CRM AI assistant.

# Choose exactly one tool:
# - "log" → user is describing a meeting/interaction
# - "edit" → user is correcting a previous interaction
# - "followup" → user asks for follow-up actions
# - "history" → user asks for previous interaction/history
# - "compliance" → user asks to check compliance or regulations

# Return ONLY valid JSON:
# {{ "tool": "log" | "edit" | "followup" | "history" | "compliance" }}

# User message:
# {state["message"]}
# """
#     res = llm.invoke(prompt)
#     route = safe_json(res.content)
#     return {"tool": route.get("tool", "log")}

# # ----------------- LANGGRAPH -----------------
# graph = StateGraph(GraphState)

# graph.add_node("router", router)
# graph.add_node("log", log_interaction_tool)
# graph.add_node("edit", edit_interaction_tool)
# graph.add_node("followup", suggest_followups_tool)
# graph.add_node("history", fetch_hcp_history_tool)
# graph.add_node("compliance", compliance_check_tool)

# graph.set_entry_point("router")

# graph.add_conditional_edges(
#     "router",
#     lambda s: s["tool"],
#     {
#         "log": "log",
#         "edit": "edit",
#         "followup": "followup",
#         "history": "history",
#         "compliance": "compliance",
#     }
# )

# for node in ["log", "edit", "followup", "history", "compliance"]:
#     graph.add_edge(node, END)

# app_graph = graph.compile()

# # ----------------- API -----------------
# @app.get("/")
# def home():
#     return {"status": "AI CRM Backend running"}

# @app.post("/chat")
# def chat(data: ChatInput):
#     result = app_graph.invoke({"message": data.message})
#     return result.get("result", {})



import os
import json
from typing import TypedDict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, JSON
from sqlalchemy.orm import declarative_base, sessionmaker

from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END

# ----------------- ENV -----------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ----------------- APP -----------------
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- DB -----------------
DATABASE_URL = "sqlite:///./hcp.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)

Base.metadata.create_all(bind=engine)

# ----------------- LLM -----------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.3-70b-versatile",  # gemma2 deprecated
    temperature=0.2
)

# ----------------- MODELS -----------------
class ChatInput(BaseModel):
    message: str

class GraphState(TypedDict, total=False):
    message: str
    tool: str
    result: dict

# ----------------- HELPERS -----------------
def safe_json(text: str):
    try:
        return json.loads(text)
    except Exception:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
    return {}

def safe_llm_invoke(prompt: str):
    try:
        return llm.invoke(prompt)
    except Exception as e:
        print("LLM Error:", e)
        return type("obj", (), {"content": "{}"})

# ----------------- TOOLS -----------------
def log_interaction_tool(state: GraphState) -> GraphState:
    prompt = f"""
Extract structured fields from the interaction below.
Return ONLY valid JSON.

Fields:
hcp_name
date (YYYY-MM-DD)
sentiment (positive | neutral | negative)
materials_shared (list of strings)
samples_distributed (list of strings)
topics_discussed (list of strings)
attendees (string)
outcomes (string)
followups (list of strings)

Text:
{state["message"]}
"""
    res = safe_llm_invoke(prompt)
    return {"result": safe_json(res.content)}

def edit_interaction_tool(state: GraphState) -> GraphState:
    prompt = f"""
You are editing an existing CRM interaction.

STRICT RULES:
- Return ONLY fields the user explicitly corrected.
- DO NOT include any other fields.
- DO NOT include empty strings, nulls, or empty arrays.
- Return ONLY valid JSON.

Allowed fields:
hcp_name
date
sentiment
materials_shared
samples_distributed
topics_discussed
attendees
outcomes
followups

User correction:
{state["message"]}
"""
    res = llm.invoke(prompt)
    data = safe_json(res.content)

    # Safety filter: remove empty values if LLM returns them
    clean = {}
    for k, v in (data or {}).items():
        if v is None:
            continue
        if isinstance(v, list) and len(v) == 0:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        clean[k] = v

    return {"result": clean}

def suggest_followups_tool(state: GraphState) -> GraphState:
    prompt = """
Suggest 3 follow-up actions for a pharma sales interaction.
Return ONLY valid JSON:
{ "followups": ["...", "...", "..."] }
"""
    res = safe_llm_invoke(prompt)
    return {"result": safe_json(res.content)}

def fetch_hcp_history_tool(state: GraphState) -> GraphState:
    return {
        "result": {
            "last_interaction": "2026-01-21",
            "last_topic": "Product X efficacy",
            "last_sentiment": "neutral"
        }
    }

def compliance_check_tool(state: GraphState) -> GraphState:
    prompt = f"""
Check the following text for compliance issues.
Return ONLY valid JSON:
{{ "issues": ["issue 1", "issue 2"] }}

Text:
{state["message"]}
"""
    res = safe_llm_invoke(prompt)
    data = safe_json(res.content)

    # Map issues -> compliance_issues for frontend
    if "issues" in data:
        return {"result": {"compliance_issues": data.get("issues", [])}}

    return {"result": {}}


# ----------------- ROUTER -----------------
def router(state: GraphState) -> GraphState:
    text = state["message"].lower()

    if "compliance" in text or "regulation" in text or "compliant" in text:
        return {"tool": "compliance"}

    if "previous" in text or "history" in text or "last interaction" in text:
        return {"tool": "history"}

    if "follow" in text:
        return {"tool": "followup"}

    if "sorry" in text or "actually" in text or "wrong" in text:
        return {"tool": "edit"}

    prompt = f"""
Choose one tool:
log | edit | followup | history | compliance

Return ONLY valid JSON:
{{ "tool": "log" | "edit" | "followup" | "history" | "compliance" }}

Message:
{state["message"]}
"""
    res = safe_llm_invoke(prompt)
    route = safe_json(res.content)
    return {"tool": route.get("tool", "log")}

# ----------------- LANGGRAPH -----------------
graph = StateGraph(GraphState)
graph.add_node("router", router)
graph.add_node("log", log_interaction_tool)
graph.add_node("edit", edit_interaction_tool)
graph.add_node("followup", suggest_followups_tool)
graph.add_node("history", fetch_hcp_history_tool)
graph.add_node("compliance", compliance_check_tool)

graph.set_entry_point("router")

graph.add_conditional_edges(
    "router",
    lambda s: s["tool"],
    {
        "log": "log",
        "edit": "edit",
        "followup": "followup",
        "history": "history",
        "compliance": "compliance",
    }
)

for node in ["log", "edit", "followup", "history", "compliance"]:
    graph.add_edge(node, END)

app_graph = graph.compile()

# ----------------- API -----------------
@app.get("/")
def home():
    return {"status": "AI CRM Backend running"}

@app.post("/chat")
def chat(data: ChatInput):
    result = app_graph.invoke({"message": data.message})

    db = SessionLocal()
    db.add(Interaction(data=result.get("result", {})))
    db.commit()
    db.close()

    return result.get("result", {})
