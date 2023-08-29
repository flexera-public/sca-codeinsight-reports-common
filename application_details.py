'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Aug 25 2023
File : application_details.py
'''
import logging
import common.api.project.get_project_information
logger = logging.getLogger(__name__)

#----------------------------------------------#
def determine_application_details(projectID, baseURL, authToken):
    logger.debug("Entering determine_application_details.")
    # Create a application name for the report if the custom fields are populated
    # Default values
    applicationName = None
    applicationVersion = None
    applicationPublisher = None

    projectInformation = common.api.project.get_project_information.get_project_information_summary(baseURL, projectID, authToken)
 
    # Project level custom fields added in 2022R1
    if "customFields" in projectInformation:
        customFields = projectInformation["customFields"]

        # See if the custom project fields were propulated for this project
        for customField in customFields:

            # Is there the reqired custom field available?
            if customField["fieldLabel"] == "Application Name":
                if customField["value"] is not None and customField["value"] != "":
                    applicationName = customField["value"]

            # Is the custom version field available?
            if customField["fieldLabel"] == "Application Version":
                if customField["value"] is not None and customField["value"] != "":
                    applicationVersion = customField["value"]     

            # Is the custom Publisher field available?
            if customField["fieldLabel"] == "Application Publisher":
                if customField["value"] is not None and customField["value"] != "":
                    applicationPublisher = customField["value"]    

    # Join the custom values to create the application name for the report artifacts
    if applicationName is None:
        applicationName = projectInformation["name"]

    if applicationVersion is None:
        applicationNameVersion = applicationName
    else:
        applicationNameVersion = applicationName + " - " + applicationVersion

    if applicationPublisher is None:
        applicationDocumentString = applicationNameVersion        
    else:
        applicationDocumentString = applicationPublisher + " - " + applicationNameVersion
    
    applicationDetails = {}
    applicationDetails["applicationName"] = applicationName
    applicationDetails["applicationVersion"] = applicationVersion
    applicationDetails["applicationPublisher"] = applicationPublisher
    applicationDetails["applicationNameVersion"] = applicationNameVersion
    applicationDetails["applicationDocumentString"] = applicationDocumentString

    logger.info("    applicationDetails: %s" %applicationDetails)

    return applicationDetails

