# Simple OAuth refresh token retreiver for Twitch API

from http.server import HTTPServer, BaseHTTPRequestHandler
from time import sleep
from urllib import request, parse
import webbrowser
import threading
import json


client_id = ""                # your App client ID
client_secret = ""            # your app Secret
port = 8000                   # port for this web server
scope_list = ['bits:read', 'chat:read', 'channel:read:subscriptions', 'whispers:read',
              'moderation:read', 'channel:read:redemptions', 'channel:read:hype_train',
              'channel:manage:broadcast', 'channel:read:editors', 'user:read:blocked_users',
              'user:read:subscriptions', 'user:read:follows', 'channel:read:polls', 'channel:read:predictions',
              'channel:read:goals', 'moderator:read:automod_settings', 'moderator:read:blocked_terms',
              'moderator:read:chat_settings', 'channel:read:vips']    # scopes of Twitch API.

# list of all scopes available at https://dev.twitch.tv/docs/authentication/scopes
""" all_scopes = ["analytics:read:extensions", "analytics:read:games", "bits:read",
              "channel:edit:commercial", "channel:manage:broadcast", "channel:manage:extensions",
              "channel:manage:moderators", "channel:manage:polls", "channel:manage:predictions",
              "channel:manage:raids", "channel:manage:redemptions", "channel:manage:schedule",
              "channel:manage:videos", "channel:read:editors", "channel:read:goals",
              "channel:read:hype_train", "channel:read:polls", "channel:read:predictions",
              "channel:read:redemptions", "channel:read:stream_key", "channel:read:subscriptions",
              "channel:read:vips", "channel:manage:vips", "clips:edit", "moderation:read",
              "moderator:manage:announcements", "moderator:manage:automod",
              "moderator:read:automod_settings", "moderator:manage:automod_settings",
              "moderator:manage:banned_users", "moderator:read:blocked_terms",
              "moderator:manage:blocked_terms", "moderator:manage:chat_messages",
              "moderator:read:chat_settings", "moderator:manage:chat_settings",
              "user:edit", "user:edit:follows", "user:manage:blocked_users",
              "user:read:blocked_users", "user:read:broadcast", "user:manage:chat_color",
              "user:read:email", "user:read:follows", "user:read:subscriptions",
              "user:manage:whispers", "channel:moderate", "chat:edit", "chat:read",
              "whispers:read", "whispers:edit"]
 """

redirect_uri = "http://localhost:" + str(port)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    # disable verbose log of request
    def log_message(self, format, *args):
        return

    def do_GET(self):
        lines = self.path
        code = lines.split("/?code=")[1].split("&scope")[0]
        self.wfile.write(
            b"successful Twitch API auth request, go back to the python script\n")
        self.send_response(200)
        self.end_headers()

        url_post_refresh_token = "https://id.twitch.tv/oauth2/token"
        args = {"client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": redirect_uri
                }
        data = parse.urlencode(args).encode()
        req = request.Request(url_post_refresh_token, data=data)
        with request.urlopen(req) as resp:
            j = json.loads(resp.read())
            print()
            print("--- Your REFRESH TOKEN to use with the Twitch API: ---")
            print()
            print(j["refresh_token"])
            print()


def startBrowserAuthWithDelay():
    sleep(2)
    base_url_authorize = "https://id.twitch.tv/oauth2/authorize"
    scope = "+".join(scope_list)
    args = f"?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&force_verify=false"
    url = base_url_authorize + args
    webbrowser.open(url)


def start_server_and_auth_request():
    # send request AFTER the localhost server launched
    th = threading.Thread(target=startBrowserAuthWithDelay)
    th.start()

    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()


if not client_id:
    client_id = input("input Twitch App client id: ")
if not client_secret:
    client_secret = input("input Twitch App client secret: ")
print("redirect uri is : " + redirect_uri)
start_server_and_auth_request()
