class User:
    def __init__(self, username, password, role, login_count):
        self.username = username
        self.password = password
        self.role = role
        self.login_count = login_count
    
    def matrix_shuffle(self):
        return ''.join(self.password[i] for i in [6, 1, 2, 7, 3, 5, 8, 4, 0])

    def matrix_deshuffle(self):
        return ''.join(self.password[i] for i in [8, 1, 2, 4, 7, 5, 0, 3, 6])