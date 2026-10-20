"""Shared Jinja snippets for the templates.

Shorthand tokens are expanded by ``x()`` so the content files stay readable:

    @T@  -> {{ T }}            (Trustor / Settlor)
    @Ts@ -> {{ Ts }}           (Trustors / Settlors)
    @S1@ -> {{ s1_name }}      @S2@ -> {{ s2_name }}
    @DATE@ -> signing date, or a highlighted blank
    @TRUSTID@ -> trust name with its date (handles restatements)
    @ART:key@ -> {{ art["key"] }}  (article number in words)
    @SUB@ -> {{ subtrust_name }}
"""

import re

DATE = ('{% if trust_date_known %}{{ signing_date_text }}{% else %}'
        '<ph>____________________, 20____</ph>{% endif %}')

DATED = ('{% if is_restatement %}dated {{ original_dated }}, as restated on ' + DATE +
         '{% else %}dated ' + DATE + '{% endif %}')

TRUSTID = '{{ trust_title }}, ' + DATED

COUNTY = ('{% if signing_county %}{{ signing_county }}{% else %}'
          '<ph>____________________</ph>{% endif %}')


def x(text):
    text = text.replace('@TRUSTID@', TRUSTID)
    text = text.replace('@DATED@', DATED)
    text = text.replace('@DATE@', DATE)
    text = text.replace('@COUNTY@', COUNTY)
    text = text.replace('@Ts@', '{{ Ts }}')
    text = text.replace('@T@', '{{ T }}')
    text = text.replace('@S1@', '{{ s1_name }}')
    text = text.replace('@S2@', '{{ s2_name }}')
    text = text.replace('@SUB@', '{{ subtrust_name }}')
    text = re.sub(r'@ART:(\w+)@', r'{{ art["\1"] }}', text)
    leftover = re.search(r'@[A-Za-z0-9:]+@', text)
    assert not leftover, 'unexpanded token %s in %r' % (leftover.group(0), text)
    return text


class X:
    """Wrap a Builder so every text argument goes through x()."""

    def __init__(self, builder):
        self.b = builder

    def __getattr__(self, name):
        fn = getattr(self.b, name)

        def call(*args, **kwargs):
            args = [x(a) if isinstance(a, str) else a for a in args]
            return fn(*args, **kwargs)
        return call
