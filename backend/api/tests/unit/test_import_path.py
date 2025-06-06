from resources import get_table


def test_import_path():
    assert callable(get_table)
