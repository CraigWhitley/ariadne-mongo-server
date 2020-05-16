from app import index


def test_index_route():
    """Tests the index route returns expected result"""
    assert index() == '<h1> Hello, World </h1>'
