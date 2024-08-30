def get_user_by_id(cur, user_id):
    cur.execute("SELECT user_id, username, email "
                "FROM users "
                "WHERE user_id = %s",
                [user_id])
    user = cur.fetchone()
    return user


def format_user(user):
    if user is None:
        return None
    return {
        "user_id": user[0],
        "username": user[1],
        "email": user[2]
    }


def format_users(users):
    return [format_user(user) for user in users]
