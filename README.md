# 2024-06-05 demonstration of pip bug with logging

## Setup

To test this out, create a venv:

    python -m venv .venv
    source .venv/bin/activate

Install deps (this installed keyring, plus a custom keyring backend defined in ./my-backend):

    pip install -r requirements.txt

## Demo

I'm able to reproduce the issue described here with these versions of Python
and pip:

    $ pip --version
    pip 24.0 from ...
    $ python --version
    Python 3.11.9

Note how `pip install` can succesfully use our custom backend (the creds it returns don't
actually work, but that's because `https://httpstat.us/401` unconditionally
returns a HTTP 401):

    $ pip -v --keyring-provider import install --index-url https://httpstat.us/401 requests
    Using pip 24.0 from /home/jeremy/tmp/2024-06-05-pyhack-2/.direnv/python-3.11.9/lib/python3.11/site-packages/pip (python 3.11)
    Looking in indexes: https://httpstat.us/401
    Keyring provider requested: import
    Keyring provider set: import
    Hello from JflyBackend::get_credential. I'm about to log a message
    Successfully logged a message. Now I'm going to return a credential
    WARNING: 401 Error, Credentials not correct for https://httpstat.us/401/requests/
    ERROR: Could not find a version that satisfies the requirement requests (from versions: none)
    ERROR: No matching distribution found for requests


Now check out what happens if we crank the logging up to `-vv`. Note how we see
the "I'm about to log a message" message, and then the next thing is pip giving
up on the backend ("WARNING: Keyring is skipped due to an exception"):

    $ pip -vv --keyring-provider import install --index-url https://httpstat.us/401 requests
    Using pip 24.0 from /home/jeremy/tmp/2024-06-05-pyhack-2/.direnv/python-3.11.9/lib/python3.11/site-packages/pip (python 3.11)
    Non-user install because user site-packages disabled
    Created temporary directory: /run/user/1000/pip-build-tracker-nn_sm5wc
    Initialized build tracking at /run/user/1000/pip-build-tracker-nn_sm5wc
    Created build tracker: /run/user/1000/pip-build-tracker-nn_sm5wc
    Entered build tracker: /run/user/1000/pip-build-tracker-nn_sm5wc
    Created temporary directory: /run/user/1000/pip-install-ym1lagii
    Created temporary directory: /run/user/1000/pip-ephem-wheel-cache-h6x7xfz9
    Looking in indexes: https://httpstat.us/401
    1 location(s) to search for versions of requests:
    * https://httpstat.us/401/requests/
    Fetching project page and analyzing links: https://httpstat.us/401/requests/
    Getting page https://httpstat.us/401/requests/
    Found index url https://httpstat.us/401/
    Looking up "https://httpstat.us/401/requests/" in the cache
    Request header has "max_age" as 0, cache bypassed
    No cache entry available
    Starting new HTTPS connection (1): httpstat.us:443
    https://httpstat.us:443 "GET /401/requests/ HTTP/1.1" 401 16
    Found index url https://httpstat.us/401/
    Keyring provider requested: import
    Keyring provider set: import
    Getting credentials from keyring for https://httpstat.us/401/
    Loading jfly backend
    Loading KWallet
    Loading SecretService
    Loading Windows
    Loading chainer
    Loading libsecret
    Loading macOS
    Hello from JflyBackend::get_credential. I'm about to log a message
    WARNING: Keyring is skipped due to an exception:
    Keyring provider requested: import
    Keyring provider set: disabled
    User for httpstat.us:
