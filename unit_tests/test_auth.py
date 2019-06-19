from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from saleor.account.models import User

import pytest


@pytest.mark.django_db
def test_user_pk_should_be_integer():
    user = User.objects.create_user(email='test@shopozor.ch')
    assert isinstance(user.pk, int)


@pytest.mark.parametrize(
    "user_id",
    [
        1,
        2,
        100,
        1578
    ],
)
def test_encoded_userid_should_be_decoded_from_url(user_id):
    encoded_user_id = urlsafe_base64_encode(force_bytes(user_id))
    decoded_user_id = force_text(urlsafe_base64_decode(encoded_user_id))
    assert user_id == int(decoded_user_id)

# TODO: test that the send password reset email uses the above encoded_user_id
