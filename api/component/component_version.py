'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Thu Apr 04 2024
File : component_version.py
'''

import logging, requests

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------------------#
def get_component_versions_details(baseURL, authToken, componentVersionId):
    logger.info("Entering get_component_versions_details")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    RESTAPI_URL = RESTAPI_BASEURL + "components/versions/%s" %componentVersionId
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken}   
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}
        
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Component version information received")
        licenseInformation = response.json()["data"]

        return licenseInformation

    else:
        return {"error" : response.text}


