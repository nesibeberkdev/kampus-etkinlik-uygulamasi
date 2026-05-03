from src.modules.user import User
class Admin(User):
    """
    Yönetici kullanıcısını temsil eder.
    User sınıfından kalıtım alır.
    """
    def __init__(self, id, username, email, password_hash):
        super().__init__(id, username, email, password_hash, role="admin")
    def create_event(self):
        return "Etkinlik oluşturma yetkisi mevcut."