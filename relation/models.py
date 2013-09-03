#!/usr/bin/env python
# coding=utf-8
'''
Created on 2013-6-26

@author: Tietang
'''
from functools import wraps
from hashlib import md5
from peewee import *
from datetime import *
# create a peewee database instance -- our models will use this database to
# persist information
database = MySQLDatabase("sp", host="127.0.0.1",port=4000, user="root")

# model definitions -- the standard "pattern" is to define a base model class
# that specifies which database to use.  then, any subclasses will automatically
# use the correct storage. for more information, see:
# http://charlesleifer.com/docs/peewee/peewee/models.html#model-api-smells-like-django
class BaseModel(Model):
    class Meta:
        database = database

# the user model specifies its fields (or columns) declaratively, like django
class User(BaseModel):
    username = CharField()
    password = CharField()
    email = CharField()
    join_date = DateTimeField()

    class Meta:
        order_by = ('username',)

    # it often makes sense to put convenience methods on model instances, for
    # example, "give me all the users this user is following":
    def following(self):
        # query other users through the "relationship" table
        return User.select().join(
            Relationship, on=Relationship.to_user,
        ).where(Relationship.from_user == self)

    def followers(self):
        return User.select().join(
            Relationship, on=Relationship.from_user,
        ).where(Relationship.to_user == self)

    def is_following(self, user):
        return Relationship.select().where(
            (Relationship.from_user == self) & 
            (Relationship.to_user == user)
        ).count() > 0

    def gravatar_url(self, size=80):
        return 'http://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
            (md5(self.email.strip().lower().encode('utf-8')).hexdigest(), size)


# this model contains two foreign keys to user -- it essentially allows us to
# model a "many-to-many" relationship between users.  by querying and joining
# on different columns we can expose who a user is "related to" and who is
# "related to" a given user
class Relationship(BaseModel):
    from_user = ForeignKeyField(User, related_name='relationships')
    to_user = ForeignKeyField(User, related_name='related_to')


# a dead simple one-to-many relationship: one user has 0..n messages, exposed by
# the foreign key.  because we didn't specify, a users messages will be accessible
# as a special attribute, User.message_set
class Message(BaseModel):
    user = ForeignKeyField(User)
    content = TextField()
    pub_date = DateTimeField()

    class Meta:
        order_by = ('-pub_date',)


# simple utility function to create tables
def create_tables():
    database.connect()
    User.create_table(True)
    Relationship.create_table(True)
    Message.create_table(True)
    
if __name__ == '__main__':
    create_tables()
    User(username="x1",password="sd",email="aa@33.com",join_date=datetime.now()).save()
 
