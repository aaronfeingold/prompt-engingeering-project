from app.models import Team


class TeamService:
    @staticmethod
    def get_team_members(team_leader_id):
        """
        Retrieves the team members for the given team leader ID.

        Parameters:
        - team_leader_id (str): The ID of the team leader.

        Returns:
        - list: A list of usenames who are members of the team.
        """
        team = Team.query.filter_by(leader_id=team_leader_id).first()
        if not team:
            raise ValueError("Team not found")
        return [mate.username for mate in team.teammates]
