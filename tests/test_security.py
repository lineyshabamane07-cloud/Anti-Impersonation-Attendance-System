
import os

os.environ["USE_MOCK"] = "true"

from app import create_app
from config import Config
from services import auth_service


def make_client():

    auth_service._failures.clear()

    return create_app().test_client()


def with_csrf(client):

    with client.session_transaction() as s:
        s["csrf"] = "test-token"


def post_login(client, user_code, password):

    return client.post(
        "/login",
        data={
            "user_code": user_code,
            "password": password,
            "csrf": "test-token"
        }
    )


def test_anonymous_is_sent_to_login():

    r = make_client().get("/faculty/dashboard")

    assert r.status_code == 302
    assert "/login" in r.headers["Location"]


def test_wrong_role_is_forbidden():

    cases = [
        ("student", "/faculty/dashboard"),
        ("faculty", "/student/dashboard"),
        ("student", "/admin/dashboard"),
        ("faculty", "/admin/dashboard")
    ]

    for role, url in cases:

        client = make_client()

        client.get(f"/dev/login/{role}")

        assert client.get(url).status_code == 403, (role, url)


def test_good_login_goes_to_the_right_dashboard():

    client = make_client()

    with_csrf(client)

    r = post_login(client, "F001", "demo123")

    assert r.status_code == 302
    assert r.headers["Location"].endswith("/faculty/dashboard")


def test_bad_password_is_refused():

    client = make_client()

    with_csrf(client)

    r = post_login(client, "F001", "wrong")

    assert r.status_code == 200
    assert b"Wrong ID or password" in r.data


def test_login_without_csrf_token_is_refused():

    r = make_client().post(
        "/login",
        data={
            "user_code": "F001",
            "password": "demo123"
        }
    )

    assert r.status_code == 400


def test_lockout_after_five_failures():

    client = make_client()

    with_csrf(client)

    for _ in range(5):
        post_login(client, "F001", "wrong")

    r = post_login(client, "F001", "demo123")

    assert b"Too many failed attempts" in r.data


def test_dev_login_is_off_when_dev_mode_is_false():

    old = Config.DEV_MODE

    Config.DEV_MODE = False

    try:
        assert make_client().get(
            "/dev/login/faculty"
        ).status_code == 404

    finally:
        Config.DEV_MODE = old

