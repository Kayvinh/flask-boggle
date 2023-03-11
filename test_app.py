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
            self.assertIn('table id="boggle-board"', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:

            response = client.post('/api/new-game')
            json = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertTrue(isinstance(json['game_id'], str))
            self.assertTrue(isinstance(json['board'], list))
            self.assertTrue(isinstance(json['board'][0], list))

    def test_score_word(self):
        """Test scoring a word in the game."""
        with self.client as client:

            response = client.post('/api/new-game')
            breakpoint()
            game_id = response.json['game_id']
            game = games[game_id]

            # testing 'not-on-board'
            # TODO: Reset the board to ensure the test word is not present
            response = client.post('/api/score-word',
                                   json={'game_id': game_id,
                                         'word': 'MEAL'})
            self.assertEqual({'result': 'not-on-board'}, response.json)

            # testing 'not-word'
            response = client.post('/api/score-word',
                                   json={'game_id': game_id,
                                         'word': 'ASLKdJA'})
            self.assertEqual({'result': 'not-word'}, response.json)

            # testing 'ok'
            game.board[0] = ['C', 'A', 'T', 'A', 'B']
            # TODO: Can do this when setting the board above for the not-on-board test

            response = client.post('/api/score-word',
                                   json={'game_id': game_id,
                                         'word': 'CAT'})
            self.assertEqual({'result': 'ok'}, response.json)