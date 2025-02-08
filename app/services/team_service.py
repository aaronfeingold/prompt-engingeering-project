from app.models import Team


class TeamService:
    @staticmethod
    def get_leaders_teammates(team_leader_id, team_id=None):
        """
        Retrieves the team mates for the given team leader ID.

        Parameters:
        - team_leader_id (str): The ID of the team leader.

        Returns:
        - list: A list of usernames who are mates of the team.
        """
        team = Team.query.filter_by(leader_id=team_leader_id).first()
        if not team:
            raise ValueError("Team not found")
        return [mate.username for mate in team.teammates]

    @staticmethod
    def get_team_leaders(team_leader_id):
        """
        Retrieves the team leaders for the given team leader ID.

        Parameters:
        - team_leader_id (str): The ID of the team leader.

        Returns:
        - list: A list of usenames who are leaders of the team.
        """
        team = Team.query.filter_by(leader_id=team_leader_id).first()
        if not team:
            raise ValueError("Team not found")
        return [leader.username for leader in team.team_leaders]
