from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config["TESTING"] = True
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]


class FlaskTests(TestCase):
    def setUp(self):
        with app.test_client() as client:
            client.get("/")

    def test_start_game(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>Boggle</h1>", html)

    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session["board"] = [
                    ["G", "T", "W", "Y", "F"],
                    ["Z", "B", "Q", "N", "M"],
                    ["Y", "I", "L", "H", "W"],
                    ["M", "P", "Z", "Y", "N"],
                    ["Z", "S", "Q", "W", "O"],
                ]
            resp = client.get("/check?guess=now")
            self.assertEqual(resp.json["result"], "ok")

    def test_check_fake_word(self):
        with app.test_client() as client:
            client.get("/")
            resp = client.get("/check?guess=asdfsd")
            self.assertEqual(resp.json["result"], "not-a-word")

    def test_check_invalid_word(self):
        with app.test_client() as client:
            client.get("/")
            resp = client.get("/check?guess=inconsequential")
            self.assertEqual(resp.json["result"], "not-on-board")
