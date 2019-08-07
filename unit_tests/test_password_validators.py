from django.contrib.auth.password_validation import MinimumLengthValidator, ValidationError
from shopozor.password_validation import NumberAndLetterValidator, SpecialCharacterValidator, HasBeenPwndValidator

import pytest


@pytest.mark.parametrize(
    "pwned_password",
    [
        "p@ssword", "p@ssword1", "@123", "asdf1234"
    ],
)
def test_has_been_pwnd_not_valid(pwned_password):
    with pytest.raises(ValidationError):
        HasBeenPwndValidator().validate(pwned_password)


@pytest.mark.parametrize(
    "valid_password",
    [
        "@asdf1", "p@ssword1", "fdsjlkwern23", "asdf1234"
    ],
)
def test_number_and_letter_validator_valid(valid_password):
    NumberAndLetterValidator().validate(valid_password)


@pytest.mark.parametrize(
    "invalid_password",
    [
        "@sdf", "@*123", "p@ssword", "@123"
    ],
)
def test_number_and_letter_validator_not_valid(invalid_password):
    with pytest.raises(ValidationError):
        NumberAndLetterValidator().validate(invalid_password)


@pytest.mark.parametrize(
    "valid_password",
    [
        "@sdf", "@asdf1", "@*123", "p@ssword", "p@ssword1", "@123"
    ],
)
def test_special_character_validator_valid(valid_password):
    SpecialCharacterValidator().validate(valid_password)


@pytest.mark.parametrize(
    "invalid_password",
    [
        "fdsjlkwern23", "asdf1234"
    ],
)
def test_special_character_validator_not_valid(invalid_password):
    with pytest.raises(ValidationError):
        SpecialCharacterValidator().validate(invalid_password)
