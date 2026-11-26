from app.domain.services.auth_service import AuthService, verify_password


def test_e2e_scenario_1_complete_password_recovery_flow(client, db_session, sample_user):
    # 1. Usuario solicita recuperación desde el servicio/endpoint
    service = AuthService(db=db_session)
    delivery = service.request_password_reset(sample_user.email)
    assert delivery["reset_token"] is not None

    api_req = client.post(
        "/api/v1/auth/forgot-password",
        json={"email": sample_user.email},
    )
    assert api_req.status_code == 200

    # 2. Usuario usa el token recibido para establecer nueva contraseña
    reset_res = client.post(
        "/api/v1/auth/reset-password",
        json={"token": delivery["reset_token"], "new_password": "E2eRecoveredPass1"},
    )
    assert reset_res.status_code == 200

    # 3. Se verifica persistencia en BD e invalidación de credenciales anteriores
    db_session.refresh(sample_user)
    assert verify_password("E2eRecoveredPass1", sample_user.password_hash) is True
    assert verify_password("OldPass123", sample_user.password_hash) is False
    assert sample_user.token_version == 2


def test_e2e_scenario_2_replay_and_invalid_payload_rejection(client, db_session, sample_user):
    service = AuthService(db=db_session)
    token = service.request_password_reset(sample_user.email)["reset_token"]

    # Primer uso válido
    ok = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "ValidFirstPass1"},
    )
    assert ok.status_code == 200

    # Reintento con el mismo token (replay) debe fallar
    replay = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token, "new_password": "ValidSecondPass2"},
    )
    assert replay.status_code == 400
    assert replay.json()["error"]["code"] == "BUSINESS_RULE_VIOLATION"
    assert "utilizado" in replay.json()["error"]["message"].lower()


def test_e2e_scenario_3_anti_enumeration_and_isolation_between_accounts(
    client, db_session, sample_user, second_user
):
    # Solicitudes para correo existente vs inexistente responden igual
    r1 = client.post("/api/v1/auth/forgot-password", json={"email": sample_user.email})
    r2 = client.post("/api/v1/auth/forgot-password", json={"email": "noexiste@tcg.cl"})
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["message"] == r2.json()["message"]

    # El restablecimiento de sample_user no altera a second_user
    service = AuthService(db=db_session)
    token_sample = service.request_password_reset(sample_user.email)["reset_token"]
    res = client.post(
        "/api/v1/auth/reset-password",
        json={"token": token_sample, "new_password": "IsolatedPass123"},
    )
    assert res.status_code == 200

    db_session.refresh(second_user)
    assert verify_password("RivalPass123", second_user.password_hash) is True