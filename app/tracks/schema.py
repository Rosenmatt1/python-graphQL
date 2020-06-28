import graphene
import json
from graphene_django import DjangoObjectType
from .models import Track

class TrackType(DjangoObjectType):
    class Meta:
        model = Track


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType)

    def resolve_tracks(self, info):
        return Track.objects.all()


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

    def mutate(self, info, track_id, title, description, url):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise Exception('Not permitted to delete this track')

        track.delete()

        return DeleteTrack(track_id=track_id)


class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()


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


# schema = graphene.Schema(query=Query, mutation=Mutation)
# #  auto_camelcase=False, pass as 2nd argument in query as the autocamelcase false allows the bellow is_admin to be written in snake case

# # ! means it is required

# result = schema.execute(
#     '''
#         query {
#         tracks {
#             id
            
#         }
#     }
#     '''
# )

# dictResult = dict(result.data.items())
# print(json.dumps(dictResult, indent=2))