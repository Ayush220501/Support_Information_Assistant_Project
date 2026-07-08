# 🤖 Support Information Assistant — Gen AI Multi-Agent System

## Overview

Support Information Assistant is a Generative AI-powered application that helps customer support teams retrieve customer information and company policy details using natural language queries.
The system uses SQL data for customer records and a vector database for policy document search.
---
## Features
* Retrieve customer profile information
* Retrieve past support ticket details
* Search company policies using RAG
* Generate AI-based responses using LLM
* Simple Streamlit interface
---
## Tech Stack
* Python
* LangChain
* LangGraph
* Groq LLM
* SQLite Database
* Chroma Vector Database
* HuggingFace Embeddings
* Streamlit
* MCP Server
---
## Project Structure
```
Support_Information_Assistant_Project/
├── app.py
├── mcp_server.py
├── support_information_assistant.py
├── requirements.txt
---
## Setup
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Add Groq API Key
Set your Groq API key before running the application.

### Run Application

```bash
streamlit run app.py
```
---
## Example Queries
**Customer Information**

```
Give me a quick overview of customer Ema's profile and past support ticket details.
```

**Policy Search**
```
What is the current refund policy?
```
---
## Demo Video
Add demo link:
```
https://youtu.be/d-aOQ6FxA3gYOUR_VIDEO_LINK
```
