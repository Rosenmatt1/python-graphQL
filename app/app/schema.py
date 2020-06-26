import graphene
import tracks.schema
import users.schema

class Query(tracks.schema.Query, graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation, tracks.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)


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


