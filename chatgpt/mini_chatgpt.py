from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser


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

"""
start
session_id = session_1
user input
do you want to continue the session
yes
no
create new session or exit

"""
session_id = 1
print("-----START-----")
while True:
    user_input = input('''
    Enter your query ....
    or
    for exit type => exit
    Query : \n''').lower()
    if user_input == 'exit':
        print("Thank You")
        break
    try:
        res = chain_with_memory.invoke(
            {'input' : user_input},
            config={"configurable" : {"session_id" : session_id}}
        )
        print(f'''
        User : {user_input}
        Bot : {res}''')
    except Exception as e:
        print(f"Error : {e}")
        break
    new_session = input("""
If you want to continue with same session type anything except 'no'
for new session type  => No\n""").lower()
    if new_session == "no":
        session_id += 1
    