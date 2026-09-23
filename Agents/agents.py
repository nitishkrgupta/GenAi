from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

@tool
def make_uppercase(text : str) -> str:
    """Convert the text into uppercase"""
    print(f"uppercase tool called :  make_uppercase -> {text}")
    result = text.upper()
    print(f"tool result :  {result}")
    return result

@tool
def count_characters(text : str) -> int:
    """Count the characters from the given text"""
    print(f"count tool called :  count_characters -> {text}")
    result = len(text)
    print(f"Count tool result : {result}")
    return result

@tool
def reverse_text(text: str) -> str:
    """Reverse the given text"""
    print(f"reverse tool called: {text}")
    result = text[::-1]
    print(f"tool result: {result}")
    return result

@tool
def check_even_odd(num : int) -> str:
    """Check the given number is even or odd"""
    print(f"check even odd tool called : {num}")
    if num % 2 == 0:
        return "even"
    return "odd"

@tool
def square_number(num: int) -> int:
    """Return the square of a number"""
    print(f"square tool called: {num}")
    result = num ** 2
    print(f"Square result: {result}")
    return result

@tool
def remove_spaces(text: str) -> str:
    """Remove all spaces from the given text"""
    print(f"remove spaces tool called: {text}")
    result = text.replace(" ", "")
    print(f"Tool result: {result}")
    return result

tools = [make_uppercase, count_characters, check_even_odd, reverse_text, square_number, remove_spaces]
# llm = ChatOllama(
#     model = 'qwen2.5:1.5b',
#     temperature=0
# )
llm = ChatGoogleGenerativeAI(
    model='gemini-3.5-flash-lite'
)
tool_agent = create_agent(llm, tools)

class AgentState(TypedDict):
    question : str
    decision : str
    tool_result : str
    answer : str

def agent(state : AgentState):
    question = state['question']
    prompt = f"""You are an AI agent
    user question : {question}
    decide what to do
    If the question requires any of these operations:
    - uppercase conversion
    - character counting
    - even/odd checking
    - reverse the text
    - squared of a number
    - remove spaces from the text
    respond with exactly:

    USE_TOOLS
    
    otherwise respond exactly:
    DIRECT_ANSWER
    
    do not provide any explanations"""

    response = llm.invoke(prompt)
    decision = response.text       # response.content when invoking ollama model

    return {
        'decision' : decision
    }

def use_tool(state : AgentState):
    question = state['question']

    result = tool_agent.invoke({
        'messages': [
        {
            'role': 'user',
            'content': question
        }
    ]
    })
    tool_result = result['messages'][-1].content
    return {
        'tool_result' : str(tool_result)
    }

def final_answer(state : AgentState):
    question = state['question']
    tool_result = state.get('tool_result', "")
    if tool_result:
        prompt = f"""
    Answer the user's question
    qeustion : {question}
    result :  {tool_result}
Give only the final answer"""
        response = llm.invoke(prompt)
        return {
            'answer' : response.text
        }
    else:
        prompt = f"""
Answer the question directly
question : {question}"""
        response = llm.invoke(prompt)
        return {
            "answer" : response.text
        }

def router(state : AgentState):
    decision = state['decision']

    if "USE_TOOLS" in decision:
        return 'tool'
    return 'answer'

graph = StateGraph(AgentState)
graph.add_node('agent', agent)
graph.add_node('tool', use_tool)
graph.add_node('answer', final_answer)
graph.add_edge(START, 'agent')
graph.add_conditional_edges('agent',
                            router,{
                                'tool' : 'tool',
                                'answer' : 'answer'
                            })
graph.add_edge('tool', 'answer')
graph.add_edge('answer', END)

app = graph.compile()

result = app.invoke({
    "question": input("Enter your query : \n"),
    "decision": "",
    "tool_result": "",
    "answer": ""
})
print("Agent Answer:")
print(result["answer"])