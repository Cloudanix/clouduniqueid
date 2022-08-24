import logging
from typing import Dict

from .uniqueid import unique_ids

logger = logging.getLogger(__name__)


class AWSUniqueId:
    def get_unique_id(
        self, service: str, resourceType: str, resource: str, parent: str = None,
        accountId: str = None, region: str = None, partition: str = 'aws',
    ) -> str:

        uniqueIds: Dict = unique_ids

        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            raise ValueError(f"AWS service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(f"AWS service {service} resource type {resourceType} not supported")
            raise ValueError(f"AWS service {service} resource type {resourceType} not supported")

        elif 'accountId' in uniqueIds[service][resourceType] and not accountId:
            logger.error("AWS accountId required")
            raise ValueError("Invalid parameters provided, AWS accountId required")

        elif 'region' in uniqueIds[service][resourceType] and not region:
            logger.error("AWS region required")
            raise ValueError("Invalid parameters provided, AWS region required")

        elif 'parent' in uniqueIds[service][resourceType] and not parent:
            logger.error("AWS parent required")
            raise ValueError("Invalid parameters provided, AWS parent required")

        elif resource.replace(" ", "") == "" or not resource:
            logger.error("AWS resource required")
            raise ValueError("Invalid parameters provided, AWS resource required")

        else:
            return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")
