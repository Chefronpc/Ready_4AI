from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


load_dotenv()

model = init_chat_model(model="gpt-4.1-nano", model_provider="openai", verbose=True)

messages = [
    SystemMessage("Odpowiadaj z humorem")
]

while True:
    user_input = input("Ty: ")
    messages.append(HumanMessage(user_input))

    response = model.invoke(messages)
    messages.append(AIMessage(response.content))

    print("Asystent: " + response.content)



