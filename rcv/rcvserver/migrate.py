from rcvserver.models import Poll

def migrate():

    # Migration #1 (06/04/2021)
    #   - Migrate limit_rank_choices, changed default/no limit value from -1 to None
    #   Local:  Done
    #   Prod:   Done
    if False:
        print('Running Migration #1')
        for p in Poll.objects.all():
            if p.limit_rank_choices == -1:
                print('Updating Poll <{}>'.format(p.id))
                p.limit_rank_choices = None
                p.save()
