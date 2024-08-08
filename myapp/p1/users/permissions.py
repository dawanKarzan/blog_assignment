from rest_framework import permissions

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class IsRoleCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.can_create == True
    
class IsRoleReader(permissions.BasePermission):
    # print('reader role is working')
    def has_permission(self, request, view):
        # print('reader role is working  = ', request.user)
        return request.user and request.user.is_authenticated and request.user.role.can_read == True
    
class IsRoleCanUpdate(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.can_update == True

class IsRoleCanDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role.can_delete == True
    
class IsUserAuthor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff == False
