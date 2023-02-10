from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, marshal, fields

# Initialize Flask
app = Flask(__name__)
api = Api(app)

games = [{
    "id": 1,
    "title": "Sims 4",
    "developer": "Electronic Arts",
    "publisher": "Electronic Arts",
    "metacritic_rating": 70,
    "ign_rating": 7.5,
    "platforms": ["PC", "Mac", "X-Box", "PS4"]
},
    {
        "id": 2,
        "title": "Story of Seasons: Trio of Towns",
        "developer": "Marvelous",
        "publisher": "XSeed Games",
        "metacritic_rating": 74,
        "ign_rating": 7.7,
        "platforms": ["3DS"]
    }
]

gameFields = {
    "id": fields.Integer,
    "title": fields.String,
    "developer": fields.String,
    "publisher": fields.String,
    "metacritic_rating": fields.Float,
    "ign_rating": fields.Float,
    "platforms": fields.List(fields.String)
}


class Game(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("title", type=str, required=True, location="json")
        self.reqparse.add_argument("developer", type=str, required=True, location="json")
        self.reqparse.add_argument("publisher", type=str, required=True, location="json")
        self.reqparse.add_argument("metacritic_rating", type=float, location="json")
        self.reqparse.add_argument("ign_rating", type=float, location="json")
        self.reqparse.add_argument("platforms", type=str, required=True, action="append", location="json")
        super(Game, self).__init__()

    def game_search(self, id):
        game = [game for game in games if game['id'] == id]
        if len(game) == 0:
            abort(404)
        return game

    def get(self, id):
        game = self.game_search(id)
        return {"game": marshal(game[0], gameFields)}

    def put(self, id):
        game = self.game_search(id)
        game = game[0]

        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                game[k] = v
        return {"game": marshal(game, gameFields)}

    def delete(self, id):
        game = self.game_search(id)
        games.remove(game[0])

        return 201


class GameList(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser(bundle_errors=True)
        self.reqparse.add_argument("title", required=True, type=str, help="The title of the game must be provided",
                                   location="json")
        self.reqparse.add_argument("developer", required=True, help="The developer of the game must be provided",
                                   location="json", type=str)
        self.reqparse.add_argument("publisher", required=True, help="The publisher of the game must be provided",
                                   location="json", type=str)
        self.reqparse.add_argument("metacritic_rating", type=float, required=False, location="json")
        self.reqparse.add_argument("ign_rating", type=float, required=False, location="json")
        self.reqparse.add_argument("platforms", required=True, help="The platforms of the game must be provided",
                                   location="json", type=str, action="append")

    def get(self):
        return {"games": [marshal(game, gameFields) for game in games]}

    def post(self):
        args = self.reqparse.parse_args()
        game = {
            "id": games[-1]['id'] + 1 if len(games) > 0 else 1,
            "title": args["title"],
            "developer": args["developer"],
            "publisher": args["publisher"],
            "metacritic_rating": args["metacritic_rating"],
            "ign_rating": args["ign_rating"],
            "platforms": args["platforms"]
        }
        games.append(game)
        return {"game": marshal(game, gameFields)}, 201


api.add_resource(GameList, "/games")
api.add_resource(Game, "/game/<int:id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
