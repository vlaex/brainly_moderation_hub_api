from enum import Enum


def make_db_choices_from_enum(e: Enum) -> list[tuple[str, str]]:
    choices = [(member.name, member.value) for member in e]

    return choices
