from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_text
import re

def validate_domain(value):
    # """
    # Let's validate the email passed is in the domain "yourdomain.com"
    # """
    # if not "yourdomain.com" in value:
    #     raise ValidationError(_"Sorry, the email submitted is invalid. All emails have to be registered on this domain only.", status='invalid')

    message = 'Enter a valid domain name.'
    code = 'invalid'
    domain_regex = re.compile(
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}|[A-Z0-9-]{2,})$'  # domain
        # literal form, ipv4 address (SMTP 4.1.3)
        r'|^\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$',
        re.IGNORECASE)
    domain_whitelist = ['localhost']

    value = force_text(value)

    if not value:
        raise ValidationError(message, code=code)

    if (not value in domain_whitelist and not domain_regex.match(value)):
        # Try for possible IDN domain-part
        try:
            value = value.encode('idna').decode('ascii')
            if not domain_regex.match(value):
                raise ValidationError(message, code=code)
            else:
                return
        except UnicodeError:
            pass
        raise ValidationError(message, code=code)



# from django.core.exceptions import ValidationError