from app.models import User
from app.models.user import RoleEnum


class UserService:
    @staticmethod
    def get_user_profile(username):
        """
        Retrieves the user profile for the given user ID.

        Parameters:
        - username (str): The username of the user.

        Returns:
        - dict: A dictionary containing user profile information.
        """
        user = User.query.get(username)
        if not user:
            raise ValueError("User not found")

        return {
            "username": user.username,
            "user_id": user.id,
            "role": user.role,
            "leading_teams": user.leading_teams,
        }

    @staticmethod
    def is_user_admin_or_higher(user_role):
        """
        Checks if the user has a role of admin or higher.

        Parameters:
        - user_role (str): The role of the user.

        Returns:
        - bool: True if the user is admin or higher, False otherwise.
        """
        return user_role.value >= RoleEnum.ADMIN.value
