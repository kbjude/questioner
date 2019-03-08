from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from question.models import Question

@csrf_exempt
def questions(request):
    '''
        this views method is responsible for the following;
        - creating new questions
        - getting all questions from the database
    '''
    if request.method == 'POST':
        payload = json.loads(request.body)
        title = payload['title']
        body = payload['body']
        created_by = payload['created_by']
        question = Question(title=title, body=body, created_by=created_by, date_created=timezone.now(), date_modified=timezone.now())
        try:
            # if not Question.objects.get(title=title) or not Question.objects.get(title=title):
            question.save()
            response = json.dumps([{'message': 'question successfully added'}])
            # response = json.dumps([{'error': 'question already exists'}])
        except:
            response = json.dumps([{'error': 'question could not be added'}])

    if request.method == 'GET':
        questions = Question.objects.all().order_by('date_modified').reverse()
        response = json.dumps([{"Message": "No questions available"}])
        all_questions = []
        for question in questions:
            qus_details = {}
            qus_details['id'] = question.id
            qus_details['title'] = question.title
            qus_details['body'] = question.body
            qus_details['created_by'] = question.created_by
            qus_details['date_created'] = str(question.date_created)
            qus_details['date_modified'] = str(question.date_modified)
            all_questions.append(qus_details)
        if all_questions != []:
            response = json.dumps(all_questions)
    return HttpResponse(response, content_type='text/json')

@csrf_exempt
def question(request, question_id):
    '''
        this views method is responsible for the following;
        - getting a question by id
        - updating a question's fields (title, body) by id
        - deleting a question by id
    '''
    question_id = int(question_id)
    if request.method == 'GET':
        try:
            question = Question.objects.get(id=question_id)
            response = json.dumps(
                [
                    {
                        'title': question.title,
                        'body': question.body,
                        'created_by': question.created_by,
                        'date_created': str(question.date_created),
                        'date_modified': str(question.date_modified)
                    }
                ]
            )
        except:
            response = json.dumps([{'error': 'no question available by the id: {}'.format(question_id)}])

    if request.method == 'PUT':
        payload = json.loads(request.body)
        title = payload['title']
        body = payload['body']
        try:
            question = Question.objects.get(id=question_id)
            question.title = title
            question.body = body
            question.date_modified = timezone.now()
            question.save()
            response = json.dumps([{'message': 'question successfully updated'}])
        except:
            response = json.dumps([{'error': 'no question available by the id: {}, update failed!'.format(question_id)}])

    if request.method == 'DELETE':
        try:
            question = Question.objects.get(id=question_id)
            question.delete()
            response = json.dumps([{'message': 'question successfully deleted'}])
        except Exception:
            response = json.dumps([{'error': 'no question available by the id: {}, deletion failed!'.format(question_id)}])
    return HttpResponse(response, content_type='text/json')
