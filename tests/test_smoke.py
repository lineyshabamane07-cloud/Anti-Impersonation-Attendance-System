from app import create_app


def test_health_and_pages():
    client = create_app().test_client()
    assert client.get("/health").get_json()["status"] == "ok"
    for url in ["/", "/login"]:
        assert client.get(url).status_code == 200, url
    for url in ["/faculty/dashboard", "/student/dashboard", "/admin/dashboard"]:
        # 200 = open page, 302 = sent to the login page (once routes are protected)
        assert client.get(url).status_code in (200, 302), url
