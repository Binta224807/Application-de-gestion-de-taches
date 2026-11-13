from rest_framework import permissions

from .models import UserRole


# ============================================================
# UTILITAIRES
# ============================================================


def get_user_profile(user):

    try:

        return user.profile

    except AttributeError:

        return None


def get_user_company(user):

    profile = get_user_profile(user)

    if profile:

        return profile.company

    return None


def is_ceo(user):

    profile = get_user_profile(user)

    return profile and profile.is_ceo


# ============================================================
# PERMISSIONS
# ============================================================


class IsCEOOrAdmin(permissions.BasePermission):

    """
    Autorise uniquement les PDG/administrateurs d'entreprise.
    """

    def has_permission(self, request, view):

        return (
            request.user
            and request.user.is_authenticated
            and is_ceo(request.user)
        )


class HasCompanyAccess(permissions.BasePermission):

    """
    Autorise uniquement les utilisateurs rattachés à une entreprise.
    """

    def has_permission(self, request, view):

        return (
            request.user
            and request.user.is_authenticated
            and get_user_company(request.user) is not None
        )


class IsCompanyMember(permissions.BasePermission):

    """
    Vérifie que l'objet appartient à la même entreprise que l'utilisateur.
    """

    def has_object_permission(self, request, view, obj):

        user_company = get_user_company(request.user)

        if not user_company:

            return False

        return getattr(obj, "company", None) == user_company


class IsTaskAccessible(permissions.BasePermission):

    """
    PDG : accès à toutes les tâches de son entreprise.
    Employé : accès uniquement aux tâches qui lui sont assignées.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:

            return False

        user_company = get_user_company(request.user)

        if not user_company or obj.company != user_company:

            return False

        if is_ceo(request.user):

            return True

        return obj.assigned_to == request.user


class IsCEOOrTaskAssignee(permissions.BasePermission):

    """
    Autorise le PDG ou l'employé assigné à modifier une tâche.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:

            return False

        user_company = get_user_company(request.user)

        if not user_company or obj.company != user_company:

            return False

        if is_ceo(request.user):

            return True

        return obj.assigned_to == request.user


class IsCompanyOwner(permissions.BasePermission):

    """
    Vérifie que l'utilisateur est le propriétaire (PDG) de l'entreprise.
    """

    def has_object_permission(self, request, view, obj):

        return (
            request.user
            and request.user.is_authenticated
            and getattr(obj, "owner", None) == request.user
        )
