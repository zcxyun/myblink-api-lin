from pprint import pprint

from app.app import create_app

app = create_app()


def test_get_comments():
    with app.test_client() as e:
        rv = e.get('/cms/comment?type=400')
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200
