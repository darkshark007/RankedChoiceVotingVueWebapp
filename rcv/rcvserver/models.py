from djongo import models
from bson import ObjectId
import pendulum
from django.http import HttpResponse


TYPE_CLASSIC_RCV = 'classic_rcv'
TYPE_COOMBS_RCV = 'coombs_rcv'
TYPE_FIRST_PAST_THE_POST = 'fptp'
TYPE_SCORE_THEN_AUTOMATIC_RUNOFF = 'star_vote'
TYPE_APPROVAL = 'approval'
TYPE_RANKED_CUMULATIVE_APPROVAL = 'ranked_cumulative_approval'
TYPE_RANKED_SCORED_TIER = 'ranked_score_tier'
TYPE_RANKED_SCORED_SPLIT = 'ranked_score_split'
TYPE_RANKED_GRAPH_MAXIMAL = 'ranked_graph_maximal'
TYPE_CHOICES = (
    (TYPE_CLASSIC_RCV, 'Classic RCV / IRV'),
    # (TYPE_COOMBS_RCV, 'Reverse-Elimination RCV'),
    (TYPE_FIRST_PAST_THE_POST, 'Single-Choice Popular Vote'),
    (TYPE_RANKED_CUMULATIVE_APPROVAL, 'Ranked Cumulative Approval (Bucklin)'),
    (TYPE_SCORE_THEN_AUTOMATIC_RUNOFF, 'Score Then Automatic Runoff (STAR)'),
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
    star_result = models.DictField(default={})


    def __getitem__(self, name):
       return getattr(self, name, None)


    def update_stats_from_stats_list(self, stats, results, mult):
        for category_key in stats:
            for stat_key in stats[category_key]:
                results['stats'][category_key][stat_key] += (1 * mult)
                results['stats'][category_key]['total'] += (1 * mult)


    def expand_stats_from_stats_list(self, stats, results):
        data = results['stats']
        expanded_stats = {}
        for category_key in stats:
            expanded_stats[category_key] = {}
            expanded_stats[category_key]['total'] = data[category_key]['total']
            for stat_key in stats[category_key]:
                expanded_stats[category_key][stat_key] = data[category_key][stat_key]
        return expanded_stats

    def get_js_result_model(self, user):
        obj = {
            TYPE_FIRST_PAST_THE_POST: self.fptp_result,
            TYPE_CLASSIC_RCV: self.rcv_result,
            TYPE_RANKED_CUMULATIVE_APPROVAL: self.rca_result,
            TYPE_SCORE_THEN_AUTOMATIC_RUNOFF: self.star_result,
        }
        return obj

    
    def update_fptp_result_from_ballot(self, ballot, mult):
        if TYPE_FIRST_PAST_THE_POST not in ballot.context:
            return
        data = ballot.context[TYPE_FIRST_PAST_THE_POST].get('selected', None)
        if not data:
            return
        if data not in self.fptp_result:
            self.fptp_result[data] = 0
        self.fptp_result[data] += (1 * mult)

        # TODO: Update Result statistics


    def update_rcv_result_from_ballot(self, ballot, mult):
        if TYPE_CLASSIC_RCV not in ballot.context:
            return
        data = ballot.context[TYPE_CLASSIC_RCV]['selected']
        current = self.rcv_result
        for choice in data:
            if choice not in current:
                current[choice] = {'count': 0}
            
            current[choice]['count'] += (1 * mult)
            current = current[choice]
        self.update_stats_from_stats_list(self.get_rcv_statistics_from_ballot(ballot), self.rcv_result, mult)


    def get_rcv_statistics_from_ballot(self, ballot):
        return self.get_strict_preference_stats_from_ballot(ballot.context[TYPE_CLASSIC_RCV]['selected'])


    def update_rca_result_from_ballot(self, ballot, mult):
        if TYPE_RANKED_CUMULATIVE_APPROVAL not in ballot.context:
            return
        data = ballot.context[TYPE_RANKED_CUMULATIVE_APPROVAL]['selected']
        current = self.rca_result
        for choice in data:
            if choice not in current:
                current[choice] = {'count': 0}
            
            current[choice]['count'] += (1 * mult)
            current = current[choice]
        self.update_stats_from_stats_list(self.get_rca_statistics_from_ballot(ballot), self.rca_result, mult)


    def get_rca_statistics_from_ballot(self, ballot):
        return self.get_strict_preference_stats_from_ballot(ballot.context[TYPE_RANKED_CUMULATIVE_APPROVAL]['selected'])


    def get_strict_preference_stats_from_ballot(self, data, base_stats=None):
        if not base_stats:
            base_stats = {}
        stats = {
            **base_stats,
            'included': {},
            'picks': {},
            'top_n_picks': {},
            'preferences': {},
        }
        for choice_idx1 in range(0, len(data)):
            included_key = '{}'.format(data[choice_idx1])
            stats['included'][included_key] = 1
            pick_key = '{}-{}'.format(choice_idx1, data[choice_idx1])
            stats['picks'][pick_key] = 1
            for choice_idx2 in range(choice_idx1+1, len(data)):
                pref_key = '{}>{}'.format(data[choice_idx1], data[choice_idx2])
                stats['preferences'][pref_key] = 1
            # TODO: This doesn't include all of the Top-N preference stats IF the ballot doesn't rank all candidates.  (Add CurrentChoices field to Ballot?)
            for choice_idx2 in range(0, choice_idx1+1):
                top_n_key = '{}-{}'.format(choice_idx1, data[choice_idx2])
                stats['top_n_picks'][top_n_key] = 1
        return stats


    def update_star_result_from_ballot(self, ballot, mult):
        # TODO: How can this be done in a data-positive way?  If new Choices are added, this may break calculation.  (Add CurrentChoices field to Ballot?)
        if TYPE_SCORE_THEN_AUTOMATIC_RUNOFF not in ballot.context:
            return
        data = ballot.context[TYPE_SCORE_THEN_AUTOMATIC_RUNOFF]['selected']
        res = self.star_result
        for idx1 in range(0,len(data)):
            choice = data[idx1]
            if choice['id'] not in res:
                res[choice['id']] = {'score': 0}
            res[choice['id']]['score'] += (mult*choice['score'])
            score_key = 'score-{}'.format(choice['score'])
            if score_key not in res[choice['id']]:
                res[choice['id']][score_key] = 0
            res[choice['id']][score_key] += (mult*1)
            for idx2 in range(idx1+1,len(data)):
                choice2 = data[idx2]
                if choice2['id'] not in res:
                    res[choice2['id']] = {'score': 0}
                compare_key1 = None
                compare_key2 = None
                if choice['score'] > choice2['score']:
                    compare_key1 = ">{}".format(choice2['id'])
                    compare_key2 = "<{}".format(choice['id'])
                elif choice['score'] < choice2['score']:
                    compare_key1 = "<{}".format(choice2['id'])
                    compare_key2 = ">{}".format(choice['id'])
                else:
                    compare_key1 = "={}".format(choice2['id'])
                    compare_key2 = "={}".format(choice['id'])
                if compare_key1 not in res[choice['id']]:
                    res[choice['id']][compare_key1] = 0
                if compare_key2 not in res[choice2['id']]:
                    res[choice2['id']][compare_key2] = 0
                res[choice['id']][compare_key1] += (mult*1)
                res[choice2['id']][compare_key2] += (mult*1)
        self.update_stats_from_stats_list(self.get_star_statistics_from_ballot(ballot), self.star_result, mult)


    def get_star_statistics_from_ballot(self, ballot):
        stats = {
            'included': {},
            'score_picks': {},
            'preferences': {},
        }
        data = [*ballot.context[TYPE_SCORE_THEN_AUTOMATIC_RUNOFF]['selected']]
        data.sort(key=lambda d: d['score'], reverse=True)
        for choice_idx1 in range(0, len(data)):
            included_key = '{}'.format(data[choice_idx1]['id'])
            stats['included'][included_key] = 1
            score_pick_key = '{}-{}'.format(data[choice_idx1]['score'], data[choice_idx1]['id'])
            stats['score_picks'][score_pick_key] = 1
            for choice_idx2 in range(choice_idx1+1, len(data)):
                if data[choice_idx1]['score'] == data[choice_idx2]['score']:
                    pref_key = '{}={}'.format(data[choice_idx2]['id'], data[choice_idx1]['id'])
                    if data[choice_idx1]['id'] > data[choice_idx2]['id']:
                        pref_key = '{}={}'.format(data[choice_idx1]['id'], data[choice_idx2]['id'])
                    stats['preferences'][pref_key] = 1
                else:
                    pref_key = '{}>{}'.format(data[choice_idx1]['id'], data[choice_idx2]['id'])
                    stats['preferences'][pref_key] = 1
        return stats


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
    locked = models.BooleanField(default=False)
    randomize_choices = models.BooleanField(default=True)

    choices = models.ArrayField(model_container=Choice, default=[])
    ballots = models.ArrayField(model_container=Ballot, default=[])
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
        self.randomize_choices = model.get('randomizeChoices', None)
        self.multi_ballots_per_user = model.get('multiBallotsPerUser', None)
        self.locked = model.get('locked', None)
        self.init_stats()
        self.save()


    def init_stats(self):
        def init_strict_preference_stats(result):
            if 'stats' not in result:
                result['stats'] = {
                    'included': {'total': 0},
                    'picks': {'total': 0},
                    'top_n_picks': {'total': 0},
                    'preferences': {'total': 0},
                }
            stats = result['stats']
            for idx, choice in enumerate(self.choices):
                included_key = '{}'.format(choice.id)
                if included_key not in stats['included']:
                    stats['included'][included_key] = 0
                for idx2, choice2 in enumerate(self.choices):
                    pick_key = '{}-{}'.format(idx, choice2.id)
                    if pick_key not in stats['picks']:
                        stats['picks'][pick_key] = 0
                    if choice.id != choice2.id:
                        pref_key = '{}>{}'.format(choice.id, choice2.id)
                        if pref_key not in stats['preferences']:
                            stats['preferences'][pref_key] = 0
                    top_n_key = '{}-{}'.format(idx2, choice.id)
                    if top_n_key not in stats['top_n_picks']:
                        stats['top_n_picks'][top_n_key] = 0

        # Classic RCV
        init_strict_preference_stats(self.results.rcv_result)

        # Ranked Cumulative Approval (Bucklin)
        init_strict_preference_stats(self.results.rca_result)

        # STAR
        result = self.results.star_result
        if 'stats' not in result:
            result['stats'] = {
                'included': {'total': 0},
                'score_picks': {'total': 0},
                'preferences': {'total': 0},
            }
        stats = result['stats']
        for idx, choice in enumerate(self.choices):
            included_key = '{}'.format(choice.id)
            if included_key not in stats['included']:
                stats['included'][included_key] = 0
            for idx2, choice2 in enumerate(self.choices):
                if choice.id != choice2.id:
                    pref_key = '{}>{}'.format(choice.id, choice2.id)
                    if pref_key not in stats['preferences']:
                        stats['preferences'][pref_key] = 0
                    if str(choice.id) > str(choice2.id):
                        pref_key2 = '{}={}'.format(choice.id, choice2.id)
                        if pref_key2 not in stats['preferences']:
                            stats['preferences'][pref_key2] = 0
            for score in range(0,6):
                score_pick_key = '{}-{}'.format(score, choice.id)
                if score_pick_key not in stats['score_picks']:
                    stats['score_picks'][score_pick_key] = 0


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
            'randomizeChoices': self.randomize_choices,
            'locked': self.locked,
            'choices': list(map(lambda cand: cand.get_js_choice_model(), self.choices)),
        }
        if user.id == self.creator.id:
            obj['canEdit'] = True
        return obj


    def get_js_result_model(self, user):
        data = self.results.get_js_result_model(user)
        data['count'] = len(self.ballots)
        return data


    def get_stats_for_ballot(self, ballot):
        return {
            'ballotCount': len(self.ballots),
            TYPE_CLASSIC_RCV: self.results.expand_stats_from_stats_list(
                self.results.get_rcv_statistics_from_ballot(ballot),
                self.results.rcv_result),
            TYPE_FIRST_PAST_THE_POST: None, # TODO: Add Stats
            TYPE_RANKED_CUMULATIVE_APPROVAL: self.results.expand_stats_from_stats_list(
                self.results.get_rca_statistics_from_ballot(ballot),
                self.results.rca_result),
            TYPE_SCORE_THEN_AUTOMATIC_RUNOFF: self.results.expand_stats_from_stats_list(
                self.results.get_star_statistics_from_ballot(ballot),
                self.results.star_result),
        }


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
            self.results.update_star_result_from_ballot(current_ballot, -1)

        current_ballot.name = model['ballot']['name']
        current_ballot.context = model['ballot']['context']
        current_ballot.public = model['ballot']['publicBallot']

        # TODO: Update Results/statistics data
        self.results.update_fptp_result_from_ballot(current_ballot, 1)
        self.results.update_rcv_result_from_ballot(current_ballot, 1)
        self.results.update_rca_result_from_ballot(current_ballot, 1)
        self.results.update_star_result_from_ballot(current_ballot, 1)

        self.updated = pendulum.now()
        self.save()
        return current_ballot.get_js_ballot_model(), current_ballot
