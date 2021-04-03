from djongo import models
# from bson import ObjectId
import pendulum
# from django.utils import timezone


# Create your models here.

class Candidate(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Candidate({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'name': "Bobby Fischer",
        })
    '''
    id = models.ObjectIdField()
    name = models.CharField(max_length=40)


class User(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        User({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user_id': 'abcdefghijklmnopqrstuvwxyz'
        })
    '''
    id = models.ObjectIdField()
    user_id = models.CharField(max_length=40) # Don't have a real user model yet, this is a placeholder
    session_id = models.CharField(max_length=40)


class Ballot(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Ballot({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user':
        })
    '''
    id = models.ObjectIdField()
    user = models.EmbeddedField(model_container=User)


class Result(models.Model):
    id = models.ObjectIdField()
    rcv_result = models.CharField(max_length=40)


class Poll(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Poll({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'creator': User({...}),
            'candidates': [
                Candidate({...}),
                Candidate({...}),
                Candidate({...}),
            ],
            'ballots': [
                Ballot({...}),
                Ballot({...}),
                Ballot({...}),
            ],
            'results': Result({...}),
        })
    '''

    TYPE_CLASSIC_RCV = 'classic_rcv'
    TYPE_FIRST_PAST_THE_POST = 'fptp'
    TYPE_CHOICES = (
        (TYPE_CLASSIC_RCV, 'Classic RCV'),
        (TYPE_FIRST_PAST_THE_POST, 'First Past The Post'),
    )

    id = models.ObjectIdField()
    creator = models.EmbeddedField(model_container=User)
    created = models.DateTimeField(default=pendulum.now)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    candidates = models.ArrayField(model_container=Candidate)
    ballots = models.ArrayField(model_container=Ballot)
    results = models.EmbeddedField(model_container=Result)
