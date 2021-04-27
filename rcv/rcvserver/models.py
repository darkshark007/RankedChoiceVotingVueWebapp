from djongo import models
from bson import ObjectId
import pendulum
# from django.utils import timezone


TYPE_CLASSIC_RCV = 'classic_rcv'
TYPE_FIRST_PAST_THE_POST = 'fptp'
TYPE_CHOICES = (
    (TYPE_CLASSIC_RCV, 'Classic RCV'),
    (TYPE_FIRST_PAST_THE_POST, 'Single-Choice Popular Vote'),
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
        print('>>> get_js_choice_model:')
        print(self.__dict__)
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
    context = models.DictField(default={})


    def __getitem__(self, name):
       return getattr(self, name, None)


    def get_js_ballot_model(self):
        obj = {
            'id': str(self.id),
            'name': self.name,
            'context': self.context,
        }
        return obj



class Result(models.Model):
    id = models.CharField(max_length=24, default=ObjectId, primary_key=True)
    fptp_result = models.DictField(default={})
    rcv_result = models.DictField(default={})


    def __getitem__(self, name):
       return getattr(self, name, None)


    def get_js_result_model(self):
        obj = {
        }
        return obj

    
    def update_fptp_result_from_ballot(self, ballot, mult):

        def get_fptp_data():
            if TYPE_FIRST_PAST_THE_POST in ballot.context:
                if 'selected' in ballot.context[TYPE_FIRST_PAST_THE_POST]:
                    return ballot.context[TYPE_FIRST_PAST_THE_POST]['selected']
            return None

        def get_rcv_data():
            pass

        # Find the most relevant ballot data
        data = None
        if not data:
            data = get_fptp_data()
        if not data:
            data = get_rcv_data()
        if not data:
            raise Exception('Could not find relevant Ballot data')

        # Update Result data
        if data not in self.fptp_result:
            self.fptp_result[data] = 0
        self.fptp_result[data] += (1 * mult)

        # Update Result statistics

        print('>>> RESULTS: ')
        print(self.fptp_result)



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
        self.save()


    def get_js_poll_model(self, user):
        obj = {
            'id': str(self.id),
            'created': self.created,
            'updated': self.updated,
            'name': self.name,
            'description': self.description,
            'type': self.type,
            'choices': list(map(lambda cand: cand.get_js_choice_model(), self.choices)),
            'results': self.results.get_js_result_model(),
        }
        print('>>> IDS??? {} == {}'.format(user.id, self.creator.id))
        if user.id == self.creator.id:
            obj['canEdit'] = True
        return obj


    def update_ballot_from_js(self, model, user):
        new_ballot = False
        if model['ballot']['id']:
            ballot_id = model['ballot']['id']
            for ballot in self.ballots:
                if ballot.id == ballot_id:
                    current_ballot = ballot
                    break
            if not current_ballot:
                response = HttpResponse("Ballot with that ID does not exist!")
                response.status_code = 403
                return response
        else:
            current_ballot = Ballot()
            new_ballot = True
            self.ballots.append(current_ballot)
            current_ballot.user = user

        current_ballot.name = model['ballot']['name']

        if not new_ballot:
            # TODO: Update Results/statistics data
            self.results.update_fptp_result_from_ballot(current_ballot, -1)

        current_ballot.context = model['ballot']['context']

        # TODO: Update Results/statistics data
        self.results.update_fptp_result_from_ballot(current_ballot, 1)

        self.save()
        return current_ballot.get_js_ballot_model()
