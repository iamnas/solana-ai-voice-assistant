# agent/agent.py

from agent.openai_agent.gpt_agent import GptAgent
from agent.local_agent.local_llm import LocalLlm
from agent.rag_agent.rag import RagAgent

def agent(text, mode="openai"):
    if mode == "openai":
        agent = GptAgent()
    elif mode == "local":
        agent = LocalLlm()
    elif mode == "rag":
        agent = RagAgent()
    else:
        return "Mode not recognized"
    
    return agent.get_response(text)
