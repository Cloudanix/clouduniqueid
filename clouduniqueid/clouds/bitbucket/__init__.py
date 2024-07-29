

from .uniqueid import unique_id_patterns
import logging
import re
from typing import Dict

logger = logging.getLogger(__name__)


def check_missing_data_keys(dataKeys: list, uniqueIdFormat: str):
    uniqueIdKeys = re.findall(r"{(.*?)}", uniqueIdFormat)
    missingKeys = [key for key in uniqueIdKeys if key.lower() not in dataKeys]
    return missingKeys


class BitbucketUniqueId:
    def get_unique_id(
        self,
        resourceType: str,
        data: Dict,
        service: str = 'bitbucket',
    ) -> str:
        uniqueIds: Dict = unique_id_patterns
        data = {k.lower().replace("_", ""): v for k, v in data.items()}
        dataKeys = list(data.keys())

        if service not in uniqueIds:
            logger.error(f"Bitbucket service {service} unknown")
            return ""

        if resourceType not in uniqueIds[service]:
            logger.error(f"Bitbucket service {service} resource type {resourceType} not supported")
            return ""

        uniqueIdFormat = uniqueIds[service][resourceType]

        missingKeys = check_missing_data_keys(dataKeys, uniqueIdFormat)
        if missingKeys:
            errorMsg = ", ".join(missingKeys)
            logger.error(f"Bitbucket {errorMsg} keys required in data parameter")
            return ""

        try:
            uniqueId = uniqueIdFormat.format(**data).replace(" ", "")
            return uniqueId
        except KeyError as e:
            logger.error(f"Missing data for key: {e}")
            return ""

    def get_unique_id_format(self, resourceType: str) -> str:
        uniqueIds: Dict = unique_id_patterns

        if resourceType not in uniqueIds.get('bitbucket', {}):
            logger.error(f"Bitbucket resource type {resourceType} not supported")
            return ""

        return uniqueIds['bitbucket'][resourceType].replace(" ", "")
