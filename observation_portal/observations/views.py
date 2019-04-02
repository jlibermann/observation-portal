from django_filters.views import FilterView
from django.views.generic import DetailView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from django.core.cache import cache
from django.utils import timezone
from rest_framework.response import Response
from datetime import timedelta

from observation_portal.observations.models import Observation
from observation_portal.common.mixins import StaffRequiredMixin
from observation_portal.observations.filters import ObservationFilter


class ObservationDetailView(StaffRequiredMixin, DetailView):
    model = Observation


class ObservationListView(StaffRequiredMixin, FilterView):
    model = Observation
    filterset_class = ObservationFilter
    paginate_by = 50
    ordering = '-modified'
    template_name = 'observations/observation_list.html'


class LastScheduledView(APIView):
    """
        Returns the datetime of the last time new observations were submitted. This endpoint is expected to be polled
        frequently (~every 5 seconds) to for a client to decide if it needs to pull down the schedule or not.

        We are only updating when observations are submitted, and not when they are cancelled, because a site should
        not really care if the only change was removing things from it's schedule.
    """
    permission_classes = (IsAdminUser,)

    def get(self, request):
        last_schedule_time = cache.get('observation_portal_last_schedule_time', timezone.now() - timedelta(days=7))
        return Response({'last_schedule_time': last_schedule_time})
