from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent

@tool #tool(get_word_count)
def get_word_count(text: str) -> str:
    """Count the number of words in the given text."""
    return f"{len(text.split())} words"
@tool
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]
tools = [reverse_text,get_word_count]

llm = ChatGoogleGenerativeAI(model = 'gemini-3.7-flash')
agent = create_agent(llm, tools)

store = {}

def get_session_history(session_id):
    if session_id not in store:
        store[session_id] = []
    return store[session_id]

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
        history = get_session_history(session_id)
        history.append({'user_query' : user_input})

        res = agent.invoke({"messages": [
                {"role": "user", "content": history}]})
        res = res["messages"][-1].text
        
        history.append({'response' : res})
        store[session_id] = history
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

print(store)