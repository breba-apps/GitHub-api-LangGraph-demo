import json

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from langchain_community.agent_toolkits.github.toolkit import GitHubToolkit
from langchain_community.utilities.github import GitHubAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel


class Author(BaseModel):
    """Respond to the user in this format."""
    name: str
    issue_count: int
    comment_count: int

# Load environment variables from .env
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

agent_executor = create_react_agent(llm, tools, response_format=Author)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/data', methods=['GET'])
def get_data():
    # example_query = "Who is the most prolific author of issues. Respond in JSON with author_name as the field. Don't use markdown, your output will be sent to a software program to use. If making a function call, provide explanation for the function call. "
    example_query = ("For the most prolific author of github issues, give me the number of issues they have created. "
                     "Given the author's issues, I want to know the number of comments that same author has made." )

    events = agent_executor.stream(
        {"messages": [("user", example_query)]},
        stream_mode="values",
    )
    event = {}
    for event in events:
        event["messages"][-1].pretty_print()

    structured_response = event.get("structured_response")
    data = {"data": [structured_response.model_dump()]}
    print(data)
    return json.dumps(data)


def run():
    """
    ou can get the data by using curl http://localhost:5001/data
    """
    app.run(debug=True, port=5001)

if __name__ == '__main__':
    run()