from core.brainly_api.legacy_api import LegacyApiResponse, LegacyApiUser


def test_legacy_api_response():
    html_response = {
        "impl": 27,
        "protocol": 27,
        "schema": "user/responses/user.me.res",
        "success": True,
        "validated": True,
        "data": {
            "user_category": 500
        }
    }

    response = LegacyApiResponse(html_response)

    assert response.protocol_version == html_response["protocol"]
    assert response.users_data == []
    assert response.data == html_response["data"]


def test_legacy_api_response_with_users_data():
    html_response = {
        "impl": 27,
        "protocol": 28,
        "schema": "moderation/responses/moderation.index.res",
        "success": True,
        "validated": False,
        "data": {
            "last_id": 5816710
        },
        "users_data": [{
            "id": 54605682,
            "nick": "AndrewssBot",
            "gender": 2,
            "is_deleted": False,
            "avatar": {
                "64": "https://us-static.z-dn.net/files/d8a/2628bcb420c32a9b049b2504f01884db.jpeg",
                "100": "https://us-static.z-dn.net/files/df7/5f3f932b5758e7af4b8f65ce1918aaa5.jpeg"
            },
            "ranks": {
                "color": "#6ed6a0",
                "names": ["Ambitious"],
                "count": 1
            },
            "ranks_ids": [3]
        }]
    }

    response = LegacyApiResponse(html_response)

    assert response.protocol_version == html_response["protocol"]
    assert response.data == html_response["data"]
    assert len(response.users_data) == len(html_response["users_data"])
    assert isinstance(response.users_data[0], LegacyApiUser)
