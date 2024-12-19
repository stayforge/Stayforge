from flask import Flask, send_from_directory, Blueprint, Response
import os

# Get the absolute path of the script
script_path = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
bp = Blueprint('demo-plugin', __name__)

@bp.route('/', methods=['GET'])
def plugin():
    """
    Serves the 'plugin.yaml' file located in the script directory.
    """
    return send_from_directory(script_path, 'plugin.yaml')

@bp.route('/permissions.json', methods=['GET'])
def permissions():
    """
    Serves the 'permissions.json' file located in the script directory.
    """
    return send_from_directory(script_path, 'permissions.json')


# Register the blueprint with a namespace and prefix
app.register_blueprint(bp, url_prefix='/demo-namespace/demo-plugin')

if __name__ == '__main__':
    # Run the Flask application on port 5001
    app.run(port=5001)