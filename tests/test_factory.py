from percheck import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING':True}).testing

def test_dotenv(app):
    assert 'TESTING' in app.config
    print('\n Private Key : ' + str(app.config['PRIVATE_KEY']))
    assert 'PRIVATE_KEY' in app.config
    print('\n Github App ID: ' + str(app.config['GITHUB_APP_IDENTIFIER']))
    assert 'GITHUB_APP_IDENTIFIER' in app.config
    print('\n Webhook Secret: ' + str(app.config['GITHUB_WEBHOOK_SECRET']))
    assert 'GITHUB_WEBHOOK_SECRET' in app.config
