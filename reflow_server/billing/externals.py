from reflow_server.core import externals


class VindiExternal(externals.External):
    host = 'https://sandbox-app.vindi.com.br/api/v1'
    secure = False
    basic_auth = ('knbtmIJp7smiSzQdThuAquX80aHCGDV9VO2L6_mYOuU', '')

