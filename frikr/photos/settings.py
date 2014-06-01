from django.conf import settings

COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

LICENSES = getattr(settings, 'LICENSES', (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative Commons')
))