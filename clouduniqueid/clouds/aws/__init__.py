import logging
from typing import Dict

from .uniqueid import get_uniqueid

logger = logging.getLogger(__name__)


class AWSUniqueId:
    def get_console_link(self,service: str, resourceType: str, resourceName: str) -> str:
        logger.info(f"Start Process for AWS Resource: {resourceName}")

        uniqueIds = get_uniqueid
        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            raise ValueError(f"AWS service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(f"AWS service {service} resource type {resourceType} not supported")
            raise ValueError(f"AWS service {service} resource type {resourceType} not supported")

        else:
            return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")