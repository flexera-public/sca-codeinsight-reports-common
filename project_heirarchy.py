'''
Copyright 2023 Flexera Software LLC
See LICENSE.TXT for full license text
SPDX-License-Identifier: MIT

Author : sgeary  
Created On : Fri Aug 25 2023
File : project_heirarchy.py
'''
import logging
logger = logging.getLogger(__name__)

import common.api.project.get_child_projects


def create_project_heirarchy(baseURL, authToken, projectID, includeChildProjects):

    projectList = [] # List to hold parent/child details for report

    # Get the list of parent/child projects start at the base project
    projectHierarchy = common.api.project.get_child_projects.get_child_projects_recursively(baseURL, projectID, authToken)
    projectName = projectHierarchy["name"]

    logger.info("=" * 80)
    logger.info("Building hierarchy for root project: %s (ID: %s)" % (projectName, projectID))
    logger.info("=" * 80)

    # Create a list of project data sorted by the project name at each level for report display  
    # Add details for the parent node
    nodeDetails = {}
    nodeDetails["projectID"] = str(projectID)
    nodeDetails["uniqueID"] = str(projectID)  # Root node unique ID is just the project ID
    nodeDetails["parent"] = "#"  # The root node
    nodeDetails["projectName"] = projectName
    nodeDetails["projectLink"] = baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + str(projectID) + "&tab=projectInventory"
    nodeDetails["inventoryLinkBase"] = nodeDetails["projectLink"]  + "&pinv="

    logger.info("Adding ROOT: name='%s', id='%s', uniqueID='%s', parent='%s'" % (nodeDetails["projectName"], nodeDetails["projectID"], nodeDetails["uniqueID"], nodeDetails["parent"]))
    projectList.append(nodeDetails)

    if includeChildProjects:
        projectList = manage_child_projects(projectHierarchy, str(projectID), str(projectID), projectList, baseURL)

    logger.info("=" * 80)
    logger.info("FINAL PROJECT HIERARCHY LIST (%d projects):" % len(projectList))
    logger.info("=" * 80)
    for idx, proj in enumerate(projectList):
        logger.info("[%2d] name='%s', id='%s', uniqueID='%s', parent='%s'" % (idx, proj["projectName"], proj["projectID"], proj.get("uniqueID", proj["projectID"]), proj["parent"]))
    logger.info("=" * 80)

    return projectList


#----------------------------------------------#
def manage_child_projects(project, parentID, parentUniqueID, projectList, baseURL):
    logger.debug("Entering manage_child_projects for parentID: %s, parentUniqueID: %s" % (parentID, parentUniqueID))

    # Are there more child projects for this project?
    if len(project["childProject"]):
        logger.info("  Parent '%s' (ID=%s, UniqueID=%s) has %d child projects" % (project.get("name", "?"), parentID, parentUniqueID, len(project["childProject"])))

        # Sort by project name of child projects
        for childProject in sorted(project["childProject"], key = lambda i: i['name'] ) :

            childID = str(childProject["id"])
            # Create unique ID by combining parent's unique ID with child's ID
            # This ensures each node in the tree has a unique identifier
            childUniqueID = parentUniqueID + "_" + childID

            nodeDetails = {}
            nodeDetails["projectID"] = childID
            nodeDetails["uniqueID"] = childUniqueID
            nodeDetails["parent"] = parentUniqueID  # Use parent's unique ID
            nodeDetails["projectName"] = childProject["name"]
            nodeDetails["projectLink"] = baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + childID + "&tab=projectInventory"
            nodeDetails["inventoryLinkBase"] = nodeDetails["projectLink"]  + "&pinv="

            logger.info("    Adding CHILD: name='%s', id='%s', uniqueID='%s', parent='%s'" % (nodeDetails["projectName"], nodeDetails["projectID"], nodeDetails["uniqueID"], nodeDetails["parent"]))
            projectList.append( nodeDetails )

            # Recurse with child's unique ID
            manage_child_projects(childProject, childID, childUniqueID, projectList, baseURL)

    return projectList