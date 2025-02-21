from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from dotenv import load_dotenv

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

agent_executor = create_react_agent(llm, tools)

def ai(query: str):
    events = agent_executor.stream(
        {"messages": [("system",
                       "You are a web server, serving HTML web pages. Do not use markdown for formatting. "
                       "All output must be in HTML format and will be displayed to an end user. "
                       "You need to start with doctype and html tags and provide the entire page"),
                      ("user", query)]},
        stream_mode="values",
    )
    data = ""
    for event in events:
        event["messages"][-1].pretty_print()
        data = event["messages"][-1]

    return data.content
