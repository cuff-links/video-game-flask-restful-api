import json
from api import app


class TestGamesApi:

    def test_get_all_games(self):
        with app.test_client() as client:
            response = client.get('/games')
            res = json.loads(response.data.decode('utf-8')).get('games')
            assert type(res[0]) is dict
            assert type(res[1]) is dict
            assert res[0]['title'] == 'Sims 4'
            assert res[1]['title'] == 'Story of Seasons: Trio of Towns'
            assert len(res) == 2
            assert type(res) is list

    def test_get_individual_game(self):
        with app.test_client() as client:
            response = client.get('/game/1')
            res = json.loads(response.data.decode('utf-8')).get('game')
            assert res['title'] == 'Sims 4'
            assert len(res['platforms']) == 4

    def test_update_game(self):
        updated_game = {
            "title": "Sims 4: Double Deluxe",
            "developer": "Electronic Arts",
            "publisher": "Electronic Arts",
            "metacritic_rating": 70,
            "ign_rating": 7.5,
            "platforms": ["PC", "Mac", "X-Box", "PS4"]
        }
        with app.test_client() as client:
            response = client.put('/game/1', json=updated_game)
            assert response.status_code == 200
            games_res = client.get('/games')
            games = json.loads(games_res.data.decode('utf-8')).get('games')
            assert len(games) == 2
            assert games[0]['title'] == 'Sims 4: Double Deluxe'

    def test_game_not_found(self):
        with app.test_client() as client:
            response = client.get('/game/fake')
            assert response.status_code == 404

    def test_post_new_game(self):
        game = {
            "title": "Subnautica",
            "developer": "Unknown Worlds",
            "publisher": "Unknown Worlds",
            "metacritic_rating": 87,
            "ign_rating": 9.1,
            "platforms": ["PC", "Xbox One", "PS4", "Switch"]
        }
        with app.test_client() as client:
            response = client.post('/games', json=game)
            assert response.status_code == 201

    def test_delete_game(self):
        with app.test_client() as client:
            response = client.delete('/game/2')
            assert response.status_code == 200
            games_res = client.get('/games')
            games = json.loads(games_res.data.decode('utf-8')).get('games')
            assert len(games) == 2
            assert games[0]['title'] == 'Sims 4: Double Deluxe'
            assert games[1]["title"] == "Subnautica"
