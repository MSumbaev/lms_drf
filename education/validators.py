import re

from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        value_tmp = dict(value).get(self.field)
        link_pattern = r'https?://\S+|www\.\S+'
        youtube_pattern = r'(?:https?://)?(?:www\.)?youtube\.com'

        links = re.findall(link_pattern, value_tmp)

        for link in links:
            if not bool(re.match(youtube_pattern, link)):
                raise ValidationError('Можете добавить ссылку только на \'youtube.com\' !')
