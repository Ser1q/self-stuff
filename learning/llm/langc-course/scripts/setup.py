from dotenv import load_dotenv
from importlib.metadata import version

load_dotenv()

core_version = version("langchain-core")
lg_version = version("langgraph")
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

print(f"langchain-core version: {core_version}")
print(f"langgraph version: {lg_version}")

def main():
    llm_openai = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    response_openai = llm_openai.invoke("Say 'setup complete' in one word")
    print(f"ChatOpenAI response: {response_openai}")
    
    # llm_anthropic = ChatAnthropic(model_name="claude-haiku-4-5-20251001", temperature=0)
    # response_anthropic = llm_anthropic.invoke("Say 'setup complete' in one word")
    # print(f"ChatAnthropic response: {response_anthropic}")

    print("Setup complete!")

if __name__ == "__main__":
    main()
