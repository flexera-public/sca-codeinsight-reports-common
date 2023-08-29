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

    # Create a list of project data sorted by the project name at each level for report display  
    # Add details for the parent node
    nodeDetails = {}
    nodeDetails["projectID"] = projectID
    nodeDetails["parent"] = "#"  # The root node
    nodeDetails["projectName"] = projectName
    nodeDetails["projectID"] = projectID
    nodeDetails["projectLink"] = baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + str(projectID) + "&tab=projectInventory"

    projectList.append(nodeDetails)

    if includeChildProjects:
        projectList = manage_child_projects(projectHierarchy, projectID, projectList, baseURL)


    return projectList


#----------------------------------------------#
def manage_child_projects(project, parentID, projectList, baseURL):
    logger.debug("Entering manage_child_projects")

    # Are there more child projects for this project?
    if len(project["childProject"]):

        # Sort by project name of child projects
        for childProject in sorted(project["childProject"], key = lambda i: i['name'] ) :

            nodeDetails = {}
            nodeDetails["projectID"] = str(childProject["id"])
            nodeDetails["parent"] = parentID
            nodeDetails["projectName"] = childProject["name"]
            nodeDetails["projectLink"] = baseURL + "/codeinsight/FNCI#myprojectdetails/?id=" + str(childProject["id"]) + "&tab=projectInventory"

            projectList.append( nodeDetails )

            manage_child_projects(childProject, childProject["id"], projectList, baseURL)

    return projectList