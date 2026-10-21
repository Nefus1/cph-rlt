"""Answer scripts for the headless harness (tests/da_harness.py).

Each scenario maps a question ``id`` to the Python statements the user's
answers would produce. ``i`` is already set by docassemble when a generic
list question is asked.
"""


def _names(prefix, first, middle, last, aka=''):
    return ['%s.name.first = %r' % (prefix, first), '%s.name.middle = %r' % (prefix, middle),
            '%s.name.last = %r' % (prefix, last), '%s.name.suffix = ""' % prefix,
            '%s.aka = %r' % (prefix, aka)]


def _list_collect(var, rows, extra=None):
    """rows: list of dicts of attribute -> python literal source."""
    out = []
    for idx, row in enumerate(rows):
        if idx > 0:
            out.append('%s.appendObject()' % var)
        for attr, val in row.items():
            out.append('%s[%d].%s = %s' % (var, idx, attr, val))
    out.append('%s.there_is_another = False' % var)
    return out


def _checkboxes(var, true_keys, all_keys):
    out = ['%s = DADict(%r, auto_gather=False, gathered=True)' % (var, var)]
    for key in all_keys:
        out.append('%s[%r] = %r' % (var, key, key in true_keys))
    return out


COMMON = {
    'intro': ['intro_seen = True'],
    'spouse1 name': _names('spouse1', 'John', 'Albert', 'Smith'),
    'spouse2 name': _names('spouse2', 'Mary', 'Beth', 'Smith', 'Mary B. Jones'),
    'residence': ['residence.address = "123 Main Street"', 'residence.unit = ""',
                  'residence.city = "Pasadena"', 'residence.state = "CA"',
                  'residence.zip = "91101"', 'residence.county = "Los Angeles County"'],
    'review screen': ['review_done = True'],
}

# ---------------------------------------------------------------- Scenario A
CHILDREN_A = [
    dict(first='Emma', middle='Rose', last='Smith', parentage='joint', living=True, born='2012-03-04'),
    dict(first='Liam', middle='James', last='Smith', parentage='joint', living=True, born='1995-07-21'),
    dict(first='Olivia', middle='', last='Jones', parentage='s2', living=True, born='1990-01-15'),
    dict(first='Noah', middle='', last='Smith', parentage='joint', living=False, issue=True),
]


def child_answers(children):
    def answer(ud):
        c = children[ud['i']]
        out = ['children[i].name.first = %r' % c['first'], 'children[i].name.middle = %r' % c['middle'],
               'children[i].name.last = %r' % c['last'], 'children[i].name.suffix = ""',
               'children[i].parentage = %r' % c['parentage'], 'children[i].is_living = %r' % c['living']]
        if c['living']:
            out.append('children[i].birthdate = as_datetime(%r)' % c['born'])
        else:
            out.append('children[i].left_issue = %r' % c['issue'])
        return out
    return answer


def another(var, total):
    def answer(ud):
        return ['%s.there_is_another = %r' % (var, len(ud[var].elements) < total)]
    return answer


GIFTS_A = [
    ["specific_gifts[i].gift_type = 'cash'", 'specific_gifts[i].amount = 10000.0',
     "specific_gifts[i].beneficiary_name = 'Sarah Lee'", 'specific_gifts[i].is_charity = False',
     "specific_gifts[i].beneficiary_relationship = 'niece'", "specific_gifts[i].timing = 'final'",
     "specific_gifts[i].lapse = 'issue'"],
    ["specific_gifts[i].gift_type = 'property'",
     "specific_gifts[i].description = 'my 1965 Ford Mustang, VIN 5F08C123456'",
     "specific_gifts[i].beneficiary_name = 'Liam James Smith'", 'specific_gifts[i].is_charity = False',
     "specific_gifts[i].beneficiary_relationship = 'son'", "specific_gifts[i].timing = 'spouse1'",
     "specific_gifts[i].lapse = 'residue'"],
    ["specific_gifts[i].gift_type = 'cash'", 'specific_gifts[i].amount = 2500.5',
     "specific_gifts[i].beneficiary_name = 'Pasadena Humane Society & SPCA'",
     'specific_gifts[i].is_charity = True', "specific_gifts[i].timing = 'final'"],
]

ASSETS_A = [
    ["assets[i].asset_type = 'realprop'",
     "assets[i].description = 'Residence at 123 Main Street, Pasadena, California 91101'",
     "assets[i].character = 'cp'", "assets[i].apn = '5730-012-034'", "assets[i].legal_description = ''"],
    ["assets[i].asset_type = 'bank'", "assets[i].description = 'Chase checking account ending in 1234'",
     "assets[i].character = 'cp'"],
    ["assets[i].asset_type = 'retirement'", "assets[i].description = 'Fidelity IRA ending in 9876'",
     "assets[i].character = 's1'"],
    ["assets[i].asset_type = 'brokerage'",
     "assets[i].description = 'Schwab brokerage account ending in 5555 (inheritance)'",
     "assets[i].character = 's2'"],
]


def indexed(items):
    def answer(ud):
        return items[ud['i']]
    return answer


SCENARIO_A = dict(COMMON)
SCENARIO_A.update({
    'restatement': ['is_restatement = False'],
    'marriage': ['marriage_date_known = True', 'marriage_date = as_datetime("2001-06-15")',
                 'union_type = "married"'],
    'children any': ['children.there_are_any = True'],
    'child details': child_answers(CHILDREN_A),
    'children another': another('children', len(CHILDREN_A)),
    'stepchildren': ['stepchildren_equal = True'],
    'omitted any': ['omitted_people.there_are_any = True'],
    'omitted people': _list_collect('omitted_people', [{'name.text': "'Robert Smith'", 'relationship': "'brother'"}]),
    'trust name and date': ['trust_name = default_trust_name', 'trustor_term = "Trustor"',
                            'trust_date_known = False'],
    'initial trustee authority': ['joint_trustee_authority = "either"'],
    'successor trustees': _list_collect('successor_trustees', [
        {'name.text': "'Liam James Smith'", 'relationship': "'son'"},
        {'name.text': "'Olivia Jones'", 'relationship': "'daughter'"}]),
    'successor mode': ['successor_mode = "sequential"'],
    'trustee administration': ['incapacity_physicians = 2', 'trustee_comp = "reasonable"'],
    'plan type': ['plan_type = "disclaimer"'],
    'subtrust terms': ['subtrust_income = "mandatory"'],
    'gifts any': ['specific_gifts.there_are_any = True'],
    'gift details': indexed(GIFTS_A),
    'gifts another': another('specific_gifts', len(GIFTS_A)),
    'pets': ['has_pets = True', 'pet_description = "our dog, Biscuit"', 'pet_caretaker = "Sarah Lee"',
             'pet_alt_caretaker = ""', 'pet_fund = 5000.0'],
    'residue plan': ['residue_plan = "children"'],
    'representation': ['representation = "per_stirpes"'],
    'distribution method': ['dist_method = "staged"', 'stage_count = 3', 'stage_age_1 = 25',
                            'stage_age_2 = 30', 'stage_age_3 = 35'],
    'young beneficiaries': ['young_age = 25', 'has_special_needs = True'],
    'special needs people': _checkboxes('special_needs_people', ['Olivia Jones'],
                                        ['Emma Rose Smith', 'Liam James Smith', 'Olivia Jones',
                                         'Sarah Lee']) + ['special_needs_other = ""'],
    'ultimate plan': ['ultimate_plan = "heirs_split"'],
    'survivorship': ['survivorship_days = 30'],
    'assets any': ['assets.there_are_any = True'],
    'asset details': indexed(ASSETS_A),
    'assets another': another('assets', len(ASSETS_A)),
    'community property presumption': ['cp_presumption = False'],
    'pour over wills': ['include_wills = True', 'executor_same = True'],
    'nominate guardians': ['nominate_guardians = True'],
    'guardians': _list_collect('guardians', [
        {'name.text': "'Sarah Lee'", 'relationship': "'niece'", 'co_guardian': "'David Lee'"},
        {'name.text': "'Olivia Jones'", 'relationship': "''", 'co_guardian': "''"}]),
    'optional provisions': ['include_no_contest = True', 'has_firearms = True',
                            'initials_footer = True', 'include_toc = True'],
    'signing details': ['execution_county = ""', 'tin_mode = "blank"'],
    'preparer': ['preparer_firm = ""', 'preparer_attorney = ""', 'preparer_bar = ""',
                 'preparer_phone = ""', 'preparer_email = ""'],
    'documents wanted': _checkboxes('docs_wanted', ['cert', 'assignment', 'wills', 'summary'],
                                    ['cert', 'assignment', 'wills', 'summary']) + ['want_pdfs = True'],
})

# ---------------------------------------------------------------- Scenario B
SCENARIO_B = dict(COMMON)
SCENARIO_B.update({
    'spouse2 name': _names('spouse2', 'Alex', '', "O'Brien"),
    'restatement': ['is_restatement = True'],
    'original trust': ["original_trust_name = 'The Smith and O\\'Brien Trust'",
                       'original_trust_date = as_datetime("2010-02-01")',
                       "original_amendments = 'First Amendment dated March 3, 2015'"],
    'marriage': ['marriage_date_known = False', 'union_type = "rdp"'],
    'children any': ['children.there_are_any = False'],
    'omitted any': ['omitted_people.there_are_any = False'],
    'trust name and date': ['trust_name = default_trust_name', 'trustor_term = "Settlor"',
                            'trust_date_known = True', 'trust_date = as_datetime("2026-11-02")'],
    'initial trustee authority': ['joint_trustee_authority = "both"'],
    'successor trustees': _list_collect('successor_trustees', [
        {'name.text': "'Pat Rivera'", 'relationship': "'friend'"},
        {'name.text': "'First Republic Trust Company'", 'relationship': "''"}]),
    'successor mode': ['successor_mode = "together"', 'cotrustee_authority = "majority"'],
    'trustee administration': ['incapacity_physicians = 1', 'trustee_comp = "none_individual"'],
    'plan type': ['plan_type = "ab"'],
    'subtrust terms': ['subtrust_income = "discretionary"', 'bypass_five_five = True',
                       'bypass_lpoa = True'],
    'gifts any': ['specific_gifts.there_are_any = False'],
    'pets': ['has_pets = False'],
    'residue plan': ['residue_plan = "custom"'],
    'residuary share method': ['residuary_share_method = "percent"'],
    'residuary beneficiaries percent': _list_collect('residuary', [
        {'name.text': "'Pat Rivera'", 'relationship': "'friend'", 'is_charity': 'False', 'share': '40.0',
         'lapse': "'issue'"},
        {'name.text': "'Chris Rivera'", 'relationship': "'godchild'", 'is_charity': 'False', 'share': '35.0',
         'lapse': "'others'"},
        {'name.text': "'American Red Cross'", 'relationship': "''", 'is_charity': 'True', 'share': '20.0',
         'lapse': "'others'"}]),
    # 95% total -> the verify screen must appear; the "fix" edits a share.
    'verify residuary shares': ['residuary[2].share = 25.0', 'residuary_shares_verified = True'],
    'representation': ['representation = "per_capita"'],
    'distribution method': ['dist_method = "lifetime"', 'lifetime_cotrustee_age = 30',
                            'lifetime_lpoa = True'],
    'young beneficiaries': ['young_age = 21', 'has_special_needs = False'],
    'ultimate plan': ['ultimate_plan = "named"'],
    'ultimate named': ['ultimate_named = "One-half to UCLA Foundation\\nOne-half to the ACLU Foundation of Southern California"'],
    'survivorship': ['survivorship_days = 0'],
    'assets any': ['assets.there_are_any = True'],
    'asset details': indexed([
        ["assets[i].asset_type = 'realprop'",
         "assets[i].description = '456 Ocean Avenue, Santa Monica, California 90402'",
         "assets[i].character = 'cp'", "assets[i].apn = ''",
         "assets[i].legal_description = 'Lot 12 of Tract 3456, in the City of Santa Monica,\\nas per map recorded in Book 45, Page 6 of Maps.'"]]),
    'assets another': another('assets', 1),
    'community property presumption': ['cp_presumption = True'],
    'pour over wills': ['include_wills = False'],
    'optional provisions': ['include_no_contest = False', 'has_firearms = False',
                            'initials_footer = False', 'include_toc = True'],
    'signing details': ['execution_county = "Los Angeles"', 'tin_mode = "enter"',
                        'trust_tin = "XXX-XX-1234"'],
    'preparer': ['preparer_firm = "Example Law, APC"', 'preparer_attorney = "Jordan Example"',
                 'preparer_bar = "123456"', 'preparer_phone = "(555) 555-0100"',
                 'preparer_email = "jordan@example.com"'],
    'documents wanted': _checkboxes('docs_wanted', ['cert', 'assignment', 'summary'],
                                    ['cert', 'assignment', 'summary']) + ['want_pdfs = False'],
})

# ---------------------------------------------------------------- Scenario C
CHILDREN_C = [
    dict(first='Ava', middle='', last='Smith', parentage='joint', living=True, born='1998-05-05'),
    dict(first='Ben', middle='', last='Smith', parentage='joint', living=True, born='2000-09-09'),
]
SCENARIO_C = dict(COMMON)
SCENARIO_C.update({
    'restatement': ['is_restatement = False'],
    'marriage': ['marriage_date_known = False', 'union_type = "married"'],
    'children any': ['children.there_are_any = True'],
    'child details': child_answers(CHILDREN_C),
    'children another': another('children', len(CHILDREN_C)),
    'omitted any': ['omitted_people.there_are_any = False'],
    'trust name and date': ['trust_name = "the smith family trust"', 'trustor_term = "Trustor"',
                            'trust_date_known = False'],
    'initial trustee authority': ['joint_trustee_authority = "either"'],
    'successor trustees': _list_collect('successor_trustees', [{'name.text': "'Ava Smith'", 'relationship': "'daughter'"}]),
    'trustee administration': ['incapacity_physicians = 2', 'trustee_comp = "reasonable"'],
    'plan type': ['plan_type = "survivor"'],
    'gifts any': ['specific_gifts.there_are_any = False'],
    'pets': ['has_pets = False'],
    'residue plan': ['residue_plan = "children"'],
    'representation': ['representation = "per_stirpes"'],
    'distribution method': ['dist_method = "outright"'],
    'young beneficiaries': ['young_age = 25', 'has_special_needs = False'],
    'ultimate plan': ['ultimate_plan = "heirs"'],
    'survivorship': ['survivorship_days = 30'],
    'assets any': ['assets.there_are_any = False'],
    'community property presumption': ['cp_presumption = False'],
    'pour over wills': ['include_wills = True', 'executor_same = False'],
    'executors': _list_collect('executors', [{'name.text': "'Ben Smith'", 'relationship': "'son'"}]),
    'optional provisions': ['include_no_contest = True', 'has_firearms = False',
                            'initials_footer = False', 'include_toc = False'],
    'signing details': ['execution_county = "Orange"', 'tin_mode = "blank"'],
    'preparer': ['preparer_firm = "Example Law, APC"', 'preparer_attorney = ""', 'preparer_bar = ""',
                 'preparer_phone = ""', 'preparer_email = ""'],
    'documents wanted': _checkboxes('docs_wanted', ['wills', 'summary'],
                                    ['cert', 'assignment', 'wills', 'summary']) + ['want_pdfs = False'],
})

SCENARIO_A['_edit_after_final'] = True

SCENARIOS = {'a': SCENARIO_A, 'b': SCENARIO_B, 'c': SCENARIO_C}
