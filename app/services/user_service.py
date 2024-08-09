from app.models import User, Team
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
    def get_team_members(team_leader_id):
        """
        Retrieves the team members for the given team leader ID.

        Parameters:
        - team_leader_id (str): The ID of the team leader.

        Returns:
        - list: A list of user IDs who are members of the team.
        """
        team = Team.query.filter_by(leader_id=team_leader_id).first()
        if not team:
            raise ValueError("Team not found")
        return [
            member.id for member in team.members
        ]  # Assuming 'members' is a relationship in the Team model

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
