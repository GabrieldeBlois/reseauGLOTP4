# the client class in server

class ServerClient:
    def __init__(self, sock):
        self.state = 0
        self.sock = sock
        self.username = ""
        self.pwd = ""
        self.userPath = ""