from app.app import create_app
from pprint import pprint

app = create_app()


def test_get_latest():
    with app.test_client() as c:
        rv = c.get('v1/classic/latest')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_next():
    with app.test_client() as c:
        rv = c.get('v1/classic/2/next')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_previous():
    with app.test_client() as c:
        rv = c.get('v1/classic/6/previous')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_detail():
    with app.test_client() as e:
        rv = e.get('v1/classic/300/2')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_like():
    with app.test_client() as e:
        rv = e.get('v1/classic/300/2/favor')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200


def test_get_favor():
    with app.test_client() as e:
        rv = e.get('v1/classic/favor?page=1&count=2')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200
