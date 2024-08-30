from .members_utils import get_members_by_tree_id, format_members
from .users_utils import get_user_by_id, format_user


def format_tree(cur, tree):
    user = get_user_by_id(cur, tree[2])
    members = get_members_by_tree_id(cur, tree[0])
    return {
        "tree_id": tree[0],
        "tree_name": tree[1],
        "user": format_user(user),
        "members": format_members(members),
    }


def format_trees(cur, trees):
    return [format_tree(cur, tree) for tree in trees]
