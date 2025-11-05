from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

load_dotenv()
store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
        store[session_id].add_message(SystemMessage("Odpowiadaj z humorem"))
    return store[session_id]

model = init_chat_model(model="gpt-4.1-nano", model_provider="openai", verbose=True)
model_with_history = RunnableWithMessageHistory(model, get_session_history)

config = {"configurable": {"session_id": "Ready4AI"}}

while True:
    user_input = input("Ty: ")
    response = model_with_history.invoke(user_input, config)
    
    print("Asystent: " + response.content)



