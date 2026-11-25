from rest_framework import permissions

from .models import UserRole, Company


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


def is_company_member(user, company):

    if not company:

        return False

    profile = get_user_profile(user)

    return (
        company.owner_id == user.id
        or (
            profile
            and profile.company_id == company.id
        )
    )


def is_org_admin(user, company):

    """
    Administrateur d'une organisation : propriétaire,
    membre marqué admin, ou rôle hérité 'ceo'.
    """

    if not is_company_member(user, company):

        return False

    profile = get_user_profile(user)

    return (
        company.owner_id == user.id
        or (
            profile
            and (
                profile.is_admin
                or profile.role == UserRole.CEO
            )
        )
    )


def is_ceo(user):

    """
    Compatibilité : admin de l'entreprise rattachée au profil.
    """

    company = get_user_company(user)

    return company and is_org_admin(user, company)


PERSONAL = "personal"
FORBIDDEN = "forbidden"


def resolve_space(request):

    """
    Détermine l'espace actif de la requête.

    Retourne (company, ok) :
      - ("personal")  -> (None, True)   espace personnel
      - id entreprise -> (Company, True) si membre
      - sinon         -> (None, False)  accès refusé
      - absent        -> legacy : entreprise du profil,
                         ou personnel si aucune
    """

    space = request.query_params.get("space")

    if space == PERSONAL:

        return None, True

    if space:

        try:

            company = Company.objects.get(pk=int(space))

        except (ValueError, Company.DoesNotExist):

            return None, False

        if is_company_member(request.user, company):

            return company, True

        return None, False

    company = get_user_company(request.user)

    return company, True


def task_is_accessible(task, user):

    """
    Tâche personnelle : propriétaire ou assigné.
    Tâche d'organisation : membre, admin ou assigné.
    """

    if task.company_id is None:

        return (
            task.user_id == user.id
            or task.assigned_to.filter(
                pk=user.pk
            ).exists()
        )

    if is_org_admin(user, task.company):

        return True

    return task.assigned_to.filter(
        pk=user.pk
    ).exists()


# ============================================================
# PERMISSIONS
# ============================================================


class IsCEOOrAdmin(permissions.BasePermission):

    """
    Admin de l'organisation active (espace demandé ou profil).
    Conservé pour compatibilité.
    """

    def has_permission(self, request, view):

        if not (
            request.user
            and request.user.is_authenticated
        ):

            return False

        company, ok = resolve_space(request)

        if not ok:

            return False

        if company is None:

            return True

        return is_org_admin(request.user, company)


class HasCompanyAccess(permissions.BasePermission):

    """
    Vérifie que l'espace demandé est accessible
    (personnel ou organisation dont on est membre).
    """

    def has_permission(self, request, view):

        if not (
            request.user
            and request.user.is_authenticated
        ):

            return False

        _, ok = resolve_space(request)

        return ok


class IsCompanyMember(permissions.BasePermission):

    """
    L'objet appartient à l'espace actif de l'utilisateur
    (personnel : user == request.user, organisation : membre).
    """

    def has_object_permission(self, request, view, obj):

        company, ok = resolve_space(request)

        if not ok:

            return False

        obj_company = getattr(obj, "company", None)

        if obj_company is None:

            return getattr(obj, "user", None) == request.user

        return obj_company == company


class IsTaskAccessible(permissions.BasePermission):

    """
    Admin : toutes les tâches de l'organisation.
    Membre : tâches assignées.
    Personnel : ses propres tâches.
    """

    def has_object_permission(self, request, view, obj):

        if not (
            request.user
            and request.user.is_authenticated
        ):

            return False

        return task_is_accessible(obj, request.user)


class IsCEOOrTaskAssignee(permissions.BasePermission):

    """
    Admin de l'organisation ou assigné à la tâche.
    Personnel : propriétaire de la tâche.
    """

    def has_object_permission(self, request, view, obj):

        if not (
            request.user
            and request.user.is_authenticated
        ):

            return False

        return task_is_accessible(obj, request.user)


class IsCompanyOwner(permissions.BasePermission):

    """
    Propriétaire ou admin de l'entreprise.
    """

    def has_object_permission(self, request, view, obj):

        if not (
            request.user
            and request.user.is_authenticated
        ):

            return False

        if getattr(obj, "owner", None) == request.user:

            return True

        return is_org_admin(request.user, obj)
