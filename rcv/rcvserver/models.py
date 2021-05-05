from djongo import models
from bson import ObjectId
import pendulum
from django.http import HttpResponse


TYPE_CLASSIC_RCV = 'classic_rcv'
TYPE_FIRST_PAST_THE_POST = 'fptp'
TYPE_SCORE_THEN_AUTOMATIC_RUNOFF = 'star_vote'
TYPE_APPROVAL = 'approval'
TYPE_RANKED_CUMULATIVE_APPROVAL = 'ranked_cumulative_approval'
TYPE_RANKED_SCORED_TIER = 'ranked_score_tier'
TYPE_RANKED_SCORED_SPLIT = 'ranked_score_split'
TYPE_RANKED_GRAPH_MAXIMAL = 'ranked_graph_maximal'
TYPE_CHOICES = (
    (TYPE_CLASSIC_RCV, 'Classic RCV'),
    (TYPE_FIRST_PAST_THE_POST, 'Single-Choice Popular Vote'),
    (TYPE_RANKED_CUMULATIVE_APPROVAL, 'Ranked Cumulative Approval'),
    # (TYPE_SCORE_THEN_AUTOMATIC_RUNOFF, 'STAR Vote'),
    # (TYPE_APPROVAL, 'APPROVAL'),
    # (TYPE_RANKED_SCORED_TIER, 'Ranked Tiered-Score Vote'),
    # (TYPE_RANKED_SCORED_SPLIT, 'Ranked Split-Score Vote'),
    # (TYPE_RANKED_GRAPH_MAXIMAL, 'Ranked Graph Maximum Approval'),
)

# Create your models here.

class Choice(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Choice({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'name': "Bobby Fischer",
        })
    '''
    id = models.CharField(max_length=24, default=ObjectId, primary_key=True)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500)


    def __getitem__(self, name):
       return getattr(self, name, None)


    def get_js_choice_model(self):
        obj = {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
        }
        return obj

class User(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        User({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user_id': 'abcdefghijklmnopqrstuvwxyz'
        })
    '''
    id = models.CharField(max_length=24, default=ObjectId, primary_key=True)
    # id = models.ObjectIdField(default=ObjectId)
    user_id = models.CharField(max_length=40) # Don't have a real user model yet, this is a placeholder
    session_id = models.CharField(max_length=40)


    def __getitem__(self, name):
       return getattr(self, name, None)


    @staticmethod
    def get_user_from_request(request):
        if not request.session.session_key:
            request.session.create()
        session_id = request.session.session_key
        try:
            user = User.objects.get(session_id=session_id)
        except User.DoesNotExist:
            user = User(**{
                'session_id': session_id,
            })
            user.save()

        return user



class Ballot(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Ballot({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'user':
        })
    '''
    id = models.CharField(max_length=24, default=ObjectId, primary_key=True)
    user = models.EmbeddedField(model_container=User)
    name = models.CharField(max_length=40)
    public = models.BooleanField(default=False)
    context = models.DictField(default={})


    def __getitem__(self, name):
       return getattr(self, name, None)


    def get_js_ballot_model(self):
        obj = {
            'id': str(self.id),
            'name': self.name,
            'publicBallot': self.public,
            'context': self.context,
        }
        return obj



class Result(models.Model):
    id = models.CharField(max_length=24, default=ObjectId, primary_key=True)
    fptp_result = models.DictField(default={})
    rcv_result = models.DictField(default={})
    rca_result = models.DictField(default={})


    def __getitem__(self, name):
       return getattr(self, name, None)


    def get_js_result_model(self, user):
        obj = {
            TYPE_FIRST_PAST_THE_POST: self.fptp_result,
            TYPE_CLASSIC_RCV: self.rcv_result,
            TYPE_RANKED_CUMULATIVE_APPROVAL: self.rca_result,
        }
        return obj

    
    def update_fptp_result_from_ballot(self, ballot, mult):
        data = ballot.context[TYPE_FIRST_PAST_THE_POST].get('selected', None)
        if not data:
            return
        if data not in self.fptp_result:
            self.fptp_result[data] = 0
        self.fptp_result[data] += (1 * mult)

        # TODO: Update Result statistics

        print(self.fptp_result)


    def update_rcv_result_from_ballot(self, ballot, mult):
        data = ballot.context[TYPE_CLASSIC_RCV]['selected']
        current = self.rcv_result
        for choice in data:
            if choice not in current:
                current[choice] = {'count': 0}
            
            current[choice]['count'] += (1 * mult)
            current = current[choice]

        # TODO: Update Result statistics

        print('>>> RCV RESULTS: ')
        print(self.rcv_result)


    def update_rca_result_from_ballot(self, ballot, mult):
        data = ballot.context[TYPE_RANKED_CUMULATIVE_APPROVAL]['selected']
        current = self.rca_result
        for choice in data:
            if choice not in current:
                current[choice] = {'count': 0}
            
            current[choice]['count'] += (1 * mult)
            current = current[choice]

        # TODO: Update Result statistics

        print('>>> RCA RESULTS: ')
        print(self.rca_result)



class Poll(models.Model):
    '''
    (OUTDATED)
    Sample Data Structure:
        Poll({
            'id': ObjectId('606115f19696a4dc0e8f3f57'),
            'creator': User({...}),
            'choices': [
                Choice({...}),
                Choice({...}),
                Choice({...}),
            ],
            'ballots': [
                Ballot({...}),
                Ballot({...}),
                Ballot({...}),
            ],
            'results': Result({...}),
        })
    '''

    id = models.ObjectIdField(default=ObjectId)
    creator = models.EmbeddedField(model_container=User, default=User)
    created = models.DateTimeField(default=pendulum.now)
    updated = models.DateTimeField(default=pendulum.now)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    public = models.BooleanField(default=False)
    public_ballots = models.CharField(max_length=5, choices=[('yes','yes'), ('no','no'), ('maybe','maybe')])
    multi_ballots_per_user = models.BooleanField(default=True)
    choices = models.ArrayField(model_container=Choice, default=[])
    ballots = models.ArrayField(model_container=Ballot, default=[])
    # ballots = models.DictField(default={})
    results = models.EmbeddedField(model_container=Result, default=Result)


    def __getitem__(self, name):
       return getattr(self, name, None)


    def update_from_js_poll_model(self, model):
        self.name = model.get('name', None)
        self.description = model.get('description', None)
        self.type = model.get('type', None)
        old_choices_map = {str(cand.id): cand for cand in self.choices}
        new_choices = []
        for cand in model.get('choices', []):
            if cand.get('id', None):
                cand_obj = old_choices_map[cand.get('id')]
            else:
                cand_obj = Choice()
            cand_obj.name = cand.get('name', None)
            cand_obj.description = cand.get('description', None)
            new_choices.append(cand_obj)
        self.choices = new_choices
        self.updated = pendulum.now()
        self.public = model.get('publicPoll', None)
        self.public_ballots = model.get('publicBallots', None)
        self.multi_ballots_per_user = model.get('multiBallotsPerUser', None)
        self.save()


    def get_js_poll_model(self, user):
        obj = {
            'id': str(self.id),
            'created': self.created,
            'updated': self.updated,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'publicPoll': self.public,
            'publicBallots': self.public_ballots,
            'multiBallotsPerUser': self.multi_ballots_per_user,
            'choices': list(map(lambda cand: cand.get_js_choice_model(), self.choices)),
        }
        if user.id == self.creator.id:
            obj['canEdit'] = True
        return obj


    def get_js_result_model(self, user):
        data = self.results.get_js_result_model(user)
        data['count'] = len(self.ballots)
        return data


    def update_ballot_from_js(self, model, user):
        new_ballot = False
        if model['ballot']['id']:
            ballot_id = model['ballot']['id']
            current_ballot = None
            for ballot in self.ballots:
                if ballot.id == ballot_id:
                    current_ballot = ballot
                    break
            if not current_ballot:
                response = HttpResponse("Ballot with that ID does not exist!")
                response.status_code = 403
                return response
        else:
            if self.multi_ballots_per_user == False:
                for ballot in self.ballots:
                    if ballot.user.id == user.id:
                        response = HttpResponse("User can not create another Ballot for this Poll!")
                        response.status_code = 403
                        return response
            current_ballot = Ballot()
            new_ballot = True
            self.ballots.append(current_ballot)
            current_ballot.user = user

        if not new_ballot:
            # TODO: Update Results/statistics data
            self.results.update_fptp_result_from_ballot(current_ballot, -1)
            self.results.update_rcv_result_from_ballot(current_ballot, -1)
            self.results.update_rca_result_from_ballot(current_ballot, -1)

        current_ballot.name = model['ballot']['name']
        current_ballot.context = model['ballot']['context']
        current_ballot.public = model['ballot']['publicBallot']

        # TODO: Update Results/statistics data
        self.results.update_fptp_result_from_ballot(current_ballot, 1)
        self.results.update_rcv_result_from_ballot(current_ballot, 1)
        self.results.update_rca_result_from_ballot(current_ballot, 1)

        self.save()
        return current_ballot.get_js_ballot_model()
