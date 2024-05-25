from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from .models import Question
from django.utils import timezone
from .forms import QuestionForm, AnswerForm

# Create your views here.
def index(request):
    """_summary_

    pybo 목록
    """
    page = request.GET.get('page', 1)
    question_list = Question.objects.order_by('-create_date')
    
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list': page_obj}
    return render(request,'pybo/question_list.html',context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request,'pybo/question_detail.html',context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content = request.POST.get('content'),
                                create_date = timezone.now())
    answer.save()
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.create_date = timezone.now()
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = AnswerForm()
    return render(request, 'pybo/question_detail.html', {'question': question, 'form': form })

def question_create(request):
    """질문등록

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm()
        context = {'form': form}
    return render(request,'pybo/question_form.html',{'form': form})