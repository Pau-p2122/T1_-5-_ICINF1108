from app.domain.services.auth_service import AuthService


def test_regression_no_duplicate_auth_prefix_route(client):
    duplicated = client.post(
        "/api/v1/auth/auth/forgot-password",
        json={"email": "trainer@tcg.cl"},
    )
    assert duplicated.status_code == 404


def test_regression_email_case_and_whitespace_normalization(db_session, sample_user):
    service = AuthService(db=db_session)
    result = service.request_password_reset("  TRAINER@TCG.CL  ")
    assert result["reset_token"] is not None


def test_regression_validation_error_format_on_weak_password(client):
    res = client.post(
        "/api/v1/auth/reset-password",
        json={"token": "1234567890", "new_password": "123"},
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"