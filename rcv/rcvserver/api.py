import json

from django.http import JsonResponse

from rcvserver.models import Poll

# API Endpoint for Creating or Updating Poll Data from the FrontEnd
def create_or_update_poll(request):
    # Parse Request Data
    request_json = request.POST.get('json', default=None)
    if request_json:
        request_json = json.loads(request_json)

    # Process Data
    print(request_json)
    if request_json and request_json.get('id'):
        poll_id = request_json.get('id')
        # TODO: Assert User Permission to Modify Poll
        poll = Poll.objects.get(id=poll_id)
        poll.update_from_poll_model(request_json)
    else:
        poll = Poll()
        # TODO: Add User Information
    poll.update_from_poll_model(request_json)

    # Return
    data = {
        'fish': request_json.get('fish'),
        'nested': request_json.get('nested'),
    }
    response = JsonResponse(data)
    return response


# API Endpoint for Getting Poll Data for the FrontEnd
def get_poll_data(request):
    pass