import random
import string
import pytest
from app import app
from test_config import TestConfig

app.config.from_object(TestConfig)


@pytest.fixture
def client():
    app.config.from_object(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            yield client


def insert_user(client, json):
    return client.post('/users', json=json)


def insert_member(client, json):
    return client.post('/members', json=json)


def insert_tree(client, json):
    return client.post('/trees', json=json)


def insert_relationship(client, json):
    return client.post('/relationships', json=json)


def generate_random_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(5))


def get_user_id(client):
    response = client.get('/users')
    user_id = response.get_json()["users"][0]["user_id"]
    return user_id


# users

def test_create_user(client):
    username = generate_random_string()
    response = insert_user(client, {
        "username": username,
        "email": username + "@test.com",
        "password": "password"
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "user_id" in json_data


def test_get_user(client):
    username = generate_random_string()
    response = insert_user(client, {
        "username": username,
        "email": username + "@test.com",
        "password": "password"
    })
    user_id = response.get_json()["user_id"]

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["username"] == username


def test_update_user(client):
    username = generate_random_string()
    response = insert_user(client, {
        "username": username,
        "email": username + "@test.com",
        "password": "password"
    })
    user_id = response.get_json()["user_id"]

    response = client.put(f'/users/{user_id}', json={
        "username": "updated" + username,
        "email": "updated" + username + "@test.com",
        "password": "newpassword"
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["username"] == "updated" + username
    assert json_data["data"]["email"] == "updated" + username + "@test.com"


def test_delete_user(client):
    username = generate_random_string()
    response = insert_user(client, {
        "username": username,
        "email": username + "@test.com",
        "password": "password"
    })
    user_id = response.get_json()["user_id"]

    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "User deleted successfully"

    response = client.get(f'/users/{user_id}')
    assert response.status_code == 404


# family_members

def test_create_member(client):
    user_id = get_user_id(client)

    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]

    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "member_id" in json_data


def test_get_member(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    member_id = response.get_json()["member_id"]

    response = client.get(f'/members/{member_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["first_name"] == "John"


def test_update_member(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    member_id = response.get_json()["member_id"]

    response = client.put(f'/members/{member_id}', json={
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["first_name"] == "Jane"


def test_delete_member(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    member_id = response.get_json()["member_id"]

    response = client.delete(f'/members/{member_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Member deleted successfully"

    response = client.get(f'/members/{member_id}')
    assert response.status_code == 404


# family_relationship

def test_create_relationship(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    child_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    mother_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "James",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    father_id = response.get_json()["member_id"]

    response = insert_relationship(client, {
        "child_id": child_id,
        "mother_id": mother_id,
        "father_id": father_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert "relationship_id" in json_data


def test_get_relationship(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    child_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    mother_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "James",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    father_id = response.get_json()["member_id"]
    response = insert_relationship(client, {
        "child_id": child_id,
        "mother_id": mother_id,
        "father_id": father_id
    })
    relationship_id = response.get_json()["relationship_id"]

    response = client.get(f'/relationships/{relationship_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["child"]["first_name"] == "John"


def test_update_relationship(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    child_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    mother_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "James",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    father_id = response.get_json()["member_id"]
    response = insert_relationship(client, {
        "child_id": child_id,
        "mother_id": mother_id,
        "father_id": father_id
    })
    relationship_id = response.get_json()["relationship_id"]

    response = client.put(f'/relationships/{relationship_id}', json={
        "child_id": child_id,
        "mother_id": father_id,
        "father_id": mother_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["data"]["mother"]["member_id"] == father_id


def test_delete_relationship(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]
    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    child_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    mother_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "James",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    father_id = response.get_json()["member_id"]
    response = insert_relationship(client, {
        "child_id": child_id,
        "mother_id": mother_id,
        "father_id": father_id
    })
    relationship_id = response.get_json()["relationship_id"]

    response = client.delete(f'/relationships/{relationship_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == "Relationship deleted successfully"

    response = client.get(f'/relationships/{relationship_id}')
    assert response.status_code == 404


# family_trees

def test_create_tree(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'tree_id' in json_data
    assert isinstance(json_data['tree_id'], int)


def test_get_tree(client):
    user_id = get_user_id(client)
    post_response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = post_response.get_json()['tree_id']

    response = client.get(f'/trees/{tree_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['tree_id'] == tree_id
    assert json_data['tree_name'] == 'Test Family'
    assert "user" in json_data
    assert "members" in json_data


def test_get_trees(client):
    user_id = get_user_id(client)
    insert_tree(client, {
        "tree_name": "Test Family 1",
        "user_id": user_id
    })
    insert_tree(client, {
        "tree_name": "Test Family 2",
        "user_id": user_id
    })

    response = client.get('/trees')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'trees' in json_data
    assert isinstance(json_data['trees'], list)
    assert len(json_data['trees']) >= 2


def test_update_tree(client):
    user_id = get_user_id(client)
    post_response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = post_response.get_json()['tree_id']

    response = client.put(f'/trees/{tree_id}', json={
        "tree_name": "Updated Test Family",
        "user_id": user_id
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Tree updated successfully'
    assert json_data['data']['tree_name'] == "Updated Test Family"


def test_delete_tree(client):
    user_id = get_user_id(client)
    post_response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = post_response.get_json()['tree_id']

    response = client.delete(f'/trees/{tree_id}')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == 'Tree deleted successfully'

    get_response = client.get(f'/trees/{tree_id}')
    assert get_response.status_code == 404


# calculate_tree_height

def test_calculate_tree_height(client):
    user_id = get_user_id(client)
    response = insert_tree(client, {
        "tree_name": "Test Family",
        "user_id": user_id
    })
    tree_id = response.get_json()["tree_id"]

    response = insert_member(client, {
        "first_name": "John",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    child_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "Jane",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    mother_id = response.get_json()["member_id"]
    response = insert_member(client, {
        "first_name": "James",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    father_id = response.get_json()["member_id"]

    insert_relationship(client, {
        "child_id": child_id,
        "mother_id": mother_id,
        "father_id": father_id
    })

    response = client.get(f'/trees/{tree_id}/height')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["height"] == 1

    response = insert_member(client, {
        "first_name": "Jeff",
        "last_name": "Doe",
        "tree_id": tree_id
    })
    grandfather_id = response.get_json()["member_id"]

    insert_relationship(client, {
        "child_id": father_id,
        "father_id": grandfather_id
    })

    response = client.get(f'/trees/{tree_id}/height')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["height"] == 2
