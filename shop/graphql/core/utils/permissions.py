from graphql.type.definition import GraphQLResolveInfo

class UserPermissionError(PermissionError):
    def __init__(self, msg='You do not have permission to perform this action', *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


def check_permission(name, *args):
    for arg in args:
        if isinstance(arg, GraphQLResolveInfo):
            if not getattr(arg.context.user, name):
                raise UserPermissionError


def superuser_required(func):
    def check_su(*args, **kwargs):
        check_permission('is_superuser', *args)
        return func(*args, **kwargs)
    return check_su


def staff_member_required(func):
    def check_staff(*args, **kwargs):
        check_permission('is_staff', *args)
        return func(*args, **kwargs)
    return check_staff
