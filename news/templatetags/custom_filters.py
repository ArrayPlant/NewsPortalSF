from django import template
import re

register = template.Library()

BAD_WORDS = ['редиска']


@register.filter(name='censor')
def censor(text):
    if not isinstance(text, str):
        raise ValueError('Цензор может применяться только к строкам!')

    for bad_word in BAD_WORDS:
        pattern = re.compile(bad_word[0] + r'[a-zа-я]*', re.IGNORECASE)
        text = pattern.sub(bad_word[0] + '*' * (len(bad_word) - 1), text)

    return text
