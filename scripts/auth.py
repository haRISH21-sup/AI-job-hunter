from scripts.database import (
    get_connection,
    initialize_database
)

import hashlib


def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def register_user(
        username,
        password
):

    initialize_database()

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users
            (
                username,
                password
            )
            VALUES (?, ?)
            """,
            (
                username,
                hash_password(password)
            )
        )

        conn.commit()

        return True

    except:

        return False

    finally:

        conn.close()


def login_user(
        username,
        password
):

    conn = get_connection()
    cursor = conn.cursor()

    print("USERNAME:", username)

    print(
        "HASH:",
        hash_password(password)
    )

    cursor.execute(
        """
        SELECT
            id,
            username
        FROM users
        WHERE username=?
        AND password=?
        """,
        (
            username,
            hash_password(password)
        )
    )

    user = cursor.fetchone()

    print("USER:", user)

    conn.close()

    return user


def get_user_id(
        username
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM users
        WHERE username=?
        """,
        (
            username,
        )
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        return user[0]

    return None