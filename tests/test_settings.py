"""test functions in helpers.settings"""

import helpers.settings as settings


def test_suggests_secret():
    assert not settings._suggests_secret('foo')
    assert not settings._suggests_secret('foo_bar')
    assert not settings._suggests_secret('foo_secret')
    assert not settings._suggests_secret('foo_password')
    assert not settings._suggests_secret('FOO_PASSWORD')


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
