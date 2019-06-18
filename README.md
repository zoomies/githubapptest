# Github App Test

This is a skeleton GitHub  app written on Flask in Python to allow testing the permissions on repos as seens from a GitHub App.

Although there is a pytest structure set up - the tests are 'stale' once the app evolved to authenticating back to GitHub - as testing at that point would require extensive mocking and fixtures - and this is not a production app.

The heavy lifting of the authentication is in app_auth.py and the route /webhook is used as the callback from GitHub