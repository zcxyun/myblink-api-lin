from app.app import create_app
from pprint import pprint

app = create_app()


def test_like():
    with app.test_client() as e:
        rv = e.post('/v1/like', json={
            'art_id': 224,
            'type': 400
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201


def test_unlike():
    with app.test_client() as e:
        rv = e.post('/v1/like/cancel', json={
            'art_id': 224,
            'type': 400
        })
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 201
