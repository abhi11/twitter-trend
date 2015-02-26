#Imports that will fail in 3+
try:
    import httplib
except ImportError:
    import http.client as httplib

import urllib

class https_req:
    def __init__(self, domain):
        self._conn = httplib.HTTPSConnection(domain)

    def _get_conn(self):
        """
        Returns connection object.
        """
        return self._conn

    def _make_req(self, uri, request_method, params, headers):
        """
        Performs request and returns payload.
        Returns None if unsuccessful.
        Note: This does not close the connection upon exit.
        """
        self._conn.request(request_method, uri, params, headers)
        response = self._conn.getresponse()

        payload = response.read()
        return payload

    def _close_conn(self):
        """
        Closes connection.
        """
        if self._conn != None:
            self._conn.close()
