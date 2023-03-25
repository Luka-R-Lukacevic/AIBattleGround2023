import requests


IP = "192.168.200.100"
USERNAME = "GPT-3D"
PASSWORD = ""
headers = {"Content-Type": "application/json", }

api_default_endpoint = "http://localhost:8081"


def get_token(username, password):
    body = {"username": username, "password": password, }
    api_endpoint = api_default_endpoint + "/user/login"

    response = requests.post(url=api_endpoint, headers=headers, json=body)

    return response.json()["token"]


def create_game(_token, _id, player1_name, player2_name):
    header_auth = {'Authorization': 'Bearer ' + _token}
    body = {"gameId": _id, "playerUsernames": [player1_name, player2_name], }

    api_endpoint = api_default_endpoint + "/game/createGame"

    return requests.post(url=api_endpoint, headers={**headers, **header_auth}, json=body).json()


def join_game(game_id, _token):
    header_auth = {'Authorization': 'Bearer ' + _token}

    api_endpoint = api_default_endpoint + "/game/joinGame?gameId=" + str(game_id)

    return requests.get(url=api_endpoint, headers={**headers, **header_auth}).json()


def make_move(_token, move):
    header_auth = {'Authorization': 'Bearer ' + _token}

    api_endpoint = api_default_endpoint + "/game/doAction"

    body = {"action": move}

    return requests.post(url=api_endpoint, headers={**headers, **header_auth}, json=body).json()


if __name__ == '__main__':
    admin_token = get_token("admin", "admin")
    print(create_game(admin_token, 1, "player1", "player2")["message"])
