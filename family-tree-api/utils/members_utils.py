def get_member_by_id(cur, member_id):
    cur.execute("SELECT member_id, user_id, first_name, last_name, tree_id "
                "FROM family_members "
                "WHERE member_id = %s",
                [member_id])
    member = cur.fetchone()
    return member


def format_member(member):
    if member is None:
        return None
    return {
        "member_id": member[0],
        "user_id": member[1],
        "first_name": member[2],
        "last_name": member[3],
        "tree_id": member[4]
    }


def get_members_by_tree_id(cur, tree_id):
    cur.execute("SELECT member_id, user_id, first_name, last_name, tree_id "
                "FROM family_members "
                "WHERE tree_id = %s",
                [tree_id])
    member = cur.fetchall()
    return member


def format_members(members):
    return [format_member(member) for member in members]
