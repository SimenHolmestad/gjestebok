from django import template
from ..models import Member, Entry

register = template.Library()

@register.simple_tag
def age_at(member, entry):
    return member.get_age_at(entry.pub_date.date())

