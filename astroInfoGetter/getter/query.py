#! /usr/bin/env python

import numpy as np
import requests
from IPython.display import display, HTML
import sys
import os
import time
import re
import json
from urllib.parse import quote as urlencode
from urllib.request import urlretrieve
import http.client as httplib
from astropy.table import Table


# def mastQuery(req):

#    """Basic mast query maker. Similar to
#    example code from astroquery documentation """

#    server='mast.stsci.edu'

#    version = ".".join(map(str, sys.version_info[:3]))

# HTTP header variables for request
#    headers = {"Content-type": "application/x-www-form-urlencoded",
#               "Accept": "text/plain",
#               "User-agent":"python-requests/"+version}

# Make request string
#    reqStr = json.dumps(req)
#    reqStr = urlencode(reqStr)

# Open https connection
#    conn = httpcli.HTTPSConnection(server)

# Run the query
#    conn.request("POST", "api/v0/invoke", "request="+reqStr, headers)

# Get and save the response
#    resp = conn.getresponse()
# Save headers
#    head = resp.getheaders()
# Save content of response
#    content = resp.read().decode('utf-8')

# Close connection
#    conn.close()

#    return head,content


def mastQuery(request):
    """Perform a MAST query.
    
        Parameters
        ----------
        request (dictionary): The MAST request json object
        
        Returns head,content where head is the response HTTP headers, and content is the returned data"""

    server = "mast.stsci.edu"

    # Grab Python Version
    version = ".".join(map(str, sys.version_info[:3]))

    # Create Http Header Variables
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
        "User-agent": "python-requests/" + version,
    }

    # Encoding the request as a json string
    requestString = json.dumps(request)
    requestString = urlencode(requestString)

    # opening the https connection
    conn = httplib.HTTPSConnection(server)

    # Making the query
    conn.request("POST", "/api/v0/invoke", "request=" + requestString, headers)

    # Getting the response
    resp = conn.getresponse()
    head = resp.getheaders()
    content = resp.read().decode("utf-8")

    # Close the https connection
    conn.close()

    return head, content
