from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import \
    ( DetailView,
      ListView )

from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .models import Cars
from .forms import CarsForm
from .filters import CarFilter

# Create your views here.


def car_filter(request):
    car_list = Cars.objects.all()
    car_filter = CarFilter(request.GET, queryset=car_list)
    return render(request, 'cars/car_filter.html', {'filter': car_filter})


class Car_list_view(ListView):
    template_name = "cars/cars.html"
    model = Cars
    context_object_name = 'cars'
    paginate_by = 3
    filterset_class = CarFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def cars_list(request):
    pg = Paginator(Cars.objects.all().order_by('year_of_production'), 2)
    page_number = request.GET.get('page')
    try:
        cars = pg.page(page_number)
    except EmptyPage:
        cars = pg.page(pg.num_pages)
    except PageNotAnInteger:
        cars = pg.page(1)
    return render(request, 'cars/cars.html', {'cars':cars})


@staff_member_required
def add_car(request):
    submitted = False
    if request.method == "POST":
        form = CarsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(redirect_to=reverse("main_app:add-car"))
    else:
        form = CarsForm
        if 'submitted' in request.GET:
            submitted = True
    return render(request, "cars/add_car.html", {'form': form, 'submitted': submitted})


class CarsDetailView(DetailView):
    template_name = "cars/cars_detail.html"
    #queryset = Cars.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Cars, id=id_)


def search_car(request):
    if request.method == "POST":
        search = request.POST.get('car_search')
        #cars = Cars.objects.filter(mark=search)
        cars = Cars.objects.filter(Q(mark=search) | Q(model=search) )
        return render(request, "cars/search_car.html", {'query': search, 'query_base': cars})
    else:
        return render(request, "cars/search_car.html", {})



@login_required(login_url="/user_account/login/")
def get_reservation_view(request, cars_id):
    car = Cars.objects.get(pk=cars_id)
    if car.car_is_rented == False:
        car.car_is_rented = True
        car.save()
        return render(request, "cars/cars_status.html", {'car': car})
    else:
        return render(request, "cars/cars_status.html", {'car': car})

# def update_view(request, cars_id ):
#     car = Cars.objects.get(pk=cars_id)
#     return render(request, 'cars/cars_info_update.html', {'car':car})

@staff_member_required
def update_view(request, cars_id):
    car = Cars.objects.get(pk=cars_id)
    form = CarsForm(request.POST or None, instance=car)
    if form.is_valid():
        form.save()
        return redirect('http://127.0.0.1:8000/cars/')
    return render(request, 'cars/cars_info_update.html',
                  {'car':car,
                   'form':form
                   })

