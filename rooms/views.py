from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, UpdateView, FormView
from django.views.generic.base import View

from rooms.forms import SearchForm, CreatePhotoForm
from rooms.models import Room, Photo
from users.mixins import LoggedInOnlyView


class HomeView(ListView):
    """
    HomeView Definition
    """

    model = Room
    paginate_by = 12
    ordering = "-created"
    paginate_orphans = 5
    context_object_name = "rooms"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoomDetail(DetailView):
    """ RoomDetail Definition"""

    model = Room


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        country = request.GET.get("country")

        if not country:
            form = SearchForm()
            return render(request, "rooms/search.html", {"form": form})

        form = SearchForm(request.GET)

        if not form.is_valid():
            return render(request, "rooms/search.html", {"form": form})

        city = form.cleaned_data.get("city")
        country = form.cleaned_data.get("country")
        room_type = form.cleaned_data.get("room_type")
        price = form.cleaned_data.get("price")
        guests = form.cleaned_data.get("guests")
        bedrooms = form.cleaned_data.get("bedrooms")
        beds = form.cleaned_data.get("beds")
        baths = form.cleaned_data.get("baths")
        instant_book = form.cleaned_data.get("instant_book")
        super_host = form.cleaned_data.get("super_host")
        amenities = form.cleaned_data.get("amenities")
        facilities = form.cleaned_data.get("facilities")
        filter_args = {}

        if city != "Anywhere":
            filter_args["city__startswith"] = city

        filter_args["country"] = country

        if room_type is not None:
            filter_args["room_type"] = room_type

        if price is not None:
            filter_args["price__lte"] = price

        if guests is not None:
            filter_args["guests__gte"] = guests

        if bedrooms is not None:
            filter_args["bedrooms__gte"] = bedrooms

        if beds is not None:
            filter_args["beds__gte"] = beds

        if baths is not None:
            filter_args["baths__gte"] = baths

        if instant_book is True:
            filter_args["instant_book"] = True

        if super_host is True:
            filter_args["host__super_host"] = True

        for amenity in amenities:
            filter_args["amenities"] = amenity

        for facility in facilities:
            filter_args["facilities"] = facility

        qs = Room.objects.filter(**filter_args).order_by("-created")
        paginator = Paginator(qs, 10, orphans=5)
        page = request.GET.get("page", 1)
        rooms = paginator.get_page(page)

        return render(
            request, "rooms/search.html", {"form": form, "rooms": rooms}
        )


class EditRoomView(LoggedInOnlyView, UpdateView):
    model = Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(LoggedInOnlyView, RoomDetail):
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photos(request, room_pk, photo_pk):
    user = request.user
    try:
        room = Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(request, "Can't delete that photo")
        else:
            Photo.objects.filter(pk=photo_pk).delete()
            messages.success(request, "Photo Deleted")
    except Room.DoesNotExist:
        return redirect(reverse("core:home"))
    return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))


class EditPhotoView(LoggedInOnlyView, SuccessMessageMixin, UpdateView):
    model = Photo
    template_name = "rooms/edit_photo.html"
    pk_url_kwarg = "photo_pk"
    fields = ("caption",)
    success_message = "Photo Updated"

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(LoggedInOnlyView, FormView):
    model = Photo
    template_name = "rooms/photo_create.html"
    fields = ("caption", "file")
    form_class = CreatePhotoForm

    def form_valid(self, form):
        pk = self.kwargs.get("pk")
        form.save(**{"pk": pk})
        messages.success(self.request, "Photo Uploaded")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))
