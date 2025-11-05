from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv()

model = init_chat_model(model="gpt-4.1-nano", model_provider="openai", verbose=True)

chat_history = InMemoryChatMessageHistory()
chat_history.add_message(SystemMessage("Odpowiadaj z humorem"))

while True:
    user_input = input("Ty: ")
    chat_history.add_message(HumanMessage(user_input))

    response = model.invoke(chat_history.messages)
    chat_history.add_message(AIMessage(response.content))

    print("Asystent: " + response.content)



