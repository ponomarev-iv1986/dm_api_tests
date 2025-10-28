class Configuration:
    def __init__(self, host, headers=None, disable_log=False):
        self.host = host
        self.headers = headers
        self.disable_log = disable_log
