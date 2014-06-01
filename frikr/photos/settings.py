from django.conf import settings

COPYRIGHT = 'RIG'
COPYLEFT = 'LEF'
CREATIVE_COMMONS = 'CC'

LICENSES = getattr(settings, 'LICENSES', (
    (COPYRIGHT, 'Copyright'),
    (COPYLEFT, 'Copyleft'),
    (CREATIVE_COMMONS, 'Creative Commons')
))

"""
Define el remitente de los e-mails
"""
SENDER_EMAIL = getattr(settings, 'SENDER_EMAIL', 'admin@localhost')