from question.models import Question

# def admin_status(user_id):
#     current_user = User.objects.get(id=user_id):
#     return current_user.is_admin

def check_obj(Model, obj_id):
    '''
        this method checks if an item with id provided exists
    '''
    if Model.objects.get(id=obj_id):
        return True
    return False

def check_obj_dup(meetup_id, title, body):
    '''
        this method checks if the question already exists
    '''
    if Question.objects.filter(meetup_id=meetup_id, title=title, body=body):
        return True
    return False

def qus_details(qus_object):
    '''
        this method packages question properties for display
    '''
    details = {
        'id': qus_object.id,
        'title': qus_object.title,
        'body': qus_object.body,
        'votes': {'up votes': 0, 'down votes': 0},
        'created_by': qus_object.created_by,
        'date_created': str(qus_object.date_created),
        'date_modified': str(qus_object.date_modified)
    }
    return details

def fields_checker(payload):
    '''
        this method checks for missing required fields
    '''
    missing_fields = []
    fields = ['title', 'body', 'created_by']
    for field in fields:
        if field not in payload.keys():
            missing_fields.append(field)
    return missing_fields
