from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from meetup.models import Meeting
from question.models import Question
from question.utils import check_obj, check_obj_dup, qus_details, fields_checker

@csrf_exempt
def questions(request, meetup_id):
    '''
        this views method is responsible for the following;
        - creating new questions
        - getting all questions from the database
    '''
    meetup_id = int(meetup_id)
    try:
        if check_obj(Meeting, meetup_id):
            meeting = Meeting.objects.get(id=meetup_id)
            if request.method == 'POST':
                try:
                    payload = json.loads(request.body)
                    missing_fields = fields_checker(payload)
                    if missing_fields == []:
                        title = payload['title']
                        body = payload['body']
                        created_by = payload['created_by']
                        question = Question(title=title, body=body, created_by=created_by, date_created=timezone.now(), date_modified=timezone.now(), meetup_id=meetup_id, delete_status=False)
                        if check_obj_dup(meetup_id, title, body):
                            response = json.dumps(
                                [
                                    {'error': 'this question has already been asked for this meeting'}
                                ]
                            )
                            status = 400
                        else:
                            question.save()
                            response = json.dumps([{'message': 'question successfully added'}])
                            status = 201
                    else:
                        response = json.dumps([{'error': 'missing {}.'.format(missing_fields)}])
                        status = 400
                except:
                    response = json.dumps([{'error': 'question could not be added'}])
                    status = 400

            if request.method == 'GET':
                status = 200
                questions = Question.objects.filter(meetup_id=meetup_id, delete_status=False).order_by('date_modified').reverse()
                response = json.dumps([{"Message": "No questions available"}])
                all_questions = []
                for question in questions:
                    all_questions.append(qus_details(question))
                if all_questions != []:
                    response = json.dumps({'meeting': meeting.title, 'questions': all_questions})
    except:
        response = json.dumps([{'error': 'no meeting available by the id: {}'.format(meetup_id)}])
        status = 400
    return HttpResponse(response, content_type='text/json', status=status)

@csrf_exempt
def question(request, meetup_id, question_id):
    '''
        this views method is responsible for the following;
        - getting a question by id
        - updating a question's fields (title, body) by id
        - deleting a question by id
    '''
    meetup_id = int(meetup_id)
    try:
        if check_obj(Meeting, meetup_id):
            meeting = Meeting.objects.get(id=meetup_id)
            question_id = int(question_id)
            if request.method == 'GET':
                try:
                    if check_obj(Question, question_id):
                        question = Question.objects.get(id=question_id, meetup_id=meetup_id)
                        if question:
                            response = json.dumps({'meeting': meeting.title, 'question': qus_details(question)})
                            status = 200
                except:
                    response = json.dumps(
                        [
                            {
                                'error': "no question available by the id='{}' for {}.".format(
                                    question_id,
                                    meeting.title
                                )
                            }
                        ]
                    )
                    status = 400

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
                    status = 200
                except:
                    response = json.dumps([{'error': 'no question available by the id: {}, update failed!'.format(question_id)}])
                    status = 400

            if request.method == 'DELETE':
                try:
                    question = Question.objects.get(id=question_id)
                    question.delete()
                    response = json.dumps([{'message': 'question successfully deleted'}])
                except:
                    response = json.dumps([{'error': 'no question available by the id: {}, deletion failed!'.format(question_id)}])
                    status = 400
    except:
        response = json.dumps([{'error': 'no meeting available by the id: {}'.format(meetup_id)}])
        status = 400
    return HttpResponse(response, content_type='text/json', status=status)
