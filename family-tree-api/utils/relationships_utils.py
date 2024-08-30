from .members_utils import get_member_by_id, format_member


def format_relationship(cur, relationship):
    child = get_member_by_id(cur, relationship[1])
    mother = get_member_by_id(cur, relationship[2])
    father = get_member_by_id(cur, relationship[3])
    return {
        "relationship_id": relationship[0],
        "child": format_member(child),
        "mother": format_member(mother),
        "father": format_member(father),
    }


def format_relationship_for_calc(relationship):
    return {
        "relationship_id": relationship[0],
        "child_id": relationship[1],
        "mother_id": relationship[2],
        "father_id": relationship[3],
    }


def format_relationships(cur, relationships):
    return [format_relationship(cur, relationship) for relationship in relationships]


def get_relationship_by_member_id(cur, member_id):
    cur.execute("SELECT relationship_id, child_id, mother_id, father_id "
                "FROM family_relationship "
                "WHERE child_id = %s",
                [member_id])
    relationship = cur.fetchone()
    return relationship
