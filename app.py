
import os
import asyncio
import sqlite3
import streamlit as st

from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader

from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional


os.environ["GROQ_API_KEY"] = "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"
DB_PATH = "support.db"


# ---------- DATABASE ----------

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS customers(
id INTEGER,
name TEXT,
email TEXT,
plan TEXT
)
""")

cur.execute("DELETE FROM customers")

cur.executemany(
    "INSERT INTO customers VALUES (?,?,?,?)",
    [
        (1,"Ema Watson","ema@email.com","Premium"),
        (2,"Alex","alex@email.com","Basic"),
        (3,"Sarah","sarah@email.com","Standard")
    ]
)

cur.execute("""
CREATE TABLE IF NOT EXISTS support_tickets(
id INTEGER,
customer_id INTEGER,
issue TEXT,
status TEXT
)
""")

cur.execute("DELETE FROM support_tickets")

cur.executemany(
    "INSERT INTO support_tickets VALUES (?,?,?,?)",
    [
        (1,1,"Login problem","Resolved"),
        (2,1,"Payment issue","Open")
    ]
)

conn.commit()
conn.close()


def get_customer(name):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT 
        customers.name,
        customers.email,
        customers.plan,
        support_tickets.issue,
        support_tickets.status

        FROM customers

        LEFT JOIN support_tickets

        ON customers.id = support_tickets.customer_id

        WHERE customers.name LIKE ?
        """,
        (f"%{name}%",)
    )

    result = cur.fetchall()
    conn.close()
    return result

# ---------- LLM ----------

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------- LANGGRAPH ----------

class State(TypedDict):

    question: str
    result: Optional[str]

def agent(state):

    data = get_customer("Ema")

    response = llm.invoke(
        f"""
        You are a customer support assistant.
        Use this customer profile and ticket information:

        {data}

        Answer the user question clearly.
        Include customer details and past support tickets if available.

        Question:
        {state['question']}
        """
    )

    return {
        "result": response.content
    }

graph = StateGraph(State)

graph.add_node(
    "agent",
    agent
)

graph.set_entry_point("agent")

graph.add_edge(
    "agent",
    END
)

app_graph = graph.compile()

async def ask(question):

    result = await app_graph.ainvoke(
        {
            "question": question,
            "result": ""
        }
    )

    return result["result"]

# ---------- STREAMLIT ----------

st.title("🤖 Support Information Assistant")
question = st.text_input("Ask")

if st.button("Submit"):

    answer = asyncio.run(
        ask(question)
    )

    st.write(answer)
