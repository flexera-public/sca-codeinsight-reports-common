'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Apr 03 2024
File : project_contact.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def update_project_contact(projectID, user, baseURL, authToken ):
    logger.info("    Entering update_project_contact")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL + str(projectID) + "/contact"

    logger.debug("        RESTAPI_URL: %s" %RESTAPI_URL)

    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    updateBody = '''
            {
                "contact": "%s"
            }''' %user

    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.put(RESTAPI_URL, headers=headers, data=updateBody.encode('utf-8'))
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Project Contact Updated.")
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}
