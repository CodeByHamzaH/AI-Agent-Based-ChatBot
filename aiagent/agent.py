import os
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY=os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY=os.environ.get("TAVILY_API_KEY")
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY")


#Step2: Setup LLM & Tools
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.chat_models import ChatOllama

openai_llm=ChatOpenAI(modwel="gpt-4o-mini")
# groq_llm=ChatGroq(model="llama-3.3-70b-versatile")
ollam_llm = ChatOllama(model="llama3.2:1b")

search_tool=TavilySearchResults(max_results=2)


#Step3: Setup AI Agent with Search tool functionality
from langgraph.prebuilt import create_react_agent
from langchain_core.messages.ai import AIMessage

system_prompt="Act as an AI chatbot who is smart and friendly"


def get_response_from_ai_agent(llm_id, query, allow_search, system_prompt, provider):
    if provider=="Groq":
        llm=ChatGroq(model=llm_id)
    elif provider=="OpenAI":
        llm=ChatOpenAI(model=llm_id)
    elif provider == "ollama":
        llm=ChatOllama(model=llm_id)

    tools=[TavilySearchResults(max_results=2)] if allow_search and provider!="ollama" else []

    if provider=="ollama" and allow_search:
        internet_search = TavilySearchResults(max_results=2).run({"query":query[0]})
        system_prompt = str(f"{system_prompt}\n\nSearch Result:\n{str(internet_search[0])}")
    
    agent=create_react_agent(
        model=llm,
        tools=tools,
        state_modifier=system_prompt
    )
    state={"messages": query}
    response=agent.invoke(state)
    messages=response.get("messages")
    ai_messages=[message.content for message in messages if isinstance(message, AIMessage)]
    return ai_messages[-1]