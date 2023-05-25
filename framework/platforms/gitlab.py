import gitlab
from framework.platforms.userPlatform import UserPlatform
from utilities.models import Token


class GitLab(UserPlatform):

    def __init__(self, username):
        self.username = username

    def removeUser(self):
        GITLAB_TOKEN = Token.objects.values().get(key='GITLAB_TOKEN')['value']
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        group.members.delete(userID)

    def addUser(self):
        GITLAB_TOKEN = Token.objects.values().get(key='GITLAB_TOKEN')['value']
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        try:
            group.members.create({'user_id': userID, 'access_level': gitlab.REPORTER_ACCESS})
        except:
            pass
        projectIDs = [20528933, 21712951]
        for projectID in projectIDs:
            project = gl.projects.get(projectID)
            try:
                project.members.create({'user_id': userID, 'access_level': gitlab.DEVELOPER_ACCESS})
            except:
                pass

    def checkIfUserExists(self):
        GITLAB_TOKEN = Token.objects.values().get(key='GITLAB_TOKEN')['value']
        gl = gitlab.Gitlab('https://gitlab.com/', GITLAB_TOKEN)
        gl.auth()
        group = gl.groups.get('amfoss')
        userID = gl.users.list(username=self.username)[0].id
        try:
            member = group.members.get(userID)
            if member:
                return True
            else:
                return False
        except:
            return False
