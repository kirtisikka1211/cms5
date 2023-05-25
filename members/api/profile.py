import graphene
from hashlib import md5
from ..models import Profile, SocialProfile, Portal, Group, Project
from graphql_jwt.decorators import login_required
from framework.api.APIException import APIException

from framework.platforms.gitlab import GitLab
from framework.platforms.github import GitHub
from framework.platforms.cloudflare import Cloudflare
from framework.platforms.telegram import Telegram
from django.db.models import F
from members.models import Language


class PortalObj(graphene.ObjectType):
    name = graphene.String()
    color = graphene.String()
    icon = graphene.String()


class SocialProfileObj(graphene.ObjectType):
    link = graphene.String()
    portal = graphene.Field(PortalObj)

    def resolve_portal(self, info):
        return Portal.objects.values().get(id=self['portal'])


class LanguageObj(graphene.ObjectType):
    name = graphene.String()

    def resolve_name(self, info):
        return self['name']


class ProfileObj(graphene.ObjectType):
    firstName = graphene.String()
    lastName = graphene.String()
    fullName = graphene.String()
    email = graphene.String()
    tagline = graphene.String()
    about = graphene.String()
    gravatar = graphene.String()
    links = graphene.List(SocialProfileObj)
    githubUsername = graphene.String()
    gitlabUsername = graphene.String()
    telegramUsername = graphene.String()
    twitterUsername = graphene.String()
    customEmail = graphene.String()
    displayInWebsite = graphene.Boolean()
    role = graphene.String()
    # fields that require login
    inGitLabGroup = graphene.Boolean()
    inGitHubGroup = graphene.Boolean()
    inCloudFlareGroup = graphene.Boolean()
    inTelegramGroup = graphene.Boolean()
    inCMSGroup = graphene.Boolean()
    profilePic = graphene.String()
    phone = graphene.String()
    birthDay = graphene.types.datetime.Date()
    telegramID = graphene.String()
    roll = graphene.String()
    batch = graphene.String()
    location = graphene.String()
    languages = graphene.List(LanguageObj)

    def resolve_firstName(self, info):
        return self['first_name']

    def resolve_lastName(self, info):
        return self['last_name']

    def resolve_fullName(self, info):
        if self['last_name'] is not None:
            return f"{self['first_name']} {self['last_name']}"
        else:
            return self['first_name']

    def resolve_gravatar(self, info):
        return "https://www.gravatar.com/avatar/" + md5(self['email'].lower().encode()).hexdigest()

    def resolve_links(self, info):
        return SocialProfile.objects.values('link', 'portal').filter(profile__id=self['id'])

    def resolve_githubUsername(self, info):
        return self['githubUsername']

    def resolve_gitlabUsername(self, info):
        return self['gitlabUsername']
    
    def resolve_telegramUsername(self, info):
        return self['telegramUsername']
    
    def resolve_twitterUsername(self, info):
        return self['twitterUsername']

    def resolve_customEmail(self, info):
        return self['customEmail']

    def resolve_profilePic(self, info):
        return self['profile_pic']

    def resolve_displayInWebsite(self, info):
        return self['displayInWebsite']

    def resolve_role(self, info):
        return self['role']

    @graphene.resolve_only_args
    def resolve_languages(self):
        return Profile.objects.values().annotate(
            name=F('languages__name'),
        ).filter(id=self['id'])

    @login_required
    def resolve_inGitLabGroup(self, info):
        if info.context.user.is_superuser:
            if self['gitlabUsername']:
                return GitLab(self['gitlabUsername']).checkIfUserExists()
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inGitHubGroup(self, info):
        if info.context.user.is_superuser:
            if self['githubUsername']:
                return GitHub(self['githubUsername']).checkIfUserExists()
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inCloudFlareGroup(self, info):
        if info.context.user.is_superuser:
            if self['email']:
                return Cloudflare(self['email']).checkIfUserExists()
            else:
                return False
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inTelegramGroup(self, info):
        if info.context.user.is_superuser:
            return Telegram(self['telegram_id']).checkIfUserExists()
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    @login_required
    def resolve_inCMSGroup(self, info):
        if info.context.user.is_superuser:
            return Group.objects.values().filter(members__id=self['user_id'])
        else:
            raise APIException('Only Superusers have access',
                               code='ONLY_SUPERUSER_HAS_ACCESS')

    def resolve_birthDay(self, info):
        return self['birthday']

    def resolve_location(self, info):
        return  self['location']

    @login_required
    def resolve_phone(self, info):
        return self['phone']

    @login_required
    def resolve_telegramID(self, info):
        return self['telegram_id']

    @login_required
    def resolve_roll(self, info):
        return self['roll_number']

    def resolve_batch(self, info):
        return self['batch']


class AvatarObj(graphene.ObjectType):
    githubUsername = graphene.String()

    def resolve_githubUsername(self, info):
        return self['githubUsername']


class Query(object):
    profile = graphene.Field(
        ProfileObj,
        username=graphene.String(required=True)
    )
    profiles = graphene.List(ProfileObj)
    getAvatar = graphene.Field(AvatarObj, username=graphene.String(required=True))

    def resolve_profile(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return Profile.objects.values().get(user__username=username)
        raise Exception('Username is a required parameter')

    def resolve_profiles(self, info, **kwargs):
        return Profile.objects.values().all()

    def resolve_languages(self, info):
        return Language.objects.values().all()

    def resolve_getAvatar(self, info, **kwargs):
        username = kwargs.get('username')
        if username is not None:
            return Profile.objects.values().get(user__username=username)
        raise Exception('Username is a required parameter')
