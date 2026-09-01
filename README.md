# Client Meeting Agent

An AI-powered client meeting preparation agent that helps managers prepare for upcoming client meetings by combining information from client documents, previous meeting notes, long-term memory, and current conversation context.

## Overview

The Client Meeting Agent uses Google's Gemini model together with FAISS-based semantic search to retrieve relevant business information and generate a concise meeting brief.

The agent can identify:

* Client overview
* Recent developments
* Previous meeting discussions
* Open action items
* Risks and blockers
* Opportunities
* Key stakeholders
* Recommended talking points
* Recommended next steps

## Architecture

```text
                    User Request
                         |
                         v
              +---------------------+
              |   Gemini AI Agent   |
              +---------------------+
                         |
          +--------------+--------------+
          |              |              |
          v              v              v
   Client Documents  Meeting Notes  Long-Term Memory
      FAISS Search    FAISS Search    FAISS Search
          |              |              |
          +--------------+--------------+
                         |
                         v
                Retrieved Context
                         |
                         v
                Gemini Reasoning
                         |
                         v
                 Meeting Brief
```

## Project Structure

```text
client_meeting_agent/
│
├── agent/
│   ├── agent.py
│   ├── prompts.py
│   └── __init__.py
│
├── memory/
│   ├── memory_store.py
│   ├── short_term_memory.py
│   ├── memory.index
│   ├── memory_metadata.json
│   └── __init__.py
│
├── tools/
│   ├── document_search.py
│   ├── meeting_notes_search.py
│   ├── memory_search.py
│   └── __init__.py
│
├── vector_store/
│   ├── acme_documents.index
│   └── metadata.json
│
├── requirements.txt
├── .env
└── README.md
```

## Key Components

### Gemini Agent

`agent/agent.py` contains the main AI agent.

It is responsible for:

* Receiving user requests
* Calling the appropriate search tools
* Combining retrieved information
* Maintaining short-term conversation context
* Generating the final meeting brief

### Client Document Search

`tools/document_search.py` performs semantic search over client-related documents using FAISS and sentence embeddings.

### Meeting Notes Search

`tools/meeting_notes_search.py` searches previous meeting notes to retrieve:

* Previous discussions
* Decisions
* Commitments
* Concerns
* Action items

### Long-Term Memory

`memory/memory_store.py` stores and searches persistent memories using FAISS.

Memories can contain information that should be available across different application sessions.

### Short-Term Memory

`memory/short_term_memory.py` maintains the current conversation context while the application is running.

## Technologies Used

* Python
* Google Gemini API
* Google GenAI SDK
* Sentence Transformers
* FAISS
* NumPy
* python-dotenv

## Embedding Model

The project uses:

```text
sentence-transformers/all-MiniLM-L6-v2
```

The model generates 384-dimensional sentence embeddings that are stored and searched using FAISS.

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd client_meeting_agent
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Do not commit your `.env` file or expose your API key publicly.

## Running the Agent

Run the application as a Python module:

```bash
python -m agent.agent
```

You will see:

```text
CLIENT MEETING AGENT
Type 'exit' to quit.

You:
```

Example:

```text
You: Prepare me for my meeting with Acme Corp.
```

The agent retrieves relevant information and produces a structured meeting brief.

To exit:

```text
You: exit
```

## Example Output

```text
# Meeting Brief

## Client Overview
Summary of the client and key stakeholders.

## Recent Developments
Recent developments relevant to the meeting.

## Previous Discussions
Important topics and decisions from previous meetings.

## Open Action Items
Outstanding tasks and owners.

## Risks / Blockers
Issues that may affect the project or relationship.

## Opportunities
Potential expansion or business opportunities.

## Recommended Talking Points
Important topics to discuss during the meeting.

## Recommended Next Steps
Actions to take after the meeting.
```

## Agent Workflow

1. User submits a meeting preparation request.
2. Gemini analyzes the request.
3. Gemini selects the appropriate search tools.
4. Relevant client information is retrieved using semantic search.
5. Retrieved information is provided back to Gemini.
6. Gemini combines the information with conversation context.
7. The agent generates a concise meeting brief.
8. The response is stored in short-term conversation memory.

## Security

Sensitive credentials should be stored in environment variables.

The following should **not** be committed to Git:

```text
.env
venv/
__pycache__/
*.pyc
```

These files should be excluded through `.gitignore`.

## Future Improvements

Potential improvements include:

* Web interface for the meeting agent
* Uploading new client documents directly
* Automatic meeting transcript ingestion
* Calendar integration
* Automatic action-item extraction
* Meeting follow-up email generation
* Improved memory management
* Authentication and multi-user support
* Deployment as an API service

## Author

Client Meeting Agent project built using Python, Gemini, FAISS, and semantic search.
