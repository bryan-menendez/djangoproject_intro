from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice


def details(request, question_id):
    # try:
    #     q = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")

    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/details.html', {'question': q})


def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': q})


def vote(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html',
                      {
                          'question': q,
                          'error_message': "you didnt select a choice u sneaki boi"
                      })
    else:
        selected_choice.votes += 1
        selected_choice.save()

    return HttpResponseRedirect(reverse('polls:results', args=(question_id, )))


def index(request):
    q_list = Question.objects.order_by('-pub_date')[:5]
    context = {'q_list': q_list}
    return render(request,'polls/index.html', context)
