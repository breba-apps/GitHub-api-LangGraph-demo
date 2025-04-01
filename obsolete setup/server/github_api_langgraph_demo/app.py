from pathlib import Path

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
    # Wow where is the logic?
    return ai(Path("my_app.txt").read_text())


def run():
    """
    You can get the data by using curl http://localhost:5001/data
    """
    app.run(debug=True, port=5001)


if __name__ == '__main__':
    run()
