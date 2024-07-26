from typing import Dict

#class BitbucketUniqueId:
unique_id_patterns: Dict = {
    "bitbucket": {  # Bitbucket
        "workspace": 'bitbucket:{data["workspace"]}',
        "member": 'bitbucket:{data["workspace"]}:{data["member"]}',
        "project": 'bitbucket:{data["workspace"]}:{data["project"]}',
        "repository": 'bitbucket:{data["workspace"]}:{data["repository"]}',
    },
}
