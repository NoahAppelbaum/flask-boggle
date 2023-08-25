from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- index rendered -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            # make a post request to /api/new-game
            response = client.post("/api/new-game")
            # get the response body as json using .get_json()
            response_data = response.get_json()
            print("response data", response_data)

            # test that the game_id is a string
            self.assertIsInstance(response_data["game_id"], str)
            # test that the board is a list
            self.assertIsInstance(response_data["board"], list)
            # test that the game_id is in the dictionary of games (imported from app.py above)
            self.assertIn(response_data["game_id"], games)

    def test_score_word(self):
        """Test if word is valid"""

        with self.client as client:

            # make a post request to /api/new-game
            response = client.post("/api/new-game")
            # get the response body as json using .get_json()
            response_data = response.get_json()
            # find that game in the dictionary of games (imported from app.py above)
            game = games[response_data['game_id']]
            # manually change the game board's rows so they are not random
            game.board = ["C","A","T"], ["O", "X", "X"], ["X", "G", "X"]

            # test to see that a valid word on the altered board returns {'result': 'ok'}
            word1 = client.post('/api/score-word',
                                json={'game_id':response_data['game_id'],
                                      'word':'CAT'})

            self.assertEqual(word1.get_json(),{'result': 'ok'})
            # test to see that a valid word not on the altered board returns {'result': 'not-on-board'}
            word2 = client.post('/api/score-word',
                                json={'game_id':response_data['game_id'],
                                      'word':'DOG'})

            self.assertEqual(word2.get_json(),{'result': 'not-on-board'})
            # test to see that an invalid word returns {'result': 'not-word'}
            word3 = client.post('/api/score-word',
                                json={'game_id':response_data['game_id'],
                                      'word':'ABC'})

            self.assertEqual(word3.get_json(),{'result': "not-word"})
