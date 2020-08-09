from django.contrib.auth import get_user_model
import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        # only_fields = ('id', 'email', 'password', 'username')   This would make it so the default fields such as SuperUser are not included

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int(required=True))
    me = graphene.Field(UserType)

    def resolve_user(self, info, id):
        return get_user_model().objects.get(id=id)

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not Logged in!')
        
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
    
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


# Using Insomnia put in the Header of the POST(needs to be post for get)  Authorization JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IkRvdWciLCJleHAiOjE1OTMyMjY2NzEsIm9yaWdJYXQiOjE1OTMyMjYzNzF9.D5ov7ew4zXXdCD-_9mIliIi40LQAnFjd2QQ1l_yxQ_0


# mutation {
#   createUser(username: "Doug5", password: "doug5", email: "doug5@yahoo.com") {
#     user {
#       id
#       password
#       username
#       email
#       dateJoined
#     }
#   }
# }

# {
#   user (id: 1) {
#       password
#     email
#     username
#     dateJoined

#   }
# }

#   mutation {
#     tokenAuth(username: "Doug", password: "doug") {
#       token
#     }
#   }

    

