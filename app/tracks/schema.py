import graphene
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
        track = Track(title=title, description=description, url=url)
        track.save()    #adds to database
        return CreateTrack(track=track)

class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()


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