from hamcrest import (
    all_of,
    assert_that,
    has_entries,
    has_entry,
    has_items,
    starts_with,
)


def test_get_v1_account(auth_account_helper):

    # Получаем информацию о пользователе
    response = auth_account_helper.get_current_user()

    # Проверяем поля тела ответа
    assert_that(
        response.json(),
        all_of(
            has_entry(
                "resource",
                has_entry(
                    "login",
                    starts_with("iponomarev"),
                ),
            ),
            has_entry(
                "resource",
                has_entry(
                    "settings",
                    has_entry("colorSchema", "Modern"),
                ),
            ),
            has_entry(
                "resource",
                has_entry(
                    "settings",
                    has_entry(
                        "paging",
                        has_entries(
                            {
                                "postsPerPage": 10,
                                "commentsPerPage": 10,
                                "topicsPerPage": 10,
                                "messagesPerPage": 10,
                                "entitiesPerPage": 10,
                            },
                        ),
                    ),
                ),
            ),
            has_entry(
                "resource",
                has_entry(
                    "roles",
                    has_items("Guest", "Player"),
                ),
            ),
            has_entry(
                "resource",
                has_entry(
                    "rating",
                    has_entries(
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
