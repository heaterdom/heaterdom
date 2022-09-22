# IsSass error that extends Exception. This is to stop multiple injection messages
class IsSass(Exception):
    pass


# IsGlobal error that extends Exception. This is to stop multiple injection messages
class IsGlobal(Exception):
    pass