from rest_framework import permissions

class IsCustomerPermission(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        user = request.user
        if user.has_perm("api_tasks.add_task"):
            return True
        if user.has_perm("api_tasks.delete_task"):
            return True
        if user.has_perm("api_tasks.change_task"):
            return True
        if user.has_perm("api_tasks.view_task"):
            return True
        return False