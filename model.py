from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict.get('id')
        self.email = user_dict.get('email')
        self.name = user_dict.get('name')
        self.role = user_dict.get('role')
        self.password = user_dict.get('password')
        avatar = user_dict.get('avatar')
        if isinstance(avatar, dict):
            self.avatar = avatar.get('data')
        else:
            self.avatar = avatar

    def get_id(self):
        return self.id
