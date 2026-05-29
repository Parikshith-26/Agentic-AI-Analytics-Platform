# Agentic AI Analytics Platform

A multi-agent AI analytics platform that automates data analysis workflows using Large Language Models (LLMs), enabling conversational business intelligence, SQL generation, forecasting, dashboard recommendations, and AI-driven insights.

---

## Overview

The Agentic AI Analytics Platform combines multiple specialized AI agents to automate the end-to-end analytics process. Users can upload datasets and interact with them using natural language to generate insights, forecasts, SQL queries, and dashboard recommendations.

---

## Features

### Multi-Agent Architecture

* Planner Agent
* Router Agent
* Cleaning Agent
* Analysis Agent
* Feature Engineering Agent
* Insight Agent
* Forecast Agent
* Dashboard Agent
* Feedback Agent
* SQL Agent

### Analytics Capabilities

* Automated Data Cleaning
* Business Analysis & KPI Generation
* Natural Language SQL Query Generation
* Conversational Analytics
* Predictive Analytics & Forecasting
* AI Dashboard Recommendations
* Dataset-Aware Visualizations
* Memory-Driven Context Management

### AI Capabilities

* LLM-Powered Routing
* Context-Aware Responses
* Business Insight Generation
* Executive Summary Generation
* Recommendation Engine

---

## Architecture

User Query
↓
Router Agent
↓
Planner Agent
↓
Analysis Workflow
├── Cleaning Agent
├── Analysis Agent
├── Feature Agent
├── Insight Agent
├── Forecast Agent
└── Dashboard Agent
↓
Response Generation
↓
Interactive Streamlit UI

---

## Tech Stack

### AI & LLM

* Groq API
* Llama 3.1
* Multi-Agent Systems

### Data Processing

* Pandas
* NumPy
* DuckDB

### Machine Learning

* Scikit-learn

### Visualization

* Matplotlib

### Frontend

* Streamlit

### Programming Language

* Python

---

## Project Highlights

* Developed a multi-agent AI analytics platform integrating 8+ specialized AI agents for automated data cleaning, SQL generation, forecasting, and business intelligence workflows.

* Implemented LLM-powered routing and conversational analytics, reducing manual analysis effort through natural-language querying, predictive insights, and automated visualizations.

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Parikshith-26/Agentic-AI-Analytics-Platform.git

cd Agentic-AI-Analytics-Platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

## Example Queries

### SQL Analytics

* Top 10 states by total children count
* Show average enrollment by category
* Count facilities by state

### Business Insights

* What trends are visible in this dataset?
* What operational risks do you observe?
* Provide executive recommendations

### Forecasting

* Predict future enrollment trends
* Forecast future demand

---

## Future Enhancements

* Retrieval-Augmented Generation (RAG)
* PDF Document Analytics
* Vector Database Integration
* LangGraph Workflows
* CrewAI Agent Collaboration
* Automated Report Generation
* Multi-Modal Analytics

---

## Author

Parikshith

Business Analyst | AI & Data Analytics Enthusiast

GitHub: https://github.com/Parikshith-26
