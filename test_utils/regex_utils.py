def regex_url_uid_token():
    return r'\/(?P<uidb64>[0-9A-Za-z_\-]+)\/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'