from unittest.mock import patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient


# *******************************
# ACCOUNT PROFILE / ME
# *******************************
@pytest.mark.asyncio
async def test_get_own_profile(client, test_account_authorized_headers):
    """Test get current account info"""
    response = client.get("/api/v1/accounts/me", headers=test_account_authorized_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "email" in data


# async def test_update_own_profile(client, test_account_authorized_headers):
#     """Test updating current account profile"""
#     response = client.put("/api/v1/accounts/me", json={"name": "New Name"}, headers=test_account_authorized_headers)
#     assert response.status_code == status.HTTP_200_OK


@patch("src.auth.api.v1.accounts.send_password_reset_email")
@pytest.mark.asyncio
async def test_password_reset_request(mock_send_email, client, test_account_db):
    """Test sending password reset email/token"""
    response = client.post("/api/v1/accounts/password-reset", json={"email": test_account_db.email})
    assert response.status_code == status.HTTP_201_CREATED
    mock_send_email.assert_awaited_once()


# @pytest.mark.asyncio
# async def test_password_reset_confirm(client):
#     """Test confirming new password using reset token"""
#     assert False
