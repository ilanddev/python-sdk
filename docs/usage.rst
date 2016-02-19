=====
Usage
=====

To use iland-sdk in a project::

    import iland

The API is exposed via the ``iland.Api`` class.

To create an instance of the ``iland.Api``::

    >>> import iland
    >>> api = iland.Api(client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        username=USERNAME,
                        password=PASSWORD)

You can then perform GET, PUT, PUSH and DELETE requests against the iland
cloud::

    >>> user = api.get('/user/' + USERNAME)
    >>> user.get('name'))
    USERNAME

    >>> user_alert_emails = {'emails': ['test@iland.com', 'test2@iland.com'],
                             'username': USERNAME}
    >>> api.post('/user/' + USERNAME + '/alert-emails', user_alert_emails)

