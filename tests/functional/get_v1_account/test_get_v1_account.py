from hamcrest import (
    all_of,
    assert_that,
    has_items,
    starts_with,
    has_property,
    has_properties,
)


def test_get_v1_account(auth_account_helper):

    # Получаем информацию о пользователе
    response = auth_account_helper.get_current_user()

    # Проверяем поля тела ответа
    assert_that(
        response,
        all_of(
            has_property(
                "resource",
                has_property(
                    "login",
                    starts_with("iponomarev"),
                ),
            ),
            has_property(
                "resource",
                has_property(
                    "settings",
                    has_property("color_schema", "Modern"),
                ),
            ),
            has_property(
                "resource",
                has_property(
                    "settings",
                    has_property(
                        "paging",
                        has_properties(
                            {
                                "posts_per_page": 10,
                                "comments_per_page": 10,
                                "topics_per_page": 10,
                                "messages_per_page": 10,
                                "entities_per_page": 10,
                            },
                        ),
                    ),
                ),
            ),
            has_property(
                "resource",
                has_property(
                    "roles",
                    has_items("Guest", "Player"),
                ),
            ),
            has_property(
                "resource",
                has_property(
                    "rating",
                    has_properties(
                        {
                            "enabled": True,
                            "quality": 0,
                            "quantity": 0,
                        },
                    ),
                ),
            ),
        ),
    )
