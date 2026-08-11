#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis.exceptions import ConnectionError

from Tourney.cache import clear_all_user_sessions, clear_user_session
from Tourney.config import TestingConfig
from Tourney.models import Users
from Tourney.utils.security.auth import login_user
from Tourney.utils.user import get_current_user, is_admin
from tests.helpers import create_tourney, destroy_tourney, register_user


def test_clear_user_session():
    app = create_tourney()
    with app.app_context():
        register_user(app)

        # Users by default should have a non-admin type
        user = Users.query.filter_by(id=2).first()
        with app.test_request_context("/"):
            login_user(user)
            user = get_current_user()
            assert user.id == 2
            assert user.type == "user"
            assert is_admin() is False

            # Set the user's updated type
            user = Users.query.filter_by(id=2).first()
            user.type = "admin"
            app.db.session.commit()

            # Should still return False because this is still cached
            assert is_admin() is False

            clear_user_session(user_id=2)

            # Should now return True after clearing cache
            assert is_admin() is True
    destroy_tourney(app)


def test_clear_all_user_sessions():
    app = create_tourney()
    with app.app_context():
        register_user(app)

        # Users by default should have a non-admin type
        user = Users.query.filter_by(id=2).first()
        with app.test_request_context("/"):
            login_user(user)
            user = get_current_user()
            assert user.id == 2
            assert user.type == "user"
            assert is_admin() is False

            # Set the user's updated type
            user = Users.query.filter_by(id=2).first()
            user.type = "admin"
            app.db.session.commit()

            # Should still return False because this is still cached
            assert is_admin() is False

            clear_all_user_sessions()

            # Should now return True after clearing cache
            assert is_admin() is True
    destroy_tourney(app)


def test_cache_subclass_commands():
    app = create_tourney()
    with app.app_context():
        from Tourney.cache import cache

        cache.inc("testing_inc")
        resp = cache.inc("testing_inc")
        assert resp == 2
        assert cache.get("testing_inc") == 2
        cache.expire("testing_inc", 0)
        assert cache.get("testing_inc") is None
        resp = cache.inc("testing_inc")
        assert resp == 1
    destroy_tourney(app)


def test_redis_cache_subclass_commands():
    class RedisConfig(TestingConfig):
        REDIS_URL = "redis://localhost:6379/1"
        CACHE_REDIS_URL = "redis://localhost:6379/1"
        CACHE_TYPE = "redis"

    try:
        app = create_tourney(config=RedisConfig)
    except ConnectionError:
        print("Failed to connect to redis. Skipping test.")
    else:
        with app.app_context():
            from Tourney.cache import cache

            cache.inc("testing_inc")
            resp = cache.inc("testing_inc")
            assert resp == 2
            assert cache.get("testing_inc") == 2
            cache.expire("testing_inc", 0)
            assert cache.get("testing_inc") is None
            resp = cache.inc("testing_inc")
            assert resp == 1
        destroy_tourney(app)
