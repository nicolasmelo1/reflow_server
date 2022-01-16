from reflow_server.core.externals import External

class GoogleExternal(External):
    def refresh_google_token(self, client_id, client_secret, refresh_token):
        return self.post('https://oauth2.googleapis.com/token', data={
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        })