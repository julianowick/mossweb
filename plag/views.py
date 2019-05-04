from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect

from .models import Course
from .models import Assignment
from .forms import AssignmentForm

def index(request):

    courses = Course.objects.all()

    template = loader.get_template('plag/index.html')
    context = {
        'courses': courses,
    }

    return HttpResponse(template.render(context, request))

def course(request, course_id):

    try:
        course = Course.objects.get(pk=course_id)
    except:
        raise Http404("Course does not exist")

    return render(request, 'plag/course.html', {'course': course})

def upload(request, assignment_id):
    try:
        assignment = Assignment.objects.get(pk=assignment_id)
    except:
        raise Http404("Assignment does not exist")

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect('course', assignment.course.id)
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'plag/upload.html', {'assignment': assignment, 'form': form})
