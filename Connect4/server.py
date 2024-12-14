import uuid
import socket
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

from game import Connect4


class Connect4Server:
    """
    Game Server for Connect4.

    Hosts a Flask-based API to manage game logic and allow players to interact remotely.

    Attributes:
        game (Connect4): Instance of the Connect4 game.
        app (Flask): Flask application instance for handling HTTP requests.
    """

    def __init__(self):
        """
        Initialize the Connect4 server.

        Sets up the Flask app, Swagger documentation, and API routes.
        """
        self.game = Connect4()
        self.app = Flask(__name__)

        swagger_url = '/swagger/connect4/'
        api_url = '/static/swagger.json'
        swaggerui_blueprint = get_swaggerui_blueprint(
            swagger_url,
            api_url,
            config={'app_name': "Connect 4 API"}
        )
        self.app.register_blueprint(swaggerui_blueprint, url_prefix=swagger_url)

        self.setup_routes()

    def setup_routes(self) -> None:
        """
        Define the API routes for interacting with the Connect4 game.
        """

        @self.app.route('/')
        def index():
            return "Welcome to the Connect 4 API!"

        @self.app.route('/connect4/status', methods=['GET'])
        def get_status():
            """
            Get the current status of the game.

            Returns:
                JSON response with game status, including active player, winner, and turn.
            """
            data = self.game.get_status()
            return jsonify(data), 200

        @self.app.route('/connect4/register', methods=['POST'])
        def register_player():
            """
            Register a player in the game.

            Request Body:
                - player_id (str): Unique identifier for the player.

            Returns:
                JSON response with the player's assigned icon ('X' or 'O').
            """
            data = request.get_json()
            player_id = data.get('player_id')
            if not player_id:
                return jsonify({'error': 'Invalid input'}), 400

            icon = self.game.register_player(player_id)
            if icon:
                return jsonify({'player_icon': icon}), 200
            else:
                return jsonify({'error': 'Game Full'}), 400

        @self.app.route('/connect4/board', methods=['GET'])
        def get_board():
            """
            Get the current state of the game board.

            Returns:
                JSON response with the board as a list.
            """
            board = self.game.get_board()
            board_list = board.flatten().tolist()
            return jsonify({'board': board_list})

        @self.app.route('/connect4/make_move', methods=['POST'])
        def make_move():
            """
            Make a move in the game.

            Request Body:
                - player_id (str): Unique identifier for the player.
                - column (int): Column where the player wants to place their piece.

            Returns:
                JSON response indicating success or failure of the move.
            """
            data = request.get_json()
            player_id = data.get('player_id')
            column = data.get('column')

            if self.game.check_move(column, player_id):
                return jsonify({"success": True}), 200
            else:
                return jsonify({'error': 'Invalid input'}), 400

    def run(self, debug: bool = True, host: str = '0.0.0.0', port: int = 5000) -> None:
        """
        Start the Flask server.

        Parameters:
            debug (bool): Whether to run the server in debug mode.
            host (str): The host address to bind the server to.
            port (int): The port to run the server on.
        """
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"Server is running on {local_ip}:{port}")
        self.app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    server = Connect4Server()
    server.run()
