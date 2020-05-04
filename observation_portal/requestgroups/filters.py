import django_filters
from observation_portal.requestgroups.models import RequestGroup, Request
from observation_portal.common.configdb import configdb


class RequestGroupFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(field_name='created', lookup_expr='gte', label='Submitted after')
    created_before = django_filters.DateTimeFilter(field_name='created', lookup_expr='lte', label='Submitted before')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains', label='Name contains')
    state = django_filters.ChoiceFilter(choices=RequestGroup.STATE_CHOICES)
    user = django_filters.CharFilter(field_name='submitter__username', lookup_expr='icontains', label='Username contains')
    exclude_state = django_filters.ChoiceFilter(field_name='state', choices=RequestGroup.STATE_CHOICES, label='Exclude State', exclude=True)
    # TODO: Fill in telescope_class choices from configdb
    # telescope_class = django_filters.ChoiceFilter(
    #     choices=Location.TELESCOPE_CLASSES, field_name='requests__location__telescope_class', distinct=True,
    # )
    target = django_filters.CharFilter(
        field_name='requests__configurations__target__name', lookup_expr='icontains', label='Target name contains',
        distinct=True
    )
    modified_after = django_filters.DateTimeFilter(field_name='requests__modified', lookup_expr='gte', label='Modified After', distinct=True)
    modified_before = django_filters.DateTimeFilter(field_name='requests__modified', lookup_expr='lte', label='Modified Before', distinct=True)
    order = django_filters.OrderingFilter(
        label='Ordered By',
        fields=(
            ('name', 'name'),
            ('modified', 'modified'),
            ('created', 'created'),
            ('requests__windows__end', 'end')
        ),
        field_labels={
            'requests__windows__end': 'End of window',
            'modified': 'Last Update'
        }
    )

    class Meta:
        model = RequestGroup
        fields = (
            'id', 'submitter', 'proposal', 'name', 'observation_type', 'operator', 'ipp_value',  'exclude_state',
            'state', 'created_after', 'created_before', 'user', 'modified_after', 'modified_before'
        )


class RequestFilter(django_filters.FilterSet):
    class Meta:
        model = Request
        fields = ('state',)


class TelescopeStatesFilter(django_filters.FilterSet):
    start = django_filters.DateTimeFilter(lookup_expr='gte', label='Start time for states')
    end = django_filters.DateTimeFilter(lookup_expr='gte', label='End time for states')
    site = django_filters.MultipleChoiceFilter(
        choices=sorted(configdb.get_site_tuples()),
        label='One or Multiple site codes'
    )
    telescope = django_filters.MultipleChoiceFilter(
        choices=sorted(configdb.get_telescope_tuples()),
        label='One or Multiple telescope codes',
    )

class TelescopeAvailabilityFilter(TelescopeStatesFilter):
    combine = django_filters.BooleanFilter(label='Group results by telescope class per site')

class PressureFilter(django_filters.FilterSet):
    site = django_filters.ChoiceFilter(
        choices=sorted(configdb.get_site_tuples()),
        label='Site code - defaults to all sites if none is given'
    )
    instrument = django_filters.ChoiceFilter(
        choices=sorted(configdb.get_instrument_type_tuples()),
        label='Instrument type - defaults to all instrument types if none is given'
    )