

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

    def get_unique_id(self, resourceType: str, data: Dict, service: str = 'bitbucket') -> str:

        data = {k.lower().replace("_", ""): v for k, v in data.items()}
        data_keys = list(data.keys())

        if service not in unique_id_patterns:
            logger.error(f"Service {service} unknown")
            return ""

        if resourceType not in unique_id_patterns[service]:
            logger.error(f"Service {service} resource type {resourceType} not supported")
            return ""

        unique_id_format = unique_id_patterns[service][resourceType]
        missing_keys = check_missing_data_keys(data_keys, unique_id_format)

        if missing_keys:
            error_msg = ", ".join(missing_keys)
            logger.error(f"Bitbucket {error_msg} keys required in data parameter")
            return ""

        return eval(f"f'{unique_id_format}'".format(**data)).replace(" ", "")

    def get_unique_id_format(resourceType: str) -> str:
        if resourceType not in unique_id_patterns.get('bitbucket', {}):
            logger.error(f"Bitbucket resource type {resourceType} not supported")
            return ""

        return unique_id_patterns['bitbucket'][resourceType].replace(" ", "")
