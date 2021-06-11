import json
import pendulum

from bson import ObjectId
from django.http import JsonResponse, HttpResponse

from rcvserver.models import Poll, User, Result

# API Endpoint for Creating or Updating Poll Data from the FrontEnd
def create_or_update_poll(request):
    # Parse Request Data
    request_json = request.POST.get('json', default=None)
    if request_json:
        request_json = json.loads(request_json)

    # Process Data
    user = User.get_user_from_request(request)
    if request_json and request_json.get('id'):
        poll_id = request_json.get('id')
        poll = Poll.objects.get(id=poll_id)
        # if poll.creator.id != user.id:
        #     # TODO: Add System/Permissions handling for Ballot Choice Additions
        #     response = HttpResponse("User does not have permission to modify that Poll")
        #     response.status_code = 403
        #     return response
        # if poll.locked:
        #     # TODO: If Poll is locked, block updates to Choices
        #     response = HttpResponse("This poll is locked.  Ballot changes cannot be made")
        #     response.status_code = 403
        #     return response
    else:
        poll = Poll()
        poll.results = Result()
        poll.creator = user
    poll.update_from_js_poll_model(request_json, user)

    # Return
    data = poll.get_js_poll_model(user)
    response = JsonResponse(data)
    return response


def recycle_poll(request):
    request_data = json.loads(request.POST.get('json', default=None))
    if not request_data:
        response = HttpResponse("Invalid Request data")
        response.status_code = 400
        return response

    user = User.get_user_from_request(request)
    poll_id = request_data.get('id')
    if not ObjectId.is_valid(poll_id):
        response = HttpResponse("Given Id is not valid ObjectId")
        response.status_code = 400
        return response

    if poll_id:
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            response = HttpResponse("Given Poll does not exist")
            response.status_code = 403
            return response

        timestamp = pendulum.now()

        # Clone the old Poll
        new_id = ObjectId()
        poll.id = new_id
        poll.save()

        recycled_poll = Poll.objects.get(id=new_id)
        recycled_poll.parent = str(poll_id)
        recycled_poll.updated = timestamp
        recycled_poll.locked = True
        recycled_poll.save()

        poll = Poll.objects.get(id=poll_id)
        poll.created = timestamp
        poll.updated = timestamp
        poll.ballots = []
        poll.results = Result()
        poll.init_stats()
        poll.save()

    return get_poll_data(request)


# API Endpoint for Getting Poll Data for the FrontEnd
def get_poll_data(request):
    request_data = getattr(request, request.method)
    request_json = request_data.get('json', default=None)
    if request_json:
        request_data = json.loads(request_json)
    if not request_data:
        response = HttpResponse("Invalid Request data")
        response.status_code = 400
        return response

    user = User.get_user_from_request(request)
    poll_id = request_data.get('id')
    if not ObjectId.is_valid(poll_id):
        response = HttpResponse("Given Id is not valid ObjectId")
        response.status_code = 400
        return response

    if poll_id:
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            response = HttpResponse("Given Poll does not exist")
            response.status_code = 403
            return response

        data = poll.get_js_poll_model(user)
        user_can_see_results = poll.can_get_results(user)
        include_my_ballots = request_data.get('includeMyBallots')
        if include_my_ballots:
            data['ballots'] = []
            data['ballotsPublic'] = []
            for ballot in poll.ballots:
                if ballot.user.id == user.id:
                    data['ballots'].append(ballot.get_js_ballot_model())
                elif user_can_see_results and poll.public_ballots != 'no' and (poll.public_ballots == 'yes' or ballot.public):
                    data['ballotsPublic'].append(ballot.get_js_ballot_model())

        include_results = request_data.get('includeResults')
        if include_results:
            if user_can_see_results:
                data['results'] = poll.get_js_result_model(user)
            else:
                response = HttpResponse("Poll Results are unavailable")
                response.status_code = 403
                return response

        include_old_polls = request_data.get('includeOldPolls')
        if include_old_polls:
            data['oldPolls'] = []
            if poll.allow_users_to_see_archived_polls == True or poll.creator.id == user.id:
                for old_poll in Poll.objects.filter(parent=poll_id):
                    data['oldPolls'].append({
                        'id': str(old_poll.id),
                        'created': old_poll.created,
                        'name': old_poll.name,
                    })

        response = JsonResponse(data)

    return response


# API Endpoint for Getting Poll Data for the FrontEnd
def get_ballot_data(request):
    user = User.get_user_from_request(request)
    poll_id = request.GET.get('pollId', default=None)
    if not ObjectId.is_valid(poll_id):
        response = HttpResponse("Given PollId is not valid ObjectId")
        response.status_code = 400
        return response

    ballot_id = request.GET.get('ballotId', default=None)
    if not ObjectId.is_valid(ballot_id):
        response = HttpResponse("Given BallotId is not valid ObjectId")
        response.status_code = 400
        return response

    if poll_id and ballot_id:
        try:
            poll = Poll.objects.get(id=poll_id)
        except Poll.DoesNotExist:
            response = HttpResponse("Given Poll does not exist")
            response.status_code = 403
            return response

        current_ballot = None
        for ballot in poll.ballots:
            if ballot.id == ballot_id:
                current_ballot = ballot
                break
        if current_ballot:
            if current_ballot.user.id != user.id:
                response = HttpResponse("User does not have permission to access that Ballot")
                response.status_code = 403
                return response
            data = current_ballot.get_js_ballot_model()
        else:
            response = HttpResponse("Given Ballot does not exist")
            response.status_code = 403
            return response

        include_stats = request.GET.get('includeStats', default=None)
        if include_stats:
            data['stats'] = poll.get_stats_for_ballot(current_ballot)

        response = JsonResponse(data)
        return response
    return None


def get_my_polls(request):
    user = User.get_user_from_request(request)

    user_polls = Poll.objects.filter(creator__exact={'id': user.id}, parent=None)
    found_ids = set(map(lambda poll: str(poll.id), user_polls))
    ballot_polls = Poll.objects.filter(ballots={'user.id': user.id}).exclude(id__in=found_ids)
    found_ids = found_ids | set(map(lambda poll: str(poll.id), ballot_polls))
    public_polls = Poll.objects.filter(public=True, parent=None).exclude(id__in=found_ids)
    data = {
        'polls': list(map(lambda poll: poll.get_js_poll_model(user), user_polls)),
        'ballots': list(map(lambda poll: poll.get_js_poll_model(user), ballot_polls)),
        'public': list(map(lambda poll: poll.get_js_poll_model(user), public_polls)),
    }

    response = JsonResponse(data)
    return response


# API Endpoint for Creating or Updating Ballot Data from the FrontEnd
def create_or_update_ballot(request):
    # Parse Request Data
    request_json = request.POST.get('json', default=None)
    if request_json:
        request_json = json.loads(request_json)

    # Process Data
    user = User.get_user_from_request(request)
    if request_json and request_json.get('pollId'):
        poll_id = request_json.get('pollId')
        poll = Poll.objects.get(id=poll_id)
        # if poll.creator.id != user.id:
        #     response = HttpResponse("User does not have permission to modify that Poll")
        #     response.status_code = 403
        #     return response
    else:
        response = HttpResponse("No PollId found on Request")
        response.status_code = 403
        return response

    # Return
    data, current_ballot = poll.update_ballot_from_js(request_json, user)
    if type(data) is HttpResponse:
        return data

    include_stats = request_json.get('includeStats')
    if include_stats:
        data['stats'] = poll.get_stats_for_ballot(current_ballot)

    response = JsonResponse(data)
    return response


