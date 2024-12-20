class HashMap:
    def __init__(self):
        self.users_byId={}
        self.users_byEmail={}
    def add_user(self, user):
        self.users_byId[user.id] = user
        self.users_byEmail[user.email] = user
    def get_user_by_id(self, user_id):
        return self.users_byId.get(user_id)

    def get_user_by_email(self, email):
        return self.users_byEmail.get(email)