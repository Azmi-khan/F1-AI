import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash" ,
    api_key = os.getenv("GOOGLE_API_KEY"),
)
def get_response(rulebook_text: str, user_question: str) -> str:
    """sents the rules and questions to gemini and recieves the answers"""
    prompt = PromptTemplate.from_template(
        """
        You are a Chief Race Strategist on an F1 pit wall.
        Answer the user's question using ONLY the provided rulebook text below.
        
        CRITICAL INSTRUCTION: Engineers usually keep it a bit more low-key and direct. 
        Do not use enthusiastic AI filler. Be concise, technical, and human. 
        If the answer is not in the text, say "Negative, not in current parameters."
        
        RULEBOOK TEXT:
        {text}
        
        QUESTION: {question}
        
        ENGINEER RESPONSE:
        """
    )
    chain = prompt | llm
    response = chain.invoke({"text": rulebook_text, "user_question": user_question})
    return response.content