# CortexHub: Modular LLM Agent Suite

A powerful, extensible assistant suite built with open-source LLMs via Ollama and LangChain. CortexHub hosts four intelligent agents that specialize in general chat, image document parsing, course generation, and SQL support — each with persistent session memory and strict role boundaries.

---

## Key Modules

CortexHub is composed of four specialized agents:

---

### 1. General Chat Assistant (`chat_response`)

A friendly, context-aware chatbot designed to handle broad conversations with memory retention and clarification-first behavior.

- **Model:** `llama3.2:1b`
- **Behaviors:**
  - Retains session memory using `ConversationBufferMemory`
  - Follows safe, user-first instruction set
  - Avoids guessing — asks clarifying questions when unsure

---

### 2. Image Document Analyzer (image_analyzer.py)
A multimodal vision agent that extracts structured information from uploaded government ID images using LLMs.

- **Model:** llama3.2-vision:11b
- **Input:** UploadFile (image) → encoded to base64 with MIME prefix
- **Prompt Type:** Multimodal input (text + image_url) using HumanMessage
- **Output:** Descriptive analysis of the uploaded image
- **Use Case:** Parsing a government-issued ID (like Aadhaar, PAN, or license) to describe the image contents in natural language (not JSON extraction in current version).
---

### 3. AI Course Builder (`build_course`)

Reads uploaded files (PDF, DOCX, TXT) and constructs a course plan with modules, duration, and evaluation strategies.

- **Model:** `llama3.2:1b`
- **File Types:** `.pdf`, `.docx`, `.txt`
- **Outputs:**
  - Module-wise structure
  - Content types and durations
  - Quiz, assignment, and project ideas

---

### 4. SQL Expert Bot (`answer_sql`)

A strict SQL-only agent that assists with SQL queries and syntax while refusing to answer unrelated questions.

- **Model:** `gemma3:12b`
- **Behavior:**
  - Accepts only SQL-related queries
  - Gracefully declines off-topic input
  - Offers help with query formulation and logic

---

## Technologies

- **LangChain** (Chains, Prompts, Memory)
- **Ollama** (local open-source LLM inference)
- **Python** (async functions for modular use)
- **Session Memory** (conversation-aware)
