import json
from percheck import create_app

mimetype = 'application/json'
headers = { 'Content-Type': mimetype, 'Accept': mimetype,
            'HTTP_X_HUB_SIGNATURE':'sha1=50536c72626b413164726935335543457063687a33744d504179673d'}
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

def test_webhook_post(client):

    json_data = json.loads(json_string)

    response = client.post('/webhook', json=json.dumps(json_data), headers=headers)
    
    assert response.status == '401 UNAUTHORIZED'

def test_app_auth_sig_noheader(client):
    json_data = json.loads(json_string)

    response = client.post('/webhook', json=json.dumps(json_data))
    
    assert response.status == '401 UNAUTHORIZED'
    
    
def test_app_auth_sig_badsig(client):
    json_data = json.loads(json_string)

    bad_headers =  { 'Content-Type': mimetype, 'Accept': mimetype,
            'HTTP_X_HUB_SIGNATURE':'sha1=50536c72626b413164726935335543457063687a33744d50417967'} 

    response = client.post('/webhook', json=json.dumps(json_data), headers=bad_headers)
    
    assert response.status == '401 UNAUTHORIZED'


def test_app_auth_sig_wrongdigest(client):
    json_data = json.loads(json_string)

    bad_headers =  { 'Content-Type': mimetype, 'Accept': mimetype,
            'HTTP_X_HUB_SIGNATURE':'sha256=50536c72626b413164726935335543457063687a33744d504179673d'} 

    response = client.post('/webhook', json=json.dumps(json_data), headers=bad_headers)

    assert response.status == '401 UNAUTHORIZED'


def test_webhook_get(client):

    response = client.get('/webhook',json='')
    print(response.status_code)
    assert response.status_code == 405


