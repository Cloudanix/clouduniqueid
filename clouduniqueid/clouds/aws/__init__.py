import logging
import re
from typing import Dict

from .uniqueid import unique_ids

logger = logging.getLogger(__name__)


def check_absent_data_keys(dataKeys: list, uniqueIdFormat: str):
    uniqueIdKeys = re.findall(r'{(.*?)}', uniqueIdFormat)
    dataKeys.extend(['region', 'accountid', 'partition'])
    absentKeys = []
    for key in uniqueIdKeys:
        if key.lower() not in dataKeys:
            absentKeys.append(key)

    return absentKeys


class AWSUniqueId:
    def get_unique_id(
        self, service: str, resourceType: str, data: Dict, accountId: str = None,
        region: str = None, partition: str = 'aws',
    ) -> str:

        uniqueIds: Dict = unique_ids
        data = {k.lower().replace("_", ""): v for k, v in data .items()}
        dataKeys = list(data.keys())

        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            raise ValueError(f"AWS service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(f"AWS service {service} resource type {resourceType} not supported")
            raise ValueError(f"AWS service {service} resource type {resourceType} not supported")

        elif 'accountId' in uniqueIds[service][resourceType] and not accountId:
            uniqueIdFormat = uniqueIds[service][resourceType].replace(" ", "").\
                replace('data["', "").replace('".lower()]', "")
            logger.error("AWS accountId required")
            raise ValueError(f"Invalid parameters provided, AWS accountId required, uniqu\
                eId format for resource {service} {resourceType} is {uniqueIdFormat}")

        elif 'region' in uniqueIds[service][resourceType] and not region:
            uniqueIdFormat = uniqueIds[service][resourceType].replace(" ", "").replace('data["', "").\
                replace('".lower()]', "")
            logger.error("AWS region required")
            raise ValueError(
                f"Invalid parameters provided, AWS region required, ,\
                    uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
            )

        else:
            uniqueIdFormat = uniqueIds[service][resourceType].replace(" ", "").\
                replace('data["', "").replace('".lower()]', "")
            absentKeys = check_absent_data_keys(dataKeys, uniqueIdFormat)
            if len(absentKeys) > 0:
                errorMsg = ''
                for key in absentKeys:
                    errorMsg += f" {key},"

                errorMsg = errorMsg[:-1]

                logger.error(f"AWS{errorMsg} keys required in data parameter")
                raise ValueError(
                    f"Invalid parameters provided, AWS{errorMsg} keys required in data parameter,\
                         uniqueId format for resource {service} {resourceType} is {uniqueIdFormat}",
                )

            else:
                return eval(f"f'{uniqueIds[service][resourceType]}'").replace(" ", "")

    def get_unique_id_format(self, service: str, resourceType: str) -> str:

        uniqueIds: Dict = unique_ids

        if not uniqueIds.get(service, None):
            logger.error(f"AWS service {service} unknown")
            raise ValueError(f"AWS service {service} unknown")

        elif not uniqueIds.get(service, {}).get(resourceType, None):
            logger.error(f"AWS service {service} resource type {resourceType} not supported")
            raise ValueError(f"AWS service {service} resource type {resourceType} not supported")

        else:
            return uniqueIds[service][resourceType].replace(" ", "").replace('data["', "").replace('".lower()]', "")
