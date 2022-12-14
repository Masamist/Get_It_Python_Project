from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
import requests
from django.views.generic import ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.urls import re_path

from courses.forms import TopicNoteForm

from .models import Course, Question, Topic, Content
from enrolment.models import Result, Enrolment

# Create your views here.


class DeveloperPageView(TemplateView):
    template_name = "courses/developer.html"


class CourseListView(ListView):
    model = Course

    def get(self, request):
        courses = Course.objects.all()
        
        if request.user.is_authenticated:      
            user_results = Result.objects.filter(user=request.user).all()
            enrolments = Enrolment.objects.filter(user=request.user).all()

            for c in courses:
                question_count = c.count_questions
                c.template_user_result = 0
                for e in enrolments:
                    if e.course == c:
                        for a in user_results:
                            if a.question.content.topic.course == c:
                                if a.result==True:
                                    c.template_user_result += 1
                        
                        if question_count > 0:
                            e.grade = int(c.template_user_result / question_count *100 )
                        else:
                            e.grade = 0

            context =  {'courses': courses, 'enrolments': enrolments}
        else:
            context =  {'courses': courses}
                    
        return render(request, 'courses/course_list.html', context)

    def post(self, request):
        courses = Course.objects.all()
        
        if request.user.is_authenticated:      
            user_results = Result.objects.filter(user=request.user).all()
            enrolments = Enrolment.objects.filter(user=request.user).all()

            for c in courses:
                question_count = c.count_questions
                c.template_user_result = 0
                for e in enrolments:
                    if e.course == c:
                        for a in user_results:
                            if a.question.content.topic.course == c:
                                if a.result==True:
                                    c.template_user_result += 1
                        
                        if question_count > 0:
                            e.grade = int(c.template_user_result / question_count *100 )
                        else:
                            e.grade = 0

            context =  {'courses': courses, 'enrolments': enrolments}
        else:
            context =  {'courses': courses}
                    
        return render(request, 'courses/course_list.html', context)



class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"

    def get(self, request, pk):
        course = Course.objects.get(id=pk)
        topics = Topic.objects.filter(course=course).all()

        contents = Content.objects.filter(topic__course__pk=pk).all()
        print('request.user = ', request.user)
        if request.user.is_authenticated:
            user_results = Result.objects.filter(user=request.user, result=True).all()
            
            for c in contents:
                c.template_user_result = 0
                for a in user_results:
                    if a.question.content == c:
                        c.template_user_result += 1
            context = {'course': course, 'topics': topics, 'contents': contents, 'user_results': user_results}
        else:
            context = {'course': course, 'topics': topics, 'contents': contents}

        return render(request, 'courses/course_detail.html', context)


class CourseNewDetailView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("courses.add_courses")
    model = Course
    #template_name = "courses/course_add.html"
    success_url = "../../../course/courses/list/"
    fields = ["name", "whatHeading", "whatDescription",
              "howHeading", "howDescription", "price"]


class CourseEditDetailView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ("courses.change_courses")
    model = Course
    #template_name = "courses/course_edit.html"
    success_url = "/course/courses/list/"
    fields = ["name", "whatHeading", "whatDescription",
              "howHeading", "howDescription", "price"]


class CourseDeleteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ("courses.delete_courses")
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("course_list")


class TopicListView(DetailView):
    model = Course
    template_name = "courses/topic_list.html"


class TopicNewDetailView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("courses.add_topics")
    model = Topic
    #template_name = "courses/topic_add.html"
    success_url = "/course/courses/list/"
    fields = ["course", "name", "intro"]


class TopicDetailView(DetailView):
    model = Topic
    template_name = "courses/topic_detail.html"
    
    def get(self, request, pk):
        topic = Topic.objects.get(id=pk)
        content = Content.objects.filter(topic__pk=pk).all()
        
        
        if request.user.is_authenticated:
            user_results = Result.objects.filter(user=request.user, result=True).all()

            for c in content:
                c.template_user_result = 0
                for a in user_results:
                    if a.question.content == c:
                        c.template_user_result += 1

        return render(request, 'courses/topic_detail.html', {'content': content,
                                                                'topic': topic})

    
class TopicEditDetailView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ("courses.change_courses")
    model = Topic
    #template_name = "courses/topic_edit.html"
    success_url = "/course/courses/list/"
    fields = ["course", "name", "intro"]


class TopicDeleteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView, DetailView):
    permission_required = ("courses.delete_courses")
    model = Topic
    template_name = "courses/topic_delete.html"
    success_url = reverse_lazy("course_list")


class ContentDetailView(DetailView):
    model = Content
    template_name = "courses/content_detail.html"

    def get(self, request, pk):
        content = Content.objects.get(pk=pk)
        prev_id= content.id - 1
        next_id= content.id + 1
        result_is_correct = None

        if request.user.is_authenticated:
            user_results = Result.objects.filter(user=request.user).all()
            
            context = {'content': content, 'prev_id': prev_id, 'next_id': next_id, 'result_is_correct': result_is_correct, 'user_results': user_results,}
        else:
            context = {'content': content, 'prev_id': prev_id, 'next_id': next_id, 'result_is_correct': result_is_correct }

        return render(request, 'courses/content_detail.html', context)


class ContentNewDetailView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ("courses.add_topics")
    model = Content
    template_name = "courses/content_add.html"
    success_url = "../../../courses/list/"
    fields = ["topic", "name", "explanation", "example", "minutesToComplete"]


def answer_true(request, id, pk):
    question = get_object_or_404(Question, id=id)
    result_is_correct = None
    
    if question.answer:
        result = Result.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'result': True})
        result_is_correct = True
    else:
        result = Result.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'result': False})
        result_is_correct = False

    return JsonResponse({'result_is_correct': result_is_correct})


def answer_false(request, id, pk):
    question = get_object_or_404(Question, id=id)
    result_is_correct = None
    
    if not question.answer:
        result = Result.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'result': True})
        result_is_correct = True
    else:
        result = Result.objects.update_or_create(
            user=request.user,
            question=question,
            defaults={'result': False})
        result_is_correct = False

    return JsonResponse({'result_is_correct': result_is_correct})


def enrol(request, pk):
    course = get_object_or_404(Course, id=pk)
    
    enrolment = Enrolment.objects.update_or_create(
        user=request.user,
        course=course,
        defaults={'grade': 0})
    
    enrolment.save()

    return JsonResponse({'is_correct': enrolment.access})
