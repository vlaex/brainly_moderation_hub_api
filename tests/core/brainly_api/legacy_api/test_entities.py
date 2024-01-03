from faker import Faker
from core.brainly_api.legacy_api import LegacyApiUser


def generate_user_data(faker: Faker) -> dict:
    return {
        "id": faker.random_int(min=1),
        "nick": faker.user_name(),
        "gender": faker.random_element(elements=(None, 1, 2)),
        "is_deleted": faker.pybool(),
        "avatar": {
            "64": faker.image_url(),
            "100": faker.image_url()
        }
    }


def test_legacy_api_user_from_dict(faker):
    user_data = generate_user_data(faker)
    user_instance = LegacyApiUser.from_dict(user_data)

    assert user_instance.id == user_data["id"]
    assert user_instance.nick == user_data["nick"]
    assert user_instance.gender == user_data.get("gender")
    assert user_instance.is_deleted == user_data.get("is_deleted")
    assert user_instance.avatar == user_data["avatar"]["64"]


def test_legacy_api_user_with_no_avatar(faker):
    user_data = generate_user_data(faker)
    user_data["avatar"] = None

    user_instance = LegacyApiUser.from_dict(user_data)

    assert user_instance.id == user_data["id"]
    assert user_instance.nick == user_data["nick"]
    assert user_instance.gender == user_data.get("gender")
    assert user_instance.is_deleted == user_data.get("is_deleted")
    assert user_instance.avatar is None
