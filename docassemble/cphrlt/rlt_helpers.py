# Helper classes and functions for the Joint Revocable Living Trust interview.
#
# Everything here is plain Python so the YAML stays declarative. The DOCX
# templates call these through Jinja2 (e.g. ``{{ gift.as_clause(T) }}``).

import re

from docassemble.base.util import DAObject, Person, currency, comma_and_list

__all__ = [
    'RLTPerson',
    'Beneficiary',
    'SpecificGift',
    'TrustAsset',
    'num_word',
    'article_map',
    'article_titles',
    'article_toc',
    'stage_schedule',
    'money',
    'pct',
    'relationship_suggestions',
    'join_list',
    'clean_trust_name',
    'ASSET_TYPES',
    'PLAN_LABELS',
]

_NUM_WORDS = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
              'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen',
              'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen',
              'Nineteen', 'Twenty']

PLAN_LABELS = {
    'survivor': "All to Survivor (Simple Joint Trust)",
    'disclaimer': "Survivor's Trust with Optional Disclaimer Trust",
    'ab': "Mandatory A/B Split (Survivor's Trust and Bypass Trust)",
}

ASSET_TYPES = [
    {'realprop': 'Real property (home, rental, land)'},
    {'bank': 'Bank or credit union account'},
    {'brokerage': 'Brokerage or investment account'},
    {'business': 'Business interest (LLC, corporation, partnership)'},
    {'retirement': 'Retirement account (IRA, 401(k), 403(b), pension)'},
    {'insurance': 'Life insurance or annuity'},
    {'vehicle': 'Vehicle, boat, or RV'},
    {'other': 'Other asset'},
]

# Assets that pass by beneficiary designation are listed in the funding memo,
# not on the trust schedules.
_DESIGNATION_TYPES = ('retirement', 'insurance')


def num_word(n):
    """1 -> 'One'. Falls back to digits past twenty."""
    try:
        n = int(n)
    except (TypeError, ValueError):
        return str(n)
    if 0 <= n < len(_NUM_WORDS):
        return _NUM_WORDS[n]
    return str(n)


def money(amount):
    """Currency without cents when the amount is a whole number."""
    try:
        whole = float(amount) == int(float(amount))
    except (TypeError, ValueError):
        return str(amount)
    return currency(amount, decimals=not whole)


def pct(value):
    """33.3333 -> '33.33%', 50.0 -> '50%'."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        return str(value)
    text = ('%.2f' % value).rstrip('0').rstrip('.')
    return text + '%'


def article_map(plan_type):
    """Map article keys to the words Word's list numbering will print.

    The trust template numbers its articles with an automatic Word list, so
    this order must match the order of the ARTICLE headings in
    joint_rlt_trust.docx. The only optional article is the Bypass/Disclaimer
    Trust article, which exists only for the 'ab' and 'disclaimer' plans.
    """
    keys = ['establishment', 'family', 'property', 'rights', 'trustees',
            'incapacity', 'first_death']
    if plan_type in ('ab', 'disclaimer'):
        keys.append('subtrust')
    keys += ['survivors_trust', 'final', 'beneficiary_trusts', 'powers',
             'special_assets', 'general']
    return {key: num_word(index + 1) for index, key in enumerate(keys)}


def article_titles(plan_type, trustor_word='Trustor'):
    """Article headings, used both in the article headings and the contents list."""
    one = trustor_word
    many = trustor_word + 's'
    titles = {
        'establishment': 'Establishment of the Trust',
        'family': 'Family Information',
        'property': 'Trust Property',
        'rights': 'Rights Reserved by the ' + many,
        'trustees': 'Trustees',
        'incapacity': 'Incapacity',
        'first_death': 'Administration After the Death of the First ' + one,
        'subtrust': 'Bypass Trust' if plan_type == 'ab' else 'Disclaimer Trust',
        'survivors_trust': "The Survivor's Trust",
        'final': 'Distribution After the Deaths of Both ' + many,
        'beneficiary_trusts': 'Trusts for Beneficiaries',
        'powers': 'Trustee Powers',
        'special_assets': 'Retirement Benefits and Special Assets',
        'general': 'General Provisions',
    }
    return titles


def article_toc(plan_type, trustor_word='Trustor'):
    """[{'num': 'One', 'title': 'Establishment of the Trust'}, ...] in article order.

    Printed as a static contents list, so no LibreOffice field update is needed
    when the document is assembled.
    """
    numbers = article_map(plan_type)
    titles = article_titles(plan_type, trustor_word)
    order = sorted(numbers, key=lambda key: _NUM_WORDS.index(numbers[key]))
    return [{'num': numbers[key], 'title': titles[key]} for key in order]


def stage_schedule(count, ages):
    """Return [{'age': 25, 'portion': 'one-third (1/3)'}, ...] for staged trusts.

    Each stage distributes a fraction of the balance then on hand so the last
    stage always distributes everything that remains.
    """
    count = int(count)
    ages = [int(a) for a in ages[:count]]
    portions = {
        1: ['the entire balance'],
        2: ['one-half (1/2)', 'the entire balance'],
        3: ['one-third (1/3)', 'one-half (1/2)', 'the entire balance'],
    }[count]
    return [{'age': age, 'portion': portion, 'last': idx == count - 1}
            for idx, (age, portion) in enumerate(zip(ages, portions))]


_SMALL_WORDS = {'a', 'an', 'and', 'for', 'in', 'of', 'on', 'or', 'the', 'to'}


def clean_trust_name(name):
    """Normalize spacing; title-case names typed in all lower or upper case."""
    name = ' '.join(str(name).split())
    if name in (name.lower(), name.upper()):
        words = name.lower().split(' ')
        name = ' '.join(word if idx and word in _SMALL_WORDS else word[:1].upper() + word[1:]
                        for idx, word in enumerate(words))
    if name.lower().startswith('the '):
        name = 'The ' + name[4:]
    return name


def join_list(items, conj='and'):
    """['A', 'B', 'C'] -> 'A, B, and C'; people print with their relationship."""
    words = [item.described() if hasattr(item, 'described') else str(item) for item in items]
    if len(words) <= 2:
        return (' %s ' % conj).join(words)
    return '%s, %s %s' % (', '.join(words[:-1]), conj, words[-1])


def relationship_suggestions(spouse1, spouse2):
    """Suggestions for the relationship combobox (printed in parentheses)."""
    first1 = spouse1.name.first
    first2 = spouse2.name.first
    items = [
        "son",
        "daughter",
        "child",
        "grandchild",
        "%s's brother" % first1,
        "%s's sister" % first1,
        "%s's brother" % first2,
        "%s's sister" % first2,
        "niece",
        "nephew",
        "friend",
    ]
    return items


def _clean(text):
    return re.sub(r'\s+', ' ', str(text or '')).strip()


class RLTPerson(Person):
    """A trustee, guardian, executor, or other named person.

    Uses ``name.text`` so that both individuals and institutions (a bank or
    trust company) can be entered in one field.
    """

    def described(self):
        """'Jane Doe (daughter)'; the relationship is optional."""
        rel = _clean(getattr(self, 'relationship', ''))
        if rel:
            return '%s (%s)' % (self.name.text, rel)
        return str(self.name.text)


class Beneficiary(RLTPerson):
    """A residuary beneficiary (person or charity) with a share."""

    def share_text(self, equal, count):
        if equal:
            if count == 1:
                return 'all'
            return 'an equal one-%s share' % _fraction_word(count)
        return pct(self.share)


def _fraction_word(count):
    words = {2: 'half', 3: 'third', 4: 'fourth', 5: 'fifth', 6: 'sixth',
             7: 'seventh', 8: 'eighth', 9: 'ninth', 10: 'tenth'}
    return words.get(int(count), '%sth' % count)


class SpecificGift(DAObject):
    """A specific distribution (cash, an item, or real property)."""

    def subject(self):
        if self.gift_type == 'cash':
            return 'the sum of %s' % money(self.amount)
        if self.gift_type == 'realprop':
            return ("all of the trust's interest in the real property commonly "
                    "known as %s" % _clean(self.description))
        return 'the following property: %s' % _clean(self.description).rstrip('.')

    def recipient(self):
        rel = _clean(getattr(self, 'beneficiary_relationship', ''))
        name = _clean(self.beneficiary_name)
        if rel:
            return '%s (%s)' % (name, rel)
        return name

    def lapse_clause(self, trustor_word='Trustor'):
        if self.is_charity:
            return ('If the beneficiary is not in existence or is not a '
                    'qualified charitable organization when this gift is to be '
                    'distributed, the Trustee shall distribute this gift to one or '
                    'more charitable organizations whose purposes most closely '
                    'match those of the named beneficiary.')
        if self.lapse == 'issue':
            return ('If the beneficiary does not survive to receive this gift, '
                    'the gift shall be distributed to the beneficiary\'s then '
                    'living issue, by right of representation, or, if none, it '
                    'shall lapse and become part of the residue.')
        return ('If the beneficiary does not survive to receive this gift, the '
                'gift shall lapse and become part of the residue.')

    def as_clause(self, trustor_word='Trustor'):
        return '%s to %s. %s' % (self.subject()[0].upper() + self.subject()[1:],
                                 self.recipient(), self.lapse_clause(trustor_word))

    def short(self):
        return '%s to %s' % (self.subject(), _clean(self.beneficiary_name))


class TrustAsset(DAObject):
    """An asset listed on Schedule A, B, or C (or in the funding memo)."""

    def type_label(self):
        for item in ASSET_TYPES:
            if self.asset_type in item:
                return item[self.asset_type]
        return 'Asset'

    def scheduled(self):
        return self.asset_type not in _DESIGNATION_TYPES

    def schedule_text(self):
        text = _clean(self.description).rstrip('.')
        if self.asset_type == 'realprop':
            apn = _clean(getattr(self, 'apn', ''))
            if apn:
                text += ' (Assessor\'s Parcel No. %s)' % apn
        return text

    def funding_step(self, trust_title):
        """Plain-language funding instruction for the summary memo."""
        steps = {
            'realprop': ('Record a trust transfer deed conveying title to the '
                         'Trustees of %s, with a Preliminary Change of Ownership '
                         'Report (BOE-502-A) and the trust-transfer exclusion '
                         'claimed (R&T Code 62(d)).' % trust_title),
            'bank': ('Ask the institution to retitle the account in the name of '
                     'the Trustees (or add a pay-on-death designation to the '
                     'trust). Provide the Certification of Trust.'),
            'brokerage': ('Complete the custodian\'s trust account form and '
                          'retitle the account to the Trustees. Provide the '
                          'Certification of Trust.'),
            'business': ('Prepare an assignment of membership interest or stock '
                         'transfer and update the company records. Review the '
                         'operating or shareholder agreement for transfer '
                         'restrictions and S-corporation eligibility.'),
            'retirement': ('Do NOT retitle. Update the beneficiary designation '
                           '(usually spouse primary; trust or individuals '
                           'contingent) after reviewing SECURE Act payout rules.'),
            'insurance': ('Update the beneficiary designation (often spouse '
                          'primary and the trust contingent). Do not change the '
                          'owner without tax advice.'),
            'vehicle': ('Optional. California DMV transfers are available '
                        'without probate for most vehicles; retitle only if '
                        'desired.'),
            'other': ('Covered by the General Assignment; retitle if the asset '
                      'has a title document.'),
        }
        return steps.get(self.asset_type, steps['other'])

    def character_label(self, spouse1, spouse2):
        if self.character == 's1':
            return 'Separate property of %s' % spouse1
        if self.character == 's2':
            return 'Separate property of %s' % spouse2
        return 'Community property'
