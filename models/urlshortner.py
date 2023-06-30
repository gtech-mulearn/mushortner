class UrlShortner:
    def __init__(self, db_connection):
        self.db_connection = db_connection

    def get_users(self):
        query = "SELECT * FROM user;"
        return self.db_connection.execute_query(query)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM user WHERE id = :user_id;"
        params = {'user_id': user_id}
        return self.db_connection.fetch_one(query, params)

    def insert_profile_link(self, profile_pic, discord_id):
        query = "UPDATE user SET profile_pic = :profile_pic WHERE discord_id = :discord_id;"
        params = {'discord_id': str(discord_id)}

        self.db_connection.execute(query, params)
