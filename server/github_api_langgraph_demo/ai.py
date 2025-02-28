import json
from typing import Type

from dotenv import load_dotenv
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel

load_dotenv()

# Initialize GitHub API Wrapper
github = GitHubAPIWrapper()

# Instantiate GitHub Toolkit
toolkit = GitHubToolkit.from_github_api_wrapper(github)

# View available tools
all_tools = toolkit.get_tools()
for tool in all_tools:
    print(tool.name)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

tools = [setattr(tool, "name", tool.mode) or tool for tool in toolkit.get_tools()]


def ai(query: str, response_format: Type[BaseModel]):
    agent_executor = create_react_agent(llm, tools, response_format=response_format)
    events = agent_executor.stream(
        {"messages": [("user", query)]},
        stream_mode="values",
    )
    event = {}
    for event in events:
        event["messages"][-1].pretty_print()

    structured_response = event.get("structured_response")
    data = {"data": [structured_response.model_dump()]}
    print(data)
    return json.dumps(data)
