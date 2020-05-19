from settings.app import AppSettings


def test_can_change_settings():
    """Tests we can change site settings"""
    AppSettings.JWT_EXPIRY = 24

    assert AppSettings.JWT_EXPIRY == 24

    AppSettings.JWT_EXPIRY = 78
