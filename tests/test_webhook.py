import json
from percheck import create_app

def test_webhook_post(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype, 
        'Accept': mimetype
    }
    json_string = r'''{
        "action": "revoked",
        "sender": {
            "login": "octocat",
            "id": 1,
            "node_id": "MDQ6VXNlcjIxMDMxMDY3",
            "avatar_url": "https://github.com/images/error/octocat_happy.gif",
            "gravatar_id": "",
            "url": "https://api.github.com/users/octocat",
            "html_url": "https://github.com/octocat",
            "followers_url": "https://api.github.com/users/octocat/followers",
            "following_url": "https://api.github.com/users/octocat/following{/other_user}",
            "gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
            "organizations_url": "https://api.github.com/users/octocat/orgs",
            "repos_url": "https://api.github.com/users/octocat/repos",
            "events_url": "https://api.github.com/users/octocat/events{/privacy}",
            "received_events_url": "https://api.github.com/users/octocat/received_events",
            "type": "User",
            "site_admin": false
        }
    }'''

    json_data = json.loads(json_string)

    response = client.post('/webhook', json=json.dumps(json_data), headers=headers)
    
    assert response.content_type == 'text/html; charset=utf-8'
    assert response.content_length == 0


def test_webhook_get(client):

    response = client.get('/webhook',json='')
    print(response.status_code)
    assert response.status_code == 405


