"""test functions in helpers.settings"""

import helpers.settings as settings


def test_suggests_secret():
    assert settings._suggests_secret('foo') == False
    assert settings._suggests_secret('foo_bar') == False
    assert settings._suggests_secret('foo_secret') == True
    assert settings._suggests_secret('foo_password') == True
    assert settings._suggests_secret('FOO_PASSWORD') == True


def test_get_redacted_data():

    # top level secrets
    assert settings._get_redacted_data(
        {'hello': 1, 'world': 2}) == \
        {'hello': 1, 'world': 2}
    assert settings._get_redacted_data(
        {'hello': 1, 'world_secret': 2}) == \
        {'hello': 1, 'world_secret': 'REDACTED'}

    # nested secrets
    assert settings._get_redacted_data(
        {'hello': 1, 'world': {'foo': 3, 'bar': 4}}) == \
        {'hello': 1, 'world': {'foo': 3, 'bar': 4}}
    assert settings._get_redacted_data(
        {'hello': 1, 'world': {'foo_secret': 3, 'bar': 4}}) == \
        {'hello': 1, 'world': {'foo_secret': 'REDACTED', 'bar': 4}}
