import logging
from typing import Dict

from .uniqueid import unique_ids

logger = logging.getLogger(__name__)


class AWSUniqueId:
    def get_unique_id(
        self, service: str, resourceType: str, resource: str, parent: str = None, groupId: str = None,
        accountId: str = None, region: str = None, partition: str = 'aws', UUID: str = None,
        launchConfigurationId: str = None, imageTag: str = None, loadBalancerId: str = None, listenerId: str = None,
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

        elif 'UUID' in uniqueIds[service][resourceType] and not UUID:
            logger.error("AWS UUID required")
            raise ValueError("Invalid parameters provided, AWS UUID required")

        elif 'groupId' in uniqueIds[service][resourceType] and not groupId:
            logger.error("AWS groupId required")
            raise ValueError("Invalid parameters provided, AWS groupId required")

        elif 'launchConfigurationId' in uniqueIds[service][resourceType] and not launchConfigurationId:
            logger.error("AWS launchConfigurationId required")
            raise ValueError("Invalid parameters provided, AWS launchConfigurationId required")

        elif 'imageTag' in uniqueIds[service][resourceType] and not imageTag:
            logger.error("AWS imageTag required")
            raise ValueError("Invalid parameters provided, AWS imageTag required")

        elif 'loadBalancerId' in uniqueIds[service][resourceType] and not loadBalancerId:
            logger.error("AWS loadBalancerId required")
            raise ValueError("Invalid parameters provided, AWS loadBalancerId required")

        elif 'listenerId' in uniqueIds[service][resourceType] and not listenerId:
            logger.error("AWS listenerId required")
            raise ValueError("Invalid parameters provided, AWS listenerId required")

        elif resource.replace(" ", "") == "" or not resource:
            logger.error("AWS resource required")
            raise ValueError("Invalid parameters provided, AWS resource required")

        else:
            return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")
