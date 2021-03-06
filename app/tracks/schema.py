import graphene
import json
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q  #allows to make more complex qeueries  

from .models import Track, Like
from users.schema import UserType


class TrackType(DjangoObjectType):
    class Meta:
        model = Track

class LikeType(DjangoObjectType):
    class Meta:
        model = Like

class PlayedType(DjangoObjectType):
    class Meta:
        model = Play

# user = graphene.ID(default_value=uuid.uuid4())
class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)
    played = graphene.List(PlayedType)

    def resolve_tracks(self, info, search=None):      # fallback value of search is none
        if search:
            filter = (
                Q(title__icontains=search) |
                Q(description__icontains=search) |
                Q(url__icontains=search) |
                Q(posted_by__username__icontains=search) #the __ is a way to burrow down into a object like . in JavaScript
            )
            return Track.objects.filter(filter)  #also is starts with exact(case sensitive exact match), iexact(case insensitive exact match), gt(greater than)

        return Track.objects.all()

    def resolve_likes(self, info):
        return Like.objects.all()

    def resolve_played(self, info):
        return Play.objects.all()


class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, title, description, url):
        # passing in **kwargs as paramater will give access to all 
        # kwargs.get('title')

        user = info.context.user 

        if user.is_anonymous:
            # raise GraphQLError('Log in to add a track') alternate method to handle errors
            raise Exception('Log in to add a track')

        track = Track(title=title, description=description, url=url, posted_by=user)
        track.save()    #adds to database
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        title = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception('Not permitted to update this track')

        track.title = title
        track.description = description 
        track.url = url

        track.save()
        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception('Not permitted to delete this track')

        track.delete()
        return DeleteTrack(track_id=track_id)


class CreateLike(graphene.Mutation): 
    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if user.is_anonymous:
            raise Exception('Log in to like a track')
    
        if not track:
            raise Exception('Cannot not find track with given track id')

        Like.objects.create(
        user=user,
        track=track
        )

        return CreateLike(user=user, track=track)


class CreatePlayed(graphene.Mutation): 
    # user = graphene.Field(UserType)
    track = graphene.Field(TrackType)
    # played = graphene.Field(PlayedType)

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        # user = info.context.user

        # if user.is_anonymous:
        #     raise Exception('Log in to play track')
    
        track = Track.objects.get(id=track_id)
        if not track:
            raise Exception('Cannot not find track with given track id')

        Play.objects.create(
        # user=user,
        track=track
        )

        return CreatePlayed(
            # user=user, 
            track=track
            )


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
    create_played = CreatePlayed.Field()

# this is how to create and query a new track

# mutation {
#   createTrack(title: "Track3", description: "Track3 Description", url: "http://urlTrack3.com") {
#     track {
#       id
#       title
#       description 
#       url
#       createdAt
#     }
#   }
# }

# mutation {
#   updateTrack(trackId: 4, title: "Track 5", description: "Track 5 Description", url: "http://track5.com") {
#     track {
#       id
#       title
#       url
#     }
#   }

# mutation {
#   deleteTrack(trackId: 6) {
#     trackId
#   }
# }

# mutation {
#   createLike(trackId: 1) {
#     track {
#       id
#       title
#     }
#     user {
#       username
#     }
#   }
# }

# {
#   tracks(search: "Track4"){
#     title
#   }
# }



# {
#   likes {
#     user {
#       username
#     }
#     track {
#       title
#     }
#   }
# }

# {
#   likes {
#     user {
#       likeSet {
#         id
#       }
#     }
#   }
# }