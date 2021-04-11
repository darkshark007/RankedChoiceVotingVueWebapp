from djongo import models
from bson import ObjectId
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
    id = models.ObjectIdField(default=ObjectId)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500)


    def __getitem__(self, name):
       return getattr(self, name)


class User(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        User({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user_id': 'abcdefghijklmnopqrstuvwxyz'
        })
    '''
    id = models.ObjectIdField(default=ObjectId)
    user_id = models.CharField(max_length=40) # Don't have a real user model yet, this is a placeholder
    session_id = models.CharField(max_length=40)


    def __getitem__(self, name):
       return getattr(self, name)


class Ballot(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Ballot({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user':
        })
    '''
    id = models.ObjectIdField(default=ObjectId)
    user = models.EmbeddedField(model_container=User)


    def __getitem__(self, name):
       return getattr(self, name)


class Result(models.Model):
    id = models.ObjectIdField(default=ObjectId)
    rcv_result = models.CharField(max_length=40)


    def __getitem__(self, name):
       return getattr(self, name)


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

    # id = models.ObjectIdField(default=ObjectId)
    creator = models.EmbeddedField(model_container=User)
    created = models.DateTimeField(default=pendulum.now)
    updated = models.DateTimeField(default=pendulum.now)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    candidates = models.ArrayField(model_container=Candidate, default=[])
    ballots = models.ArrayField(model_container=Ballot, default=[])
    results = models.EmbeddedField(model_container=Result)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.results = Result()


    def __getitem__(self, name):
       return getattr(self, name)


    def update_from_poll_model(self, model):
        print('>>> update_from_poll_model invoked:')
        print(self)

        self.name = model.get('name', None)
        self.description = model.get('description', None)
        self.type = model.get('type', None)
        print('>>> LEN:')
        print(len(self.candidates))
        old_candidates_map = {cand.id: cand for cand in self.candidates}
        new_candidates = []
        for cand in model.get('candidates', []):
            if cand.get('id', None):
                cand_obj = old_candidates_map[cand.get('id')]
            else:
                cand_obj = Candidate()
            cand_obj.name = cand.get('name', None)
            cand_obj.description = cand.get('description', None)
            new_candidates.append(cand_obj)
        self.candidates = new_candidates
        self.updated = pendulum.now()
        print('>>> PRE-SAVE:')
        print(self)
        self.save()
