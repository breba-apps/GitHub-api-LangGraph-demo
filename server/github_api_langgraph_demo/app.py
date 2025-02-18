from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

from github_api_langgraph_demo.ai import ai

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


@app.route('/data', methods=['GET'])
def get_data():
    return ai(
        "Given the most prolific author of github issues, give me the date the last issue was created. Respond in JSON that looks like this: { \"most_active_author\": \"Some name\", \"date\": \"YYYY-MM-DD\", \"issue_title\": \"Some title\" }."
    )


def run():
    """
    ou can get the data by using curl http://localhost:5001/data
    """
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    run()
