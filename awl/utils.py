# awl.utils.py

def refetch(obj):
    """Queries the database for the same object that is passed in, refetching
    its contents in case they are stale.

    :param obj:
        Object to refetch

    :returns:
        Refreshed version of the object
    """
    return obj.__class__.objects.get(id=obj.id)
