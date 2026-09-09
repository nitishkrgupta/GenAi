from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

llm = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash-lite'
)

prompt = ChatPromptTemplate.from_messages([
    ('system', "you are a helpful assistant"),
    MessagesPlaceholder(variable_name='history'),
    ('human', "{input}")
]
)
parser = StrOutputParser()

chain = prompt | llm | parser

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key='input',
    history_messages_key='history'
)

user = input("Enter user : ")

while True:
    user_input = input("Enter message : ")
    if user_input.lower() in ['quit', 'exit']:
        break
    chat1 = chain_with_memory.invoke(
        {'input' : user_input},
        config={"configurable" : {"session_id" : user}}
    )
    print("Me : ", user_input)
    print("Bot : ", chat1)