from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph

# This sets up our shared memory. The crucial part here is the add_messages reducer. This tells LangGraph that whenever a node updates the messages list, it should append the new message rather than overwriting the entire list.

class State(TypedDict):
    messages: Annotated[ list, add_messages ]

def chatbot_node(state : State):
    print("\n\n\n inside chatbot node ", state )
    return{ "messages": [ "This message is returned from chatbot_node...!" ] }

def sample_node(state: State):
    print("\n\n\n inside sample node", state)
    return {"messages": [ "This message got returned from sample node...!" ]}

graph_builder = StateGraph(State)

graph_builder.add_node("ChatBot", chatbot_node)
graph_builder.add_node("SampleNode", sample_node)

graph_builder.add_edge(START, "ChatBot")
graph_builder.add_edge("ChatBot", "SampleNode")
graph_builder.add_edge("SampleNode", END)

graph = graph_builder.compile()

update_state = graph.invoke({
    "messages": ["This is an invoked message...!"]
})

print("\n\n Updated state: ", update_state)

