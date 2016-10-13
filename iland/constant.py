# -*- coding: utf-8 -*-

"""A library that provides constants for the `iland.Api` object."""

#: Base URL to the iland cloud API.
BASE_URL = 'https://api.ilandcloud.com/ecs'

#: Access token URL.
ACCESS_URL = \
    'https://ecs.ilandcloud.com/auth/realms/iland-core/' \
    + 'protocol/openid-connect/token'

#: Refresh token URL. (`refresh` query param is here only for mock
# testing reason)
REFRESH_URL = ACCESS_URL + '?refresh=1'
