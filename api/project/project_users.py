'''
Copyright 2024 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Wed Apr 03 2024
File : project_users.py
'''
import logging
import requests

logger = logging.getLogger(__name__)

#------------------------------------------------------------------------------------------#
def get_project_users_by_role(projectID, role, baseURL, authToken):
    logger.info("    Entering get_project_users_by_role")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL + str(projectID) + "/users?roleId=" + role

    logger.debug("        RESTAPI_URL: %s" %RESTAPI_URL)

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
        logger.info("    Project users gathered.")
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}

#------------------------------------------------------------------------------------------#
def remove_project_users_by_role(projectID, role, usersToRemove, baseURL, authToken):
    logger.info("    Entering get_project_users_by_role")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL + str(projectID) + "/users"

    logger.debug("        RESTAPI_URL: %s" %RESTAPI_URL)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    # This is list of user so put in the proper format
    users = '"'
    users += '", "'.join(usersToRemove)
    users += '"'

    updateBody = '''
            {
                "roleId": "%s",
                "users": [
                    %s
                ]
            } '''  %(role, users)
    
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.delete(RESTAPI_URL, headers=headers, data=updateBody.encode('utf-8'))
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Users remvoed from project role: %s." %role)
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}
    
#------------------------------------------------------------------------------------------#
def add_project_users_by_role(projectID, role, usersToAdd, baseURL, authToken):
    logger.info("    Entering add_project_users_by_role")

    RESTAPI_BASEURL = baseURL + "/codeinsight/api/"
    ENDPOINT_URL = RESTAPI_BASEURL + "projects/"
    RESTAPI_URL = ENDPOINT_URL + str(projectID) + "/users"

    logger.debug("        RESTAPI_URL: %s" %RESTAPI_URL)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + authToken} 

    # This is list of user so put in the proper format
    users = '"'
    users += '", "'.join(usersToAdd)
    users += '"'

    updateBody = '''
            {
                "userRoles": {
                    "roleId": "%s",
                    "users": [
                        %s
                    ]
                }
            } '''  %(role, users)
    
    ##########################################################################   
    # Make the REST API call with the project data           
    try:
        response = requests.post(RESTAPI_URL, headers=headers, data=updateBody.encode('utf-8'))
    except requests.exceptions.RequestException as error:  # Just catch all errors
        logger.error(error)
        return {"error" : error}

    ###############################################################################
    # We at least received a response from FNCI so check the status to see
    # what happened if there was an error or the expected data
    if response.status_code == 200:
        logger.info("    Users added to project role: %s." %role)
        return response.json()
    else:
        logger.error("Response code %s - %s" %(response.status_code, response.text))
        return {"error" : response.text}