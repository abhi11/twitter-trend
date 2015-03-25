#!/usr/bin/env python

"""
Module to have utility classes. The classes
defined here will be used by others.
"""

# Copyright (C) 2015  G Nithin

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

################################################################################

#Imports that will fail in 3+
try:
    import httplib
except ImportError:
    import http.client as httplib

class https_req:
    def __init__(self, domain):
        self._conn = httplib.HTTPSConnection(domain)

    def get_conn(self):
        """
        Returns connection object.
        """
        return self._conn

    def make_req(self, uri, request_method, params, headers):
        """
        Performs request and returns payload.
        Returns None if unsuccessful.
        Note: This does not close the connection upon exit.
        """
        self._conn.request(request_method, uri, params, headers)
        response = self._conn.getresponse()

        payload = response.read()
        return payload

    def close_conn(self):
        """
        Closes connection.
        """
        if self._conn != None:
            self._conn.close()
