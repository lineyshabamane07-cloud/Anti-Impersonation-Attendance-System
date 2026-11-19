from config import Config
from services import qr_service, verify_service, report_service
from services.geo_service import haversine_m


def test_mock_contract_shapes():
    assert Config.USE_MOCK
    assert isinstance(qr_service.create_session(1, 18.5, 73.8), int)
    t = qr_service.get_current_token(1)
    assert set(t) == {"token", "expires_in"}
    for suffix, status in [("", "present"), ("-expired", "rejected"), ("-far", "rejected"),
                           ("-dup", "rejected"), ("-device", "rejected"), ("-flag", "flagged")]:
        r = verify_service.mark_attendance("x" + suffix, 101, 18.5, 73.8, "dev")
        assert r["status"] == status and set(r) == {"status", "reason", "distance_m"}
    assert isinstance(report_service.list_marked(1), list)
    assert "present" in report_service.session_summary(1)


def test_haversine():
    assert haversine_m(18.5, 73.8, 18.5, 73.8) == 0
    assert 110000 < haversine_m(18.0, 73.0, 19.0, 73.0) < 112000  # ~111 km per degree
