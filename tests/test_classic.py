from app.app import create_app
from tests.utils import get_token
from pprint import pprint

app = create_app()


def test_get_latest():
    with app.test_client() as c:
        rv = c.get('v1/classic/latest', headers={
            'Authorization': 'Bearer ' + get_token()})
        json_data = rv.get_json()
        pprint(json_data)
        assert rv.status_code == 200
