from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from config import Config
from utils.members_utils import get_member_by_id, format_member, get_members_by_tree_id, format_members
from utils.users_utils import get_user_by_id, format_user, format_users
from utils.relationships_utils import format_relationship, format_relationships, get_relationship_by_member_id, format_relationship_for_calc
from utils.trees_utils import format_tree, format_trees


app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)


# users

@app.route('/users', methods=['POST'])
def create_user():
    if request.method == "POST":
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) "
                    "VALUES (%s, %s, %s)",
                    [username, email, password])
        user_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        return jsonify(user_id=user_id), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, username, email "
                    "FROM users "
                    "WHERE user_id = %s",
                    [user_id])
        user = cur.fetchone()
        if user is None:
            return jsonify({"error": "User not found"}), 404
        response = {
            "user_id": user[0],
            "username": user[1],
            "email": user[2]
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/users', methods=['GET'])
def get_users():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT user_id, username, email "
                    "FROM users ")
        users = cur.fetchall()
        if users is None:
            return jsonify({"error": "Users not found"}), 404
        response = {"users": format_users(users)}
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if request.method == "PUT":
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users "
                    "SET username=%s, email=%s, password=%s "
                    "WHERE user_id=%s",
                    [username, email, password, user_id])
        cur.execute("SELECT user_id, username, email "
                    "FROM users "
                    "WHERE user_id = %s",
                    [user_id])
        user = cur.fetchone()
        response = {
            "message": "User updated successfully",
            "data": {
                "user_id": user[0],
                "username": user[1],
                "email": user[2]}
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if request.method == "DELETE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM users WHERE user_id=%s", [user_id])
        response = {
            "message": "User deleted successfully"
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


# family_members

@app.route('/members', methods=['POST'])
def create_member():
    if request.method == "POST":
        data = request.json
        user_id = data.get("user_id")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        tree_id = data.get("tree_id")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO family_members (user_id, first_name, last_name, tree_id) "
                    "VALUES (%s, %s, %s, %s)",
                    [user_id, first_name, last_name, tree_id])
        member_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        return jsonify(member_id=member_id), 200


@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        member = get_member_by_id(cur, member_id)
        if member is None:
            return jsonify({"error": "Member not found"}), 404
        response = format_member(member)
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/members', methods=['GET'])
def get_members():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT member_id, user_id, first_name, last_name, tree_id "
                    "FROM family_members ")
        members = cur.fetchall()
        if members is None:
            return jsonify({"error": "Members not found"}), 404
        response = {"members": format_members(members)}
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    if request.method == "PUT":
        data = request.json
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        tree_id = data.get("tree_id")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE family_members "
                    "SET first_name=%s, last_name=%s, tree_id=%s "
                    "WHERE member_id=%s",
                    [first_name, last_name, tree_id, member_id])
        cur.execute("SELECT user_id, first_name, last_name, tree_id "
                    "FROM family_members "
                    "WHERE member_id = %s",
                    [member_id])
        member = cur.fetchone()
        response = {
            "message": "Member updated successfully",
            "data": {
                "user_id": member[0],
                "first_name": member[1],
                "last_name": member[2],
                "tree_id": member[3]
            }
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    if request.method == "DELETE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM family_members WHERE member_id=%s", [member_id])
        response = {
            "message": "Member deleted successfully"
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


# family-relationship

@app.route('/relationships', methods=['POST'])
def create_relationship():
    if request.method == "POST":
        data = request.json
        child_id = data.get("child_id")
        mother_id = data.get("mother_id")
        father_id = data.get("father_id")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO family_relationship (child_id, mother_id, father_id) "
                    "VALUES (%s, %s, %s)",
                    [child_id, mother_id, father_id])
        relationship_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        return jsonify(relationship_id=relationship_id), 200


@app.route('/relationships/<int:relationship_id>', methods=['GET'])
def get_relationship(relationship_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT relationship_id, child_id, mother_id, father_id "
                    "FROM family_relationship "
                    "WHERE relationship_id = %s",
                    [relationship_id])
        relationship = cur.fetchone()
        if relationship is None:
            return jsonify({"error": "Relationship not found"}), 404
        response = format_relationship(cur, relationship)
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/relationships', methods=['GET'])
def get_relationships():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT relationship_id, child_id, mother_id, father_id "
                    "FROM family_relationship ")
        relationships = cur.fetchall()
        if relationships is None:
            return jsonify({"error": "Relationships not found"}), 404
        response = {"relationships": format_relationships(cur, relationships)}
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/relationships/<int:relationship_id>', methods=['PUT'])
def update_relationship(relationship_id):
    if request.method == "PUT":
        data = request.json
        child_id = data.get("child_id")
        mother_id = data.get("mother_id")
        father_id = data.get("father_id")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE family_relationship "
                    "SET child_id=%s, mother_id=%s, father_id=%s "
                    "WHERE relationship_id=%s",
                    [child_id, mother_id, father_id, relationship_id])
        cur.execute("SELECT relationship_id, child_id, mother_id, father_id "
                    "FROM family_relationship "
                    "WHERE relationship_id = %s",
                    [relationship_id])
        relationship = cur.fetchone()
        if relationship is None:
            return jsonify({"error": "Relationship not found"}), 404
        child = get_member_by_id(cur, relationship[1])
        mother = get_member_by_id(cur, relationship[2])
        father = get_member_by_id(cur, relationship[3])
        response = {
            "message": "Relationship updated successfully",
            "data": {
                "relationship_id": relationship[0],
                "child": format_member(child),
                "mother": format_member(mother),
                "father": format_member(father)
            }
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/relationships/<int:relationship_id>', methods=['DELETE'])
def delete_relationship(relationship_id):
    if request.method == "DELETE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM family_relationship "
                    "WHERE relationship_id=%s",
                    [relationship_id])
        response = {
            "message": "Relationship deleted successfully"
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


# family_trees

@app.route('/trees', methods=['POST'])
def create_tree():
    if request.method == "POST":
        data = request.json
        tree_name = data.get("tree_name")
        user_id = data.get("user_id")
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO family_trees (tree_name, user_id) "
                    "VALUES (%s, %s)",
                    [tree_name, user_id])
        tree_id = cur.lastrowid
        mysql.connection.commit()
        cur.close()
        return jsonify(tree_id=tree_id), 200


@app.route('/trees/<int:tree_id>', methods=['GET'])
def get_tree(tree_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT tree_id, tree_name, user_id "
                    "FROM family_trees "
                    "WHERE tree_id = %s",
                    [tree_id])
        tree = cur.fetchone()
        if tree is None:
            return jsonify({"error": "Tree not found"}), 404
        response = format_tree(cur, tree)
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/trees', methods=['GET'])
def get_trees():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        cur.execute("SELECT tree_id, tree_name, user_id "
                    "FROM family_trees ")
        trees = cur.fetchall()
        if trees is None:
            return jsonify({"error": "Trees not found"}), 404
        response = {"trees": format_trees(cur, trees)}
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/trees/<int:tree_id>', methods=['PUT'])
def update_tree(tree_id):
    if request.method == "PUT":
        data = request.json
        tree_name = data.get("tree_name")
        user_id = data.get("user_id")
        cur = mysql.connection.cursor()
        cur.execute("UPDATE family_trees "
                    "SET tree_name=%s, user_id=%s "
                    "WHERE tree_id=%s",
                    [tree_name, user_id, tree_id])
        cur.execute("SELECT tree_id, tree_name, user_id "
                    "FROM family_trees "
                    "WHERE tree_id = %s",
                    [tree_id])
        tree = cur.fetchone()
        if tree is None:
            return jsonify({"error": "Tree not found"}), 404
        user = get_user_by_id(cur, tree[2])
        members = get_members_by_tree_id(cur, tree[0])
        response = {
            "message": "Tree updated successfully",
            "data": {
                "tree_id": tree[0],
                "tree_name": tree[1],
                "user": format_user(user),
                "members": format_members(members)
            }
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


@app.route('/trees/<int:tree_id>', methods=['DELETE'])
def delete_tree(tree_id):
    if request.method == "DELETE":
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM family_trees "
                    "WHERE tree_id=%s",
                    [tree_id])
        response = {
            "message": "Tree deleted successfully"
        }
        mysql.connection.commit()
        cur.close()
        return jsonify(response), 200


def calculate_tree_height(member_id, height=0):
    cur = mysql.connection.cursor()
    relationship = get_relationship_by_member_id(cur, member_id)
    if not relationship:
        return height
    f_relationship = format_relationship_for_calc(relationship)
    heights = []
    if f_relationship["father_id"]:
        heights.append(calculate_tree_height(f_relationship["father_id"], height + 1))
    if f_relationship["mother_id"]:
        heights.append(calculate_tree_height(f_relationship["mother_id"], height + 1))
    return max(heights) if heights else height


@app.route('/trees/<int:tree_id>/height', methods=['GET'])
def get_tree_height(tree_id):
    if request.method == "GET":
        cur = mysql.connection.cursor()
        members = format_members(get_members_by_tree_id(cur, tree_id))
        if not members:
            return jsonify(height=0)
        heights = []
        for member in members:
            heights.append(calculate_tree_height(member["member_id"]))
        cur.close()
        return jsonify(height=max(heights)), 200


if __name__ == '__main__':
    app.run(debug=True)
