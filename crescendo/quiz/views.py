from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from .models import Quiz_question
from home.models import User_profile
from collections import Counter


@login_required
def take_quiz(request):
    return render(request, "quiz/landing.html")

@login_required
def quiz(request, pk):
    key = pk
    question = get_object_or_404(Quiz_question, id=pk)
    if request.method == "POST":
        selected_option = request.POST.get('selected')
        quiz_answers = request.session.get('quiz_answers', {})
        quiz_answers[str(pk)] = selected_option
        request.session['quiz_answers'] = quiz_answers
        next_id = pk + 1
        if not Quiz_question.objects.filter(id=next_id).exists():
            return HttpResponseRedirect("/quiz/result")
        return HttpResponseRedirect(f"/quiz/{next_id}/")
    return render(request, "quiz/quiz.html", {"key": key, "question": question})

def quiz_result(request):
    quiz_answers = request.session.get('quiz_answers', {})

    # If someone directly hits /result without quiz
    if not quiz_answers:
        return redirect('/quiz/1/')

    # Count selections
    counter = Counter(quiz_answers.values())

    result = {
        'a': counter.get('a', 0),
        'b': counter.get('b', 0),
        'c': counter.get('c', 0),
    }   

    most_selected = counter.most_common(1)[0][0] if counter else None
    user_class = None
    if most_selected == 'a':
        user_class = 'Knight'
    elif most_selected == 'b':
        user_class = 'Ninja'
    elif most_selected == 'c':
        user_class = 'Alchemist'
    # --- SAVE TO DATABASE ---
    if user_class and request.user.is_authenticated:
        # Get the profile for the logged in user
        profile, created = User_profile.objects.get_or_create(user=request.user)
        profile.user_class = user_class
        profile.is_quiz_completed = True
        profile.save()
        
        # --- CLEANUP ---
        # Clear the session so they start fresh if they ever retake it
        del request.session['quiz_answers']

    context = {
        'result': result,
        'user_class': user_class,
    }
    return render(request, 'quiz/result.html', context)
 
