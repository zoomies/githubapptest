
def test_install(client):
    response=client.get('install')
    assert response.data == b'Thank you for installing P2 DF Test'
