import os

# --------------------------------------------------
# SSL certificate configuration
# --------------------------------------------------

SYSTEM_CA = "/etc/ssl/certs/ca-certificates.crt"

os.environ["REQUESTS_CA_BUNDLE"] = SYSTEM_CA
os.environ["SSL_CERT_FILE"] = SYSTEM_CA
os.environ["CURL_CA_BUNDLE"] = SYSTEM_CA

print("Using certificate bundle:", SYSTEM_CA)

from dotenv import load_dotenv
from google import genai
from google.genai import types

from tools.document_search import document_search
from tools.meeting_notes_search import meeting_notes_search
from tools.memory_search import memory_search

from memory.short_term_memory import ShortTermMemory

from agent.prompts import SYSTEM_PROMPT, MEETING_BRIEF_PROMPT


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# --------------------------------------------------
# Gemini client
# --------------------------------------------------

client = genai.Client(
    api_key=api_key
)


MODEL_NAME = "gemini-3.5-flash-lite"


# --------------------------------------------------
# Short-term conversation memory
# --------------------------------------------------

conversation_memory = ShortTermMemory()


# --------------------------------------------------
# Tool functions
# --------------------------------------------------

def search_client_documents(query: str) -> str:
    """
    Search client documents using the FAISS vector store.
    """

    results = document_search(
        query,
        k=5
    )

    if not results:
        return "No relevant client documents found."

    output = []

    for result in results:

        output.append(
            f"""
Source: {result['source']}
Document Type: {result['document_type']}

{result['text']}
"""
        )

    return "\n".join(output)


def search_previous_meetings(query: str) -> str:
    """
    Search previous client meeting notes.
    """

    results = meeting_notes_search(
        query,
        k=5
    )

    if not results:
        return "No relevant meeting notes found."

    output = []

    for result in results:

        output.append(
            f"""
Source: {result['source']}

{result['text']}
"""
        )

    return "\n".join(output)


def search_long_term_memory(query: str) -> str:
    """
    Search information stored in long-term memory.
    """

    results = memory_search(
        query,
        k=5
    )

    if not results:
        return "No relevant long-term memories found."

    output = []

    for result in results:

        output.append(
            f"""
Memory Type: {result['memory_type']}

{result['text']}
"""
        )

    return "\n".join(output)


# --------------------------------------------------
# Gemini tool declarations
# --------------------------------------------------

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="search_client_documents",
                description=(
                    "Search client documents, emails, action items, "
                    "and other business documents."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="The information to search for."
                        )
                    },
                    required=["query"]
                )
            ),
            types.FunctionDeclaration(
                name="search_previous_meetings",
                description=(
                    "Search previous meeting notes for discussions, "
                    "decisions, concerns, commitments, and topics."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="The information to search for."
                        )
                    },
                    required=["query"]
                )
            ),
            types.FunctionDeclaration(
                name="search_long_term_memory",
                description=(
                    "Search long-term memory for information from "
                    "previous sessions and user preferences."
                ),
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "query": types.Schema(
                            type=types.Type.STRING,
                            description="The information to search for."
                        )
                    },
                    required=["query"]
                )
            )
        ]
    )
]


# --------------------------------------------------
# Map Gemini tool calls to Python functions
# --------------------------------------------------

TOOL_FUNCTIONS = {
    "search_client_documents": search_client_documents,
    "search_previous_meetings": search_previous_meetings,
    "search_long_term_memory": search_long_term_memory,
}


# --------------------------------------------------
# Agent
# --------------------------------------------------

def run_agent(user_request: str):

    conversation_memory.add_message(
        "user",
        user_request
    )

    chat = client.chats.create(
        model=MODEL_NAME,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools
        )
    )
    
    prompt = MEETING_BRIEF_PROMPT.format(
        client="Acme Corp",
        user_request=user_request,
        conversation_context=conversation_memory.get_context(),
        retrieved_context="The agent will retrieve the required information using the available tools."
    )

    conversation_context = conversation_memory.get_context()

    response = chat.send_message(
        f"""
        Conversation context:
        {conversation_context}

        Current user request:
        {user_request} 
        """
    )

    while response.function_calls:

        function_responses = []

        for function_call in response.function_calls:

            function_name = function_call.name
            function_args = function_call.args

            print(
                f"\n[Agent using tool: {function_name}]"
            )

            function = TOOL_FUNCTIONS.get(
                function_name
            )

            if function is None:
                tool_result = "Unknown tool requested."

            else:
                tool_result = function(
                    **function_args
                )

            function_responses.append(
                types.Part.from_function_response(
                    name=function_name,
                    response={
                        "result": tool_result
                    }
                )
            )

        response = chat.send_message(
            function_responses
        )

    final_response = response.text

    conversation_memory.add_message(
        "assistant",
        final_response
    )

    conversation_memory.save_to_long_term_memory()

    return final_response


# --------------------------------------------------
# Test agent
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 80)
    print("CLIENT MEETING AGENT")
    print("=" * 80)
    print("Type 'exit' to quit.\n")

    while True:

        request = input("You: ")

        if request.lower() == "exit":
            print("Goodbye!")
            break

        if not request.strip():
            continue

        result = run_agent(request)

        print("\nAgent:")
        print(result)
        print("\n" + "-" * 80 + "\n")
