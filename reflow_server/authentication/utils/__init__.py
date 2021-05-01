from uuid import UUID


def is_valid_uuid(uuid):
    """
    Check if a uuid is a valid UUID.

    Args:
        uuid (str): The uuid that you want to test

    Returns:
        bool: Returns True if `uuid` is a valid uuid, otherwise, returns False
    """
    try:
        uuid_obj = UUID(uuid, version=4)
    except ValueError:
        return False
    return str(uuid_obj) == uuid
