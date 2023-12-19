'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Mon Dec 14 2020
File : license_lookup.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_license_details(baseURL, selectedLicenseID, authToken):
    logger.info("Entering get_license_details")

    APIOPTIONS = "licenseId=" + str(selectedLicenseID)
    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "license/lookup?" 
    RESTAPI_URL = ENDPOINT_URL + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
       
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"errorMsg" : error}
        
    
    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    License information received")
        licenseInformation = response.json()["Content: "]

        return licenseInformation

    else:
        return {"errorMsg" : response.text}