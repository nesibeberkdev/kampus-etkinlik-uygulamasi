class User:
    """
    Sistemdeki normal kullanıcıyı temsil eder.
    """

    def __init__(self, id, username, email, password_hash, role="user"):
        self.id = id
        self.username = username
        self.email = email
        self._password_hash = password_hash
        self.role = role

    def get_email(self):
        return self.email

    def check_password(self, password_hash):
        return self._password_hash == password_hash