from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .forms import UploadFileForm, FamousForm, EditFamousForm, UploadVideoForm
from .models import UpForm, Famous, Video
from .detect_image import _detect_image
from .detect_video import _detect_video
import cv2
import json
import os
from collections import OrderedDict
from collections import Counter

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_json = os.path.join(BASE_DIR, 'search_image/data.json')


def removekey(d, key):
    r = dict(d)
    del r[key]
    return r


def index(request):
    UF = UploadFileForm()
    news = UpForm.objects.filter(
        label_detected__isnull=False).order_by('-id')[:10]
    lst = []
    lst1 = []
    lst2 = []
    # return render(request,'home.html', {'UF': UF})
    for i in news:
        lst.append(i.label_detected)

    for j in lst:
        x = j.split(",")
        for k in x:
            lst1.append(k)

    name = Counter(lst1).most_common()
    a = dict(name)
    for i in a:
        lst2.append(i)
    if len(lst2) == 1:
        n = lst2[0]
        value = Video.objects.filter(label=n).order_by('id')[:4]

        return render(request, 'home.html', {'UF': UF, 'news': value})
    elif len(lst2) == 2:
        n = lst2[0]
        n1 = lst2[1]
        value = Video.objects.filter(label=n).order_by('id')[:2]
        value1 = Video.objects.filter(label=n1).order_by('id')[:2]

        return render(request, 'home.html', {'UF': UF, 'value': value, 'value1': value1})
    elif len(lst2) == 3:
        n = lst2[0]
        n1 = lst2[1]
        value = Video.objects.filter(label=n).order_by('id')[:2]
        value1 = Video.objects.filter(label=n1).order_by('id')[:2]
        return render(request, 'home.html', {'UF': UF, 'value': value, 'value1': value1})
    else:
        n = lst2[0]
        n1 = lst2[1]
        value = Video.objects.filter(label=n).order_by('id')[:2]
        value1 = Video.objects.filter(label=n1).order_by('id')[:2]

        return render(request, 'home.html', {'UF': UF, 'value': value, 'value1': value1})


def error(request, exception):
    return render(request, 'error.html')


def addVideo(request):
    VF = UploadVideoForm()
    return render(request, 'add_video.html', {'VF': VF})


def processVideo(request):
    form = UploadVideoForm(request.POST, request.FILES)
    VF = UploadVideoForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            # Video.objects.filter(pk=191).update(label=h)
            video_db = Video.objects.latest('pk')
            video_read = video_db.video.url
            video_new = '.' + video_read
            result = _detect_video(video_new)
            name = Famous.objects.all()
            result1 = ", ".join(result)

            # return render(request,'list_famous_video.html',{'object_list': name})
            return render(request, 'detect_video.html', {'result': result, 'video_db': video_db, 'object_list': name, 'result1': result1})

    else:

        return render(request, 'add_video.html', {'VF': VF})


def addLabel(request):
    if request.method == 'POST':
        primary_key = request.POST.get("primary_key")

        list_name = request.POST.getlist('select1')
        new_list_name = sorted(list_name)
        name = "-".join(new_list_name)
        Video.objects.filter(pk=primary_key).update(label=name)
        list_famous = Famous.objects.all()
    return render(request, 'list_famous_video.html', {'object_list': list_famous})


def getFile(request):
    form = UploadFileForm(request.POST, request.FILES)
    UF = UploadFileForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            image_db = UpForm.objects.latest('pk')
            primary_key = image_db.pk
            image_read = image_db.image.url
            image_new = '.' + image_read
            image = cv2.cvtColor(cv2.imread(image_new), cv2.COLOR_BGR2RGB)
            result, name = _detect_image(image)
            for i in result:
                t = i
            label = ",".join(sorted(name))
            UpForm.objects.filter(pk=primary_key).update(label_detected=label)
            if len(name) == 0:
                name = None
                return render(request, 'data.html', {'l': result, 'name': name})

            elif len(name) == 1:
                list_video = []
                d = ", ".join(name)
                for i in name:
                    value = Video.objects.filter(label__icontains=i).all()
                    list_video.append(value)

                return render(request, 'data.html', {'l': t, 'name': name, 'video': list_video, 'd': d, 'primary': primary_key})

            elif len(name) == 2:
                label1 = "-".join(sorted(name))
                list_video = []
                d = ", ".join(name)
                for i in name:
                    value = Video.objects.filter(label=i).all()
                    list_video.append(value)

                try:
                    value1 = Video.objects.filter(label=label1).all()
                    list_video.append(value1)
                except Video.DoesNotExist:
                    value1 = []
                    return render(request, 'data.html', {'l': result, 'name': name, 'video': list_video, 'primary': primary_key})

                return render(request, 'data.html', {'l': result, 'name': name, 'video': list_video, 'd': d, 'primary': primary_key})
            else:
                label1 = "-".join(sorted(name))
                list_video = []
                d = ", ".join(name)
                for i in name:
                    value = Video.objects.filter(label__icontains=i).all()
                    list_video.append(value)

                # return render(request,'t.html',{'l': result,'name': name,'video': list_video,'d':d,'primary': primary_key})
                return render(request, 'data.html', {'l': result, 'name': name, 'video': list_video, 'd': d, 'primary': primary_key})

    else:

        return render(request, 'home.html', {'UF': UF})


def DetailVideoView(request, id):
    var_id = id
    video = Video.objects.filter(pk=var_id)
    return render(request, 'detail_video.html', {'video': video})


def DetailVideoSearchView(request, id, id1):
    var_id = id
    var_id_1 = id1
    video = Video.objects.filter(pk=var_id)
    return render(request, 'detail_video_search.html', {'video': video, 'primary': var_id_1})


def DataSearchView(request, id):
    image_db = UpForm.objects.latest('pk')
    primary_key = image_db.pk
    image_read = image_db.image.url
    image_new = '.' + image_read
    image = cv2.cvtColor(cv2.imread(image_new), cv2.COLOR_BGR2RGB)

    result, name = _detect_image(image)

    for i in result:
        t = i
    label = ",".join(sorted(name))
    UpForm.objects.filter(pk=primary_key).update(label_detected=label)
    # if len(name) == 0:
    #     name = None
    #     return render(request,'data.html', {'l': result,'name': name})
    if len(name) == 1:
        list_video = []
        d = ", ".join(name)
        for i in name:
            value = Video.objects.filter(label__icontains=i).all()
            list_video.append(value)

        return render(request, 'data.html', {'l': t, 'name': name, 'video': list_video, 'd': d, 'primary': primary_key})
    elif len(name) == 2:
        label1 = "-".join(sorted(name))
        list_video = []
        d = ", ".join(name)
        for i in name:
            value = Video.objects.filter(label=i).all()
            list_video.append(value)
        try:
            value1 = Video.objects.filter(label=label1).all()
            list_video.append(value1)
        except Video.DoesNotExist:
            value1 = []
            return render(request, 'data.html', {'l': result, 'name': name, 'video': list_video})

        return render(request, 'data.html', {'l': result, 'name': name, 'video': list_video, 'd': d, 'primary': primary_key})


def FamousVideoView(request, famous):

    famous = famous.replace('-', ' ')
    name_video = Video.objects.filter(label__icontains=famous).all()
    return render(request, 'list_name_video.html', {'famous': famous.title().replace('-', ' '), 'name_video': name_video})


def DeleteVideoView(request, id, famous):
    name_video_id = id
    name_video_name = famous
    # name_video.delete()
    return render(request, 'delete_name_video.html', {'id': name_video_id, 'name': name_video_name})


def UpdateVideoView(request, id, famous):
    name_video_id = id
    name_video = Video.objects.get(pk=name_video_id)

    return render(request, 'update_name_video.html', {'name_video': name_video, 'famous': famous})


def UpdateDetailsVideoView(request):
    if request.method == 'POST':
        primary_key = request.POST.get("primary_key")
        title_post = request.POST.get("title")
        famous = request.POST.get("famous")
        description_post = request.POST.get("description")
        Video.objects.filter(pk=primary_key).update(
            title=title_post, description=description_post)
        list_video = Video.objects.filter(label__icontains=famous).all()
        # return render(request,'t.html',{'list_video':list_video,'famous':famous})
        return render(request, 'list_name_video.html', {'name_video': list_video, 'famous': famous})


def AcceptDeleteVideoView(request, id, famous):
    try:
        name_video_delete = Video.objects.get(id=id)
    except Video.DoesNotExist:
        name_video_delete = None

    if name_video_delete is None:
        name = Famous.objects.all()
        return render(request, 'list_famous_video.html', {'object_list': name})

    else:
        get_key = []
        # name_video_delete = Video.objects.get(id=id)
        name_video_delete = Video.objects.get(pk=id)

        video = str(name_video_delete.video)
        link_video = '/media/' + video

        with open(data_json, 'r') as json_file:
            data = json.load(json_file)
        for key, value in data.items():
            for item in value:
                if value['video'] == link_video:
                    get_key.append(key)
                break
        for i in get_key:
            t = removekey(data, i)
            with open(data_json, 'w') as outfile:
                json.dump(t, outfile, indent=4)
            break
        name_video_delete.delete()
        name = Famous.objects.all()
        list_video = Video.objects.filter(label__icontains=famous).all()
        # return render(request,'list_famous_video.html',{'famous': famous, 'object_list': name})
        return render(request, 'list_name_video.html', {'famous': famous, 'object_list': name, 'name_video': list_video})


class AddFamousView(CreateView):
    model = Famous
    form_class = FamousForm
    template_name = 'add_famous.html'


class ListFamousView(ListView):
    model = Famous
    template_name = 'list_famous.html'
    ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        famous_menu_name = Famous.objects.values_list(
            'name', flat=True).distinct()
        famous_name = list(famous_menu_name)
        famous_menu = Famous.objects.all()
        famous_menu = list(famous_menu)
        famous = list(famous_menu)
        video_menu = Video.objects.values_list('label', flat=True).distinct()
        video = list(video_menu)
        famous_list = []
        famous_list.clear()
        for item in famous_menu:
            famous_list.append(item)

        famous = []
        new_data = set(famous_name) ^ set(video_menu)
        new_data = list(new_data)
        for i in famous_menu:
            for j in new_data:
                if j == i.name:
                    famous.append(j)

        context = super(ListFamousView, self).get_context_data(*args, **kwargs)
        context["famous_menu"] = famous_menu
        context["data"] = video_menu
        # context["new_data"] = new_data
        context["new_data"] = famous

        return context


class UpdateFamousView(UpdateView):
    model = Famous
    form_class = EditFamousForm
    template_name = 'update_famous.html'


class DeleteFamousView(DeleteView):
    model = Famous
    template_name = 'delete_famous.html'
    success_url = reverse_lazy('list-famous')


class ListVideoView(ListView):
    model = Famous
    template_name = 'list_famous_video.html'
    ordering = ['-id']
