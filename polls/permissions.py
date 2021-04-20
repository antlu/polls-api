from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class PostOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == 'POST'
