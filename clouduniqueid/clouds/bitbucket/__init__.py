import logging
import re
from typing import Dict

from .uniqueid import unique_id_patterns

logger = logging.getLogger(__name__)


def check_missing_data_keys(dataKeys: list, uniqueIdFormat: str):
    uniqueIdKeys = re.findall(r'{(.*?)}', uniqueIdFormat)
    print(uniqueIdKeys)
    print(uniqueIdFormat)
    missingKeys = []

    for key in uniqueIdKeys:
        if key.lower() not in dataKeys:
            missingKeys.append(key)

    return missingKeys


class BitbucketUniqueId:
    def __init__(self):
        self.valid_services = ["bitbucket"]
        self.valid_resource_types = ["workspace", "member", "project", "repository"]

    def get_unique_id(self, resourceType: str, data: Dict, service: str = 'Bitbucket'):
        if service not in self.valid_services:
            return ""

        if resourceType not in self.valid_resource_types:
            return ""

        unique_id = f"{service}:"

        if resourceType == "workspace":
            workspace = data.get("workspace", "")
            unique_id += workspace

        elif resourceType == "member":
            workspace = data.get("workspace", "")
            member = data.get("member", "")
            if workspace and member:
                unique_id += f"{workspace}:{member}"
            else:
                return ""

        elif resourceType == "project":
            workspace = data.get("workspace", "")
            project = data.get("project", "")
            if workspace and project:
                unique_id += f"{workspace}:{project}"
            #else:
                #return ""  # Return empty if workspace or project is missing

        elif resourceType == "repository":
            workspace = data.get("workspace", "")
            project = data.get("project", "")
            repository = data.get("repository", "")
            if workspace and project and repository:
                unique_id += f"{workspace}:{project}:{repository}"
            else:
                return ""

        return unique_id


# class BitbucketUniqueId:
#     def get_unique_id(
#         self,
#         resourceType: str,
#         data: Dict,
#         service: str = 'bitbucket'

#     ) -> str:
#         uniqueIds: Dict = unique_id_patterns
#         data = {k.lower().replace("_", ""): v for k, v in data.items()}
#         dataKeys = list(data.keys())

#         if not uniqueIds.get("bitbucket", None):
#             logger.error(f"Bitbucket service unknown")
#             return ""

#         elif not uniqueIds.get("bitbucket", {}).get(resourceType, None):
#             logger.error(
#                 f"Bitbucket service resource type {resourceType} not supported",
#             )
#             return ""

#         else:
#             uniqueIdFormat = (
#                 uniqueIds["bitbucket"][resourceType]
#                 .replace(" ", "")
#             )
#             missingKeys = check_missing_data_keys(dataKeys, uniqueIdFormat)
#             if len(missingKeys) > 0:
#                 errorMsg = ", ".join(missingKeys)
#                 logger.error(f"Bitbucket {errorMsg} keys required in data parameter")
#                 return ""

#             else:
#                 return eval(f"f'{uniqueIdFormat}'").replace(" ", "")


# if __name__ == "__main__":
#     bitbucket_unique_id = BitbucketUniqueId()
#     example_data = {
#         "workspace": "my_workspace",
#         "member": "my_member",
#         "project": "my_project",
#         "repository": "my_repository"
#     }
