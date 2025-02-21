from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from pydantic import BaseModel

from github_api_langgraph_demo.ai import ai

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


class Author(BaseModel):
    """Respond to the user in this format."""
    name: str
    issue_count: int
    comment_count: int


@app.route('/data', methods=['GET'])
def get_data():
    query = ("For the most prolific author of github issues, give me the number of issues they have created. "
                     "Given the author's issues, I want to know the number of comments that same author has made." )
    return ai(query, response_format=Author)


def run():
    """
    ou can get the data by using curl http://localhost:5001/data
    """
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    run()
