from random import choice
from string import ascii_letters, digits
from reportes.models import Usuario


def alphanumeric_password():
    length = 16
    characters = ascii_letters + digits
    password = ''.join(choice(characters) for _ in range(length))

    print(password)

    return password


def user_update_or_create(
    model: Usuario,
    data: dict,
):
    """

    """
