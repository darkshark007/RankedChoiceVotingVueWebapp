import json

from bson import ObjectId
from django.http import JsonResponse, HttpResponse

from rcvserver.models import Poll, User

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
    else:
        poll = Poll()
        poll.creator = user
    poll.update_from_js_poll_model(request_json)

    # Return
    data = poll.get_js_poll_model(user)
    response = JsonResponse(data)
    return response


# API Endpoint for Getting Poll Data for the FrontEnd
def get_poll_data(request):
    user = User.get_user_from_request(request)
    poll_id = request.GET.get('id', default=None)
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
        include_my_ballots = request.GET.get('includeMyBallots', default=None)
        if include_my_ballots:
            data['ballots'] = []
            for ballot in poll.ballots:
                if ballot.user.id == user.id:
                    data['ballots'].append(ballot.get_js_ballot_model())

        include_results = request.GET.get('includeResults', default=None)
        if include_results:
            data['results'] = poll.get_js_result_model(user)

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
        response = JsonResponse(data)
        return response
    return None


def get_my_polls(request):
    user = User.get_user_from_request(request)

    user_polls = Poll.objects.filter(creator__exact={'id': user.id})
    found_ids = set(map(lambda poll: str(poll.id), user_polls))
    public_polls = Poll.objects.filter(public=True).exclude(id__in=found_ids)
    # TODO: Find Polls with User Ballots in them
    data = {
        'polls': list(map(lambda poll: poll.get_js_poll_model(user), user_polls)),
        'ballots': None,
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
        #     # TODO: Add System/Permissions handling for Ballot Choice Additions
        #     response = HttpResponse("User does not have permission to modify that Poll")
        #     response.status_code = 403
        #     return response
    else:
        response = HttpResponse("No PollId found on Request")
        response.status_code = 403
        return response


    # Return
    data = poll.update_ballot_from_js(request_json, user)
    response = JsonResponse(data)
    return response


