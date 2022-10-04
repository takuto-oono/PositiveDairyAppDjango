from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import DairyContent, PictureCategory, DairyPicture
from .forms import CategoryForm
import datetime
import json


def create_date_obj(date: str) -> datetime:
    return datetime.datetime.strptime(date, '%Y-%m-%d').date()


@login_required
def index(request: HttpRequest):
    print(request.user.email)
    context = {
        'today': datetime.date.today().strftime("%Y-%m-%d"),
    }
    print(context)
    return render(request, 'dairyApp/index.html', context)


@login_required
@require_POST
def post_dairy_content(request: HttpRequest) -> JsonResponse:
    dairy_content = {
        'content': request.POST.get('content'),
        'date': request.POST.get('date'),
        'ranking': request.POST.get('ranking'),
    }

    try:
        dairy_content_obj = DairyContent.objects.get(user_object=request.user,
                                                     date=create_date_obj(dairy_content['date']),
                                                     ranking=dairy_content['ranking'], )
        dairy_content_obj.content = dairy_content['content']
        dairy_content_obj.save()
    except DairyContent.DoesNotExist:
        DairyContent.objects.create(user_object=request.user, date=create_date_obj(dairy_content['date']),
                                    ranking=dairy_content['ranking'], content=dairy_content['content'])
    return JsonResponse({
        'dairyContent': dairy_content
    })


@login_required
@require_GET
def get_dairy_content(request: HttpRequest) -> JsonResponse:
    ranking = request.GET.get('ranking')
    date = request.GET.get('date')
    print(date)
    print(ranking)
    if ranking not in ['1', '2', '3']:
        return JsonResponse({
            'status': 404,
            'message': 'rankingが正しくない'
        })

    if date is None:
        return JsonResponse({
            'status': 404,
            'message': '日付が正しくない',
        })

    try:
        content = DairyContent.objects.get(user_object=request.user, ranking=ranking,
                                           date=datetime.datetime.strptime(date,
                                                                           '%Y-%m-%d').date()).content
        return JsonResponse({
            'status': 200,
            'content': content
        })
    except DairyContent.DoesNotExist:
        return JsonResponse({
            'status': 404,
        })


@login_required
@require_POST
def delete_dairy_content(request: HttpRequest) -> JsonResponse:
    try:
        dairy_content = DairyContent.objects.get(user_object=request.user, content=request.POST.get('content'),
                                                 ranking=request.POST.get('ranking'), date=request.POST.get('date'))
        dairy_content.delete()
        return JsonResponse({
            'status': 200,
        })
    except DairyContent.DoesNotExist:
        return JsonResponse({
            'status': 404
        })


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = PictureCategory
    form_class = CategoryForm
    template_name = 'dairyApp/create_category.html'

    def form_valid(self, form):
        picture_category = form.save(commit=False)
        picture_category.user_object = self.request.user
        picture_category.picture_count = 0
        picture_category.save()

    def get_success_url(self):
        return redirect('show_pictures')


class ShowPicturesView(LoginRequiredMixin, ListView):
    model = DairyPicture
    paginate_by = 50
    template_name = 'dairyApp/show_pictures.html'

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        if category_id:
            try:
                category = PictureCategory.objects.get(user_object=self.request.user, pk=category_id)
                return DairyPicture.objects.filter(user_object=self.request.user,
                                                   category=category)
            except PictureCategory.DoesNotExist:
                raise Http404('not find')

        return DairyPicture.objects.filter(user_object=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['picture_categories'] = PictureCategory.objects.filter(user_object=self.request.user)
        return context
