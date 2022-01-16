from reflow_server.core.externals import External

class GoogleSheetsExternal(External):
    def all_sheets(self, access_token):
        return self.get(f"https://www.googleapis.com/drive/v3/files?q=mimeType='application/vnd.google-apps.spreadsheet'", headers={
            'Authorization': f'Bearer {access_token}'
        })