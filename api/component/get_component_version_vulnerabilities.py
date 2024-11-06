'''
Copyright 2020 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sarthak  
Created On : wed Oct 16 2024
File : get_component_version_vulnerabilities.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_component_version_vulnerabilities(baseURL, componentVersionID, authToken):
    logger.info("Entering get_component_version_vulnerabilities")
    APIOPTIONS = ""
    componentVersionVulnerabilities = get_component_details_with_options(baseURL, componentVersionID, authToken, APIOPTIONS)
    return componentVersionVulnerabilities

#------------------------------------------------------------------------------------------#
def get_component_details_with_options(baseURL, componentVersionID, authToken, APIOPTIONS):
    logger.info("Entering get_component_version_vulnerabilities with options")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "components/" + str(componentVersionID) + "/vulnerabilities" + "?offset=" 
    RESTAPI_URL = ENDPOINT_URL + "1" + APIOPTIONS
    logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
    
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 
    
    ##########################################################################   
    # Make the REST API call with the component version data           
    try:
        response = requests.get(RESTAPI_URL, headers=headers)
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Component version vulnerabilities details retreived")
        componentDetails = response.json()
        currentPage = response.headers["Current-page"]
        numPages = response.headers["Number-of-pages"]
        nextPage = int(currentPage) + 1

        while int(nextPage) <= int(numPages):
            RESTAPI_URL = ENDPOINT_URL + str(nextPage) + APIOPTIONS
            logger.debug("    RESTAPI_URL: %s" %RESTAPI_URL)
            response = requests.get(RESTAPI_URL, headers=headers)
            nextPage = int(nextPage) + 1
            componentDetails["data"] += response.json()["data"]
        return componentDetails
    elif response.status_code == 400:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Bad Request" %response.status_code )
        response.raise_for_status()
    elif response.status_code == 401:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        print("Response code: %s   -  Unauthorized" %response.status_code )
        response.raise_for_status() 
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}