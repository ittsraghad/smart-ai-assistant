from datetime import datetime

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv



load_dotenv()


@tool
def calculator(a: float, b: float, operation: str) -> str:
    """
    Perform basic arithmetic calculations.
    Supported operations: add, subtract, multiply, divide.
    """

    try:
        if operation == "add":
            result = a + b

        elif operation == "subtract":
            result = a - b

        elif operation == "multiply":
            result = a * b

        elif operation == "divide":
            if b == 0:
                return "Error: Cannot divide by zero."
            result = a / b

        else:
            return (
                "Error: Unsupported operation. "
                "Use add, subtract, multiply, or divide."
            )

        return f"The result of {a} {operation} {b} is {result}"

    except Exception as e:
        return f"Calculation error: {str(e)}"


@tool
def say_hello(name: str) -> str:
    """Greet the user."""

    return f"Hello {name}! I hope you are having a great day."


@tool
def get_current_datetime() -> str:
    """Return the current date and time."""

    current_time = datetime.now()

    return current_time.strftime(
        "The current date and time is %Y-%m-%d %H:%M:%S"
    )




def main():

    print("=" * 50)
    print("       SMART AI ASSISTANT")
    print("=" * 50)

    print("\nHello! I'm your AI assistant.")
    print("I can:")
    print("- Perform calculations")
    print("- Tell you the current date and time")
    print("- Remember our conversation")
    print("- Answer general questions")
    print("\nType 'quit' to exit.")
    print("Type 'clear' to clear the conversation.")
    print("=" * 50)

 
    model = ChatOpenAI(
        temperature=0
    )

 
    tools = [
        calculator,
        say_hello,
        get_current_datetime
    ]

    agent_executor = create_react_agent(
        model,
        tools
    )

 
    conversation_history = []

    while True:

        try:

            user_input = input("\nYou: ").strip()

            
            if user_input.lower() == "quit":
                print("\nAssistant: Goodbye! 👋")
                break

          
            if user_input.lower() == "clear":
                conversation_history = []

                print("\nAssistant: Conversation history cleared.")
                continue

    
            if not user_input:
                print("Assistant: Please enter a message.")
                continue

          
            conversation_history.append(
                HumanMessage(content=user_input)
            )

            print("\nAssistant: ", end="")

            response_text = ""

          
            for chunk in agent_executor.stream(
                {
                    "messages": conversation_history
                }
            ):

                if "agent" in chunk and "messages" in chunk["agent"]:

                    for message in chunk["agent"]["messages"]:

                        if message.content:

                            response_text += message.content

            print(response_text)


            conversation_history.append(
                {
                    "role": "assistant",
                    "content": response_text
                }
            )

        except Exception as e:

            print(
                f"\nAssistant: Something went wrong: {str(e)}"
            )



if __name__ == "__main__":
    main()  