from django.core.exceptions import ValidationError
from shopozor.password_validation import NumberAndLetterValidator, SpecialCharacterValidator, HasBeenPwndValidator

import pytest

# password database:"@sdf","@asdf1","@*123","fdsjlkwern23","p@ssword","p@ssword1","@123","asdf1234"


@pytest.mark.parametrize(
    "password_has_been_pwnd_valid",
    [
        "@sdf", "@asdf1", "@*123", "fdsjlkwern23"
    ],
)
def test_has_been_pwn_valid(password_has_been_pwnd_valid):
    try:
        assert HasBeenPwndValidator().is_valid_password(password_has_been_pwnd_valid)
    except ValidationError as exception:
        if exception.code == HasBeenPwndValidator().error_not_reachable:
            assert True
        else:
            assert False


@pytest.mark.parametrize(
    "password_has_been_pwnd_not_valid",
    [
        "p@ssword", "p@ssword1", "@123", "asdf1234"
    ],
)
def test_has_been_pwn_not_valid(password_has_been_pwnd_not_valid):
    try:
        assert not HasBeenPwndValidator().is_valid_password(
            password_has_been_pwnd_not_valid)
    except ValidationError as exception:
        if exception.code == HasBeenPwndValidator().error_not_reachable:
            assert True
        else:
            assert False


@pytest.mark.parametrize(
    "password_number_and_letter_valid",
    [
        "@asdf1", "p@ssword1", "fdsjlkwern23", "asdf1234"
    ],
)
def test_number_and_letter_validator_valid(password_number_and_letter_valid):
    assert NumberAndLetterValidator().is_valid_password(
        password_number_and_letter_valid)


@pytest.mark.parametrize(
    "password_number_and_letter_not_valid",
    [
        "@sdf", "@*123", "p@ssword", "@123"
    ],
)
def test_number_and_letter_validator_not_valid(password_number_and_letter_not_valid):
    assert not NumberAndLetterValidator().is_valid_password(
        password_number_and_letter_not_valid)


@pytest.mark.parametrize(
    "password_special_character_valid",
    [
        "@sdf", "@asdf1", "@*123", "p@ssword", "p@ssword1", "@123"
    ],
)
def test_special_character_validator_valid(password_special_character_valid):
    assert SpecialCharacterValidator().is_valid_password(
        password_special_character_valid)


@pytest.mark.parametrize(
    "password_special_character_not_valid",
    [
        "fdsjlkwern23", "asdf1234"
    ],
)
def test_special_character_validator_not_valid(password_special_character_not_valid):
    assert not SpecialCharacterValidator().is_valid_password(
        password_special_character_not_valid)
