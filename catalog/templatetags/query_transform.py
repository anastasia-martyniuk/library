from django import template
from django.template.defaulttags import register

reqister = template.Library()


@register.simple_tag
def query_transform(request, **kwargs):
    update = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            update[k] = v
        else:
            update.pop(k, 0)

    return update.urlencode()
