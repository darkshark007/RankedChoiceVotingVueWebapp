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
        if poll.creator.id != user.id:
            response = HttpResponse("User does not have permission to modify that Poll")
            response.status_code = 403
            return response
    else:
        poll = Poll()
        poll.creator = user
    poll.update_from_js_poll_model(request_json)

    # Return
    data = poll.get_js_poll_model()
    response = JsonResponse(data)
    return response


# API Endpoint for Getting Poll Data for the FrontEnd
def get_poll_data(request):
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

        data = poll.get_js_poll_model()
        # TODO: Assert User Permission to Modify Poll
        response = JsonResponse(data)

    return response


def get_my_polls(request):
    user = User.get_user_from_request(request)

    user_polls = Poll.objects.filter(creator__exact={'id': user.id})
    data = {
        'polls': list(map(lambda poll: poll.get_js_poll_model(), user_polls))
    }
    response = JsonResponse(data)
    return response
