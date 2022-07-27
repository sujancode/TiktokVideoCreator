import os
from os.path import exists


def cleanup(username) -> int:
    """Deletes all temporary assets in assets/temp

    Returns:
        int: How many files were deleted
    """
    if exists(f"assets/{username}/temp/"):
        os.system(f"rm -fr assets/{username}/")
    return 0
