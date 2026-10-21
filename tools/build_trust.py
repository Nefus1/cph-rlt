"""Joint Revocable Living Trust Agreement template (joint_rlt_trust.docx)."""

from docbuilder import Builder
from common import X, TRUSTID, DATE, DATED


def build(path):
    raw = Builder(numbered=True)
    b = X(raw)

    raw.footer('{{ trust_title }}, ' + DATED,
               initials='{% if initials_footer %}          Initials: ________   ________{% endif %}')

    # ------------------------------------------------------------ cover
    b.para('', 'Normal', after=96)
    b.title('{{ trust_title | upper }}')
    b.subtitle('A Joint Revocable Living Trust')
    b.center('{% if is_restatement %}Originally dated {{ original_dated }}<br>Amended and Restated in its Entirety on @DATE@'
             '{% else %}Dated @DATE@{% endif %}', after=36)
    b.center('<b>{{ s1_name | upper }}</b> and <b>{{ s2_name | upper }}</b>', after=0)
    b.center('@Ts@ and Trustees', after=60)
    b.ctl('{%p if include_toc %}')
    b.para('TABLE OF CONTENTS', 'Center Bold', after=12)
    b.ctl('{%p for a in article_contents %}')
    b.para('Article {{ a["num"] }}<tab>{{ a["title"] }}', 'Contents Line')
    b.ctl('{%p endfor %}')
    b.ctl('{%p endif %}')
    raw.page_break()

    # ------------------------------------------------------------ preamble
    b.title('{{ trust_title | upper }}')
    b.subtitle('Joint Revocable Living Trust Agreement')
    b.plain('This Trust Agreement is made on @DATE@, by <b>{{ s1_name | upper }}</b> and '
            '<b>{{ s2_name | upper }}</b>, residents of {{ county_name }} County, California, as '
            '@Ts@ (together, the "@Ts@," and each, a "@T@"), and {{ s1_name | upper }} and '
            '{{ s2_name | upper }}, as the initial trustees (together with every successor, the '
            '"Trustee").')
    b.ctl('{%p if is_restatement %}')
    b.plain('<b>Restatement.</b> The @Ts@ established {{ original_trust_name }} by a trust agreement '
            'dated {{ original_dated }}{% if original_amendments %} (as amended by '
            '{{ original_amendments | replace("\\n", "; ") }}){% endif %} (the "Original Trust '
            'Agreement"). Exercising the power to amend reserved in the Original Trust Agreement, '
            'the @Ts@ amend and restate the Original Trust Agreement in its entirety, effective '
            'on the date of this instrument. This restatement does not create a new trust. The '
            'trust continues without interruption, all property held under the Original Trust '
            'Agreement remains trust property, and every prior transfer, title, and beneficiary '
            'designation in favor of the trust remains effective.')
    b.ctl('{%p endif %}')

    # ============================================================ ARTICLE 1
    b.article('{{ art_title["establishment"] }}')
    b.section('Name of the Trust',
              'This trust shall be known as <b>{{ trust_title }}</b>, ' + DATED + '. Title to '
              'trust property may be taken in the name of "{{ s1_name }} and {{ s2_name }}, '
              'Trustees of @TRUSTID@," or in the name of any then acting Trustee in that '
              'capacity, and any reference to the trust in that or a substantially similar '
              'form shall be effective.')
    b.section('Declaration of Trust',
              'The @Ts@ transfer to the Trustee, and the Trustee accepts and agrees to hold, '
              'the property described on the attached Schedules A, B, and C, together with all '
              'property later added to the trust (the "Trust Estate"), in trust, to be '
              'administered and distributed as provided in this instrument.')
    b.section('Revocable Grantor Trust',
              'While both @Ts@ are living, this trust is revocable as provided in Article '
              '@ART:rights@. Each @T@ intends to be treated as the owner of that @T@\'s share of '
              'the trust for federal and California income tax purposes under Sections 671 '
              'through 677 of the Internal Revenue Code, and the Trustee may report trust income '
              'under the Social Security number of either @T@ as permitted by Treasury '
              'Regulations Section 1.671-4.')
    b.section('Purposes',
              'The @Ts@ create this trust to manage their property during their lifetimes, to '
              'provide for each of them during any period of incapacity, to avoid probate and '
              'conservatorship proceedings, and to provide for the orderly transfer of their '
              'property at death.')
    b.section('Effective Date',
              'This instrument takes effect when signed by the @Ts@, whether or not any property '
              'has then been transferred to the Trustee.')

    # ============================================================ ARTICLE 2
    b.article('{{ art_title["family"] }}')
    b.section('Marriage',
              '{% if union_type == "rdp" %}The @Ts@ are registered domestic partners of each '
              'other{% if marriage_date_known %}, having registered on {{ format_date(marriage_date, '
              'format="MMMM d, yyyy") }}{% endif %}. Under Family Code Section 297.5, every '
              'reference in this instrument to a spouse, marriage, or community property includes '
              'a registered domestic partner, a registered domestic partnership, and the community '
              'property of registered domestic partners.{% else %}The @Ts@ are married to each '
              'other{% if marriage_date_known %} and were married on {{ format_date(marriage_date, '
              'format="MMMM d, yyyy") }}{% endif %}.{% endif %}')
    b.ctl('{%p if children | length %}')
    b.section('Children',
              'The @Ts@ have {{ "the following child" if children | length == 1 else "the following children" }}:')
    b.ctl('{%p for c in children %}')
    b.sub('<b>{{ c.name.full(middle="full") }}</b>{% if c.parentage == "s1" %}, the child of '
          '{{ s1_name }}{% elif c.parentage == "s2" %}, the child of {{ s2_name }}{% else %}{% endif %}'
          '{% if c.is_living %}, born {{ format_date(c.birthdate, format="MMMM d, yyyy") }}'
          '{% else %}, who is deceased{% if c.left_issue %} and is survived by issue{% endif %}'
          '{% endif %}.')
    b.ctl('{%p endfor %}')
    b.ctl('{%p if any_stepchildren %}')
    b.ctl('{%p if stepchildren_equal %}')
    b.body('Each child named above who is the child of only one @T@, and the issue of that child, '
           'shall be treated for every purpose of this instrument as a child and issue of both @Ts@.')
    b.ctl('{%p else %}')
    b.body('A child named above as the child of only one @T@ is a beneficiary wherever this '
           'instrument provides for the @Ts@\' children, but for every other purpose (including '
           'gifts to the issue of a @T@) that child and that child\'s issue are treated as the '
           'child and issue of that child\'s parent only.')
    b.ctl('{%p endif %}')
    b.ctl('{%p endif %}')
    b.ctl('{%p else %}')
    b.section('Children', 'The @Ts@ have no children now living or deceased.')
    b.ctl('{%p endif %}')
    b.section('Later Children',
              'References to the children of the @Ts@ include any child later born to or adopted '
              'by the @Ts@ together. A person adopted before reaching age eighteen is treated as '
              'a child of the adopting parent.')
    b.section('Intentional Omission',
              'Except as otherwise provided in this instrument, the @Ts@ have intentionally, and '
              'with full knowledge, omitted to provide for any of their heirs, including any '
              'person who claims to be a child or spouse of either @T@.'
              '{% if omitted_people | length %} Without limiting the preceding sentence, the @Ts@ '
              'intentionally make no provision for {{ join_list(omitted_people, "or") }}.{% endif %}')

    # ============================================================ ARTICLE 3
    b.article('{{ art_title["property"] }}')
    b.section('Trust Estate',
              'The Trust Estate consists of the property listed on the Schedules, the property '
              'transferred by the @Ts@\' General Assignment of even date, and all other property '
              'later transferred to the Trustee by either @T@ or by any other person, by lifetime '
              'transfer, will, beneficiary designation, or otherwise, with the Trustee\'s consent.')
    b.section('Community Property',
              'Property transferred to the trust as community property, and its proceeds and '
              'income, shall remain the community property of the @Ts@ while both are living, '
              'as provided in Family Code Section 761. Property described on Schedule A is the '
              'community property of the @Ts@. For purposes of this instrument, quasi-community '
              'property is treated as community property.')
    b.section('Separate Property',
              'Property transferred to the trust as the separate property of a @T@, and its '
              'proceeds and income, shall remain the separate property of that @T@. Property '
              'described on Schedule B is the separate property of {{ s1_name }}, and property '
              'described on Schedule C is the separate property of {{ s2_name }}. The Trustee '
              'shall maintain records sufficient to identify the character of all trust property.')
    b.section('Effect on Character',
              'Except as provided in this Article, neither the transfer of property to the trust '
              'nor the way property is titled or listed shall change its character as community '
              'or separate property. The @Ts@ may change the character of property only by a '
              'written agreement that satisfies Family Code Section 852.')
    b.ctl('{%p if cp_presumption %}')
    b.section('Community Property Agreement',
              'The @Ts@ expressly agree and declare that all property now or later held in this '
              'trust, other than property listed on Schedule B or Schedule C or later designated '
              'in a writing signed by both @Ts@ as the separate property of one of them, is the '
              'community property of the @Ts@. Each @T@ understands that this agreement may '
              'change the character of property that would otherwise be that @T@\'s separate '
              'property, that it is intended as a transmutation under Family Code Section 852, '
              'and that each @T@ has had the opportunity to consult independent counsel before '
              'signing.')
    b.ctl('{%p endif %}')
    b.section('Property Held Under Other Names',
              'Any property titled in the name of a @T@ under a variation of that @T@\'s name'
              '{% if spouse1.aka or spouse2.aka %}, including '
              '{% if spouse1.aka %}"{{ spouse1.aka }}" for {{ s1_name }}{% endif %}'
              '{% if spouse1.aka and spouse2.aka %} and {% endif %}'
              '{% if spouse2.aka %}"{{ spouse2.aka }}" for {{ s2_name }}{% endif %},{% endif %} '
              'that the @Ts@ intend to be held in this trust is trust property.')
    b.section('Retirement Plans and Life Insurance',
              'Interests in retirement plans, individual retirement accounts, annuities, and '
              'life insurance are not transferred to the trust by this instrument or by the '
              'General Assignment. They pass according to their beneficiary designations, which '
              'may name the Trustee.')
    b.section('Additions',
              'Any person may add property acceptable to the Trustee to the trust by lifetime '
              'transfer, will, beneficiary designation, or otherwise. Property added by reason of '
              'the death of a @T@ shall be administered as part of that @T@\'s share.')

    # ============================================================ ARTICLE 4
    b.article('{{ art_title["rights"] }}')
    b.section('Income and Principal During Joint Lifetimes',
              'While both @Ts@ are living, the Trustee shall pay to or apply for the benefit of '
              'the @Ts@ as much of the net income and principal of the community property as '
              'either @T@ requests, and to or for the benefit of each @T@ as much of the net '
              'income and principal of that @T@\'s separate property as that @T@ requests. '
              'Absent a request, the Trustee shall distribute or accumulate income and principal '
              'as the Trustee considers advisable for the @Ts@\' health, support, and comfort.')
    b.section('Revocation',
              'While both @Ts@ are living: (a) either @T@ may revoke this trust as to community '
              'property, in which case the Trustee shall promptly deliver that property to the '
              '@Ts@ as their community property; and (b) a @T@ may revoke this trust as to that '
              '@T@\'s separate property, in which case the Trustee shall promptly deliver that '
              'property to that @T@. A revocation is made by a signed writing delivered to the '
              'other @T@ and to the Trustee.')
    b.section('Amendment',
              'While both @Ts@ are living, this instrument may be amended only by a writing '
              'signed by both @Ts@ and delivered to the Trustee, except that a @T@ alone may '
              'amend the provisions governing that @T@\'s separate property in a manner that '
              'does not affect the other @T@\'s interests.')
    b.section('After the Death of a @T@',
              'After the death of the first @T@ to die, the Surviving @T@ may amend, revoke, or '
              'terminate the Survivor\'s Trust in whole or in part, and may withdraw any of its '
              'property. {% if plan_type == "survivor" %}Because the Deceased @T@\'s share is '
              'added to the Survivor\'s Trust, the Surviving @T@ will hold these powers over the '
              'entire Trust Estate.{% else %}The @SUB@ shall be irrevocable, and the Surviving @T@ '
              'may not amend, revoke, or terminate it.{% endif %} After the death of both @Ts@, '
              'this instrument may not be amended or revoked.')
    b.section('Exclusive Method; Personal Powers',
              'The methods of revocation and amendment stated in this Article are exclusive. The '
              'powers to revoke and amend are personal to each @T@ and may not be exercised by a '
              'conservator or other legal representative. An agent acting under a durable power '
              'of attorney may exercise these powers only to the extent the power of attorney '
              'expressly authorizes it, as provided in Probate Code Section 4264.')
    b.section('Residence',
              'Each @T@ retains the right to possess and occupy, for life and rent free, any '
              'residence held in the trust. The @Ts@ intend this right to preserve their '
              'eligibility for the homeowners\' property tax exemption, the exclusion of gain '
              'under Section 121 of the Internal Revenue Code, and the trust-transfer exclusion '
              'from reassessment under Revenue and Taxation Code Section 62(d).')

    # ============================================================ ARTICLE 5
    b.article('{{ art_title["trustees"] }}')
    b.section('Initial Trustees',
              'The @Ts@, {{ s1_name }} and {{ s2_name }}, are the initial Trustees. While both '
              'serve, {% if joint_trustee_authority == "either" %}either of them acting alone may '
              'exercise any power of the Trustee, and any person may rely on the signature of '
              'either Trustee alone{% else %}they shall act jointly, and both signatures are '
              'required to exercise any power of the Trustee, except that either may delegate any '
              'power to the other in a signed writing{% endif %}.')
    b.section('Surviving or Remaining @T@',
              'If either @T@ dies, resigns, or becomes incapacitated, the other @T@ shall serve '
              'as sole Trustee.')
    b.section('Successor Trustees',
              'If both @Ts@ have died, resigned, or become incapacitated, '
              '{% if successor_trustees | length == 1 %}{{ successor_trustees[0].described() }} '
              'shall serve as successor Trustee.'
              '{% elif successor_mode == "together" %}the following shall serve together as '
              'co-Trustees: {{ join_list(successor_trustees) }}. '
              'If any of them fails or ceases to serve, the others shall continue to serve. While '
              'more than one co-Trustee serves, {% if cotrustee_authority == "independently" %}any '
              'one co-Trustee acting alone may exercise any power of the Trustee{% elif '
              'cotrustee_authority == "majority" %}the co-Trustees shall act by majority, and if '
              'only two serve they shall act jointly{% else %}the co-Trustees shall act '
              'unanimously{% endif %}.'
              '{% else %}the following shall serve as successor Trustee, one at a time, in the '
              'order listed:{% endif %}')
    b.ctl('{%p if successor_trustees | length > 1 and successor_mode != "together" %}')
    b.ctl('{%p for t in successor_trustees %}')
    b.sub('{{ t.described() }}{% if loop.last %}.{% else %};{% endif %}')
    b.ctl('{%p endfor %}')
    b.body('A successor listed later serves only if each successor listed earlier has died, '
           'resigned, become incapacitated, or declined to serve.')
    b.ctl('{%p endif %}')
    b.section('Vacancy',
              'If no named successor is able and willing to serve, the last serving Trustee may '
              'appoint a successor in a signed writing. Failing that appointment, a majority of '
              'the adult beneficiaries then entitled to receive income (with the parent or '
              'guardian acting for any minor or incapacitated beneficiary) may appoint an '
              'individual or a bank or trust company as successor Trustee. If no successor is '
              'appointed within sixty days, any interested person may petition the court to '
              'appoint one under Probate Code Section 15660.')
    b.section('Resignation',
              'A Trustee may resign by giving at least thirty days\' written notice to the @Ts@, '
              'if living, and otherwise to the co-Trustee (if any), the next successor Trustee, '
              'and the adult beneficiaries then entitled to receive income, as provided in '
              'Probate Code Section 15640.')
    b.section('Removal',
              'While living and not incapacitated, the @Ts@ (or the Surviving @T@) may remove any '
              'Trustee by a signed writing delivered to that Trustee. After the death of both '
              '@Ts@, a majority of the adult beneficiaries then entitled to receive income may '
              'remove any bank or trust company serving as Trustee and replace it with another '
              'bank or trust company. Nothing in this Section limits the court\'s power to remove '
              'a Trustee.')
    b.section('Bond',
              'No bond shall be required of any Trustee named or appointed under this instrument.')
    b.section('Compensation',
              '{% if trustee_comp == "reasonable" %}Each Trustee is entitled to reasonable '
              'compensation for services rendered. A bank or trust company may be compensated '
              'according to its published fee schedule.{% else %}An individual Trustee shall serve '
              'without compensation. A bank, trust company, or professional fiduciary serving as '
              'Trustee may be compensated according to its published fee schedule or, if none, '
              'reasonably.{% endif %} Every Trustee shall be reimbursed for reasonable expenses '
              'properly incurred in administering the trust.')
    b.section('Liability of Successor Trustees',
              'A successor Trustee has no duty to examine the accounts or actions of a prior '
              'Trustee and is not liable for any act or omission of a prior Trustee. An '
              'individual Trustee who acts in good faith is not liable for any loss to the trust, '
              'except a loss caused by that Trustee\'s gross negligence, willful misconduct, or bad '
              'faith, subject to Probate Code Section 16461.')
    b.section('Certification of Trust',
              'Any Trustee may furnish a certification of trust under Probate Code Section '
              '18100.5, and any person may rely on it without seeing this instrument.')

    # ============================================================ ARTICLE 6
    b.article('{{ art_title["incapacity"] }}')
    b.section('Determination of Incapacity',
              'A @T@ or an individual Trustee is incapacitated if any of the following occurs:')
    b.sub('{% if incapacity_physicians == 1 %}one licensed physician{% else %}two licensed physicians{% endif %} '
          'who {% if incapacity_physicians == 1 %}has{% else %}have{% endif %} examined the person '
          '{% if incapacity_physicians == 1 %}certifies{% else %}certify{% endif %} in writing that the '
          'person is unable to manage the person\'s own financial affairs or to administer the trust '
          'prudently;')
    b.sub('a court of competent jurisdiction determines that the person lacks the capacity to '
          'manage the person\'s financial resources or to serve as trustee; or')
    b.sub('the person has disappeared, or is held against the person\'s will, for more than thirty '
          'consecutive days.')
    b.body('A person regains capacity in the same manner, by a written physician certificate or a '
           'court determination. Any third party may rely on a certificate delivered under this '
           'Section without further inquiry.')
    b.section('Authorization to Release Health Information',
              'Each @T@ and each individual Trustee authorizes every physician, health care '
              'provider, and health plan to disclose to any successor Trustee named in this '
              'instrument the individually identifiable health information needed to determine '
              'that person\'s capacity. This authorization is intended to comply with the federal '
              'Health Insurance Portability and Accountability Act (45 C.F.R. Section 164.508) and '
              'the California Confidentiality of Medical Information Act (Civil Code Section '
              '56.11), and it remains effective until two years after the death of the person '
              'giving it.')
    b.section('Administration During Incapacity',
              'While a @T@ is incapacitated, the Trustee shall pay to or apply for the benefit of '
              'that @T@, the other @T@, and any person dependent on them, as much of the income and '
              'principal of the trust (using first that @T@\'s share of community property and '
              'separate property) as the Trustee considers necessary for their health, support, and '
              'maintenance in their accustomed manner of living. The @Ts@ prefer to remain in '
              'their home, and the Trustee shall pay for in-home care when reasonably possible. '
              'The powers of revocation and amendment of an incapacitated @T@ are suspended during '
              'the incapacity.')

    # ============================================================ ARTICLE 7
    b.article('{{ art_title["first_death"] }}')
    b.section('Definitions',
              'The "Deceased @T@" is the first @T@ to die, and the "Surviving @T@" is the other '
              '@T@. If the @Ts@ die under circumstances in which the order of their deaths cannot '
              'be established by clear and convincing evidence, each @T@ shall be treated as having '
              'survived the other for purposes of that @T@\'s share of community property and '
              'separate property, as provided in Probate Code Sections 103 and 220.')
    b.section('Payment of Expenses',
              'On the death of the Deceased @T@, the Trustee may pay from the Deceased @T@\'s '
              'Share (defined below) the Deceased @T@\'s legally enforceable debts (other than '
              'debts secured by real or personal property, which need not be paid before they are '
              'due), last illness and funeral expenses, expenses of administration, and any estate '
              'or inheritance taxes attributable to the Deceased @T@\'s Share, except to the extent '
              'they are paid from other sources.')
    b.ctl('{%p if gifts_s1 | length or gifts_s2 | length %}')
    b.section('Specific Gifts at the First Death',
              'The Trustee shall distribute the following gifts from the Deceased @T@\'s Share:')
    b.ctl('{%p if gifts_s1 | length %}')
    b.sub('If {{ s1_name }} is the Deceased @T@: {% for g in gifts_s1 %}{{ g.as_clause(T) }}'
          '{% if not loop.last %} {% endif %}{% endfor %}')
    b.ctl('{%p endif %}')
    b.ctl('{%p if gifts_s2 | length %}')
    b.sub('If {{ s2_name }} is the Deceased @T@: {% for g in gifts_s2 %}{{ g.as_clause(T) }}'
          '{% if not loop.last %} {% endif %}{% endfor %}')
    b.ctl('{%p endif %}')
    b.body('A gift designated for the death of a @T@ who is instead the Surviving @T@ shall be made '
           'at the Surviving @T@\'s death as provided in Article @ART:final@.')
    b.ctl('{%p endif %}')
    b.section('Division of the Trust Estate',
              'After the death of the Deceased @T@, the Trustee shall divide the Trust Estate, '
              'including any property added by reason of the Deceased @T@\'s death, into two '
              'shares:')
    b.sub('the "Survivor\'s Share," consisting of the Surviving @T@\'s interest in the community '
          'property and the Surviving @T@\'s separate property; and')
    b.sub('the "Deceased @T@\'s Share," consisting of the Deceased @T@\'s interest in the '
          'community property and the Deceased @T@\'s separate property.')
    b.body('The Trustee may divide community property on a non-pro-rata basis, allocating whole '
           'assets to either share, so long as each share receives property of equal aggregate '
           'value. The Survivor\'s Share shall be held as the "Survivor\'s Trust" under Article '
           '@ART:survivors_trust@.')
    b.ctl('{%p if plan_type == "survivor" %}')
    b.section('Disposition of the Deceased @T@\'s Share',
              'The Trustee shall add the balance of the Deceased @T@\'s Share to the Survivor\'s '
              'Trust. Any portion that the Surviving @T@ (or the Surviving @T@\'s legal '
              'representative) disclaims shall instead be distributed under Article @ART:final@ as '
              'though the Surviving @T@ had predeceased the Deceased @T@.')
    b.ctl('{%p elif plan_type == "disclaimer" %}')
    b.section('Disposition of the Deceased @T@\'s Share',
              'The Trustee shall add the balance of the Deceased @T@\'s Share to the Survivor\'s '
              'Trust, except that any portion of it (or of any interest in it) that the Surviving '
              '@T@, or the Surviving @T@\'s legal representative, effectively disclaims shall be '
              'held as the "@SUB@" under Article @ART:subtrust@.')
    b.section('Disclaimer',
              'The Surviving @T@ may disclaim all or any portion of the Deceased @T@\'s Share, '
              'including a fractional or pecuniary portion defined by formula, by a written '
              'disclaimer that satisfies Section 2518 of the Internal Revenue Code and Probate Code '
              'Sections 275 through 295 (generally within nine months after the Deceased @T@\'s '
              'death and before accepting any benefit of the disclaimed property). The Surviving '
              '@T@ may serve as Trustee of the @SUB@.')
    b.ctl('{%p else %}')
    b.section('Disposition of the Deceased @T@\'s Share',
              'The Trustee shall allocate to the "@SUB@," to be held under Article @ART:subtrust@, '
              'the Bypass Amount, and shall add the balance of the Deceased @T@\'s Share, if any, '
              'to the Survivor\'s Trust.')
    b.section('Bypass Amount',
              'The "Bypass Amount" is the largest amount, if any, that can pass free of federal '
              'estate tax by reason of the applicable exclusion amount available to the Deceased '
              '@T@\'s estate under Section 2010 of the Internal Revenue Code (not including any '
              'deceased spousal unused exclusion amount), after taking into account all other '
              'property passing on account of the Deceased @T@\'s death that does not qualify for '
              'the marital or charitable deduction, adjusted taxable gifts, and charges to principal '
              'that are not allowed as estate tax deductions. If the Deceased @T@\'s Share is equal '
              'to or less than the Bypass Amount, the entire Deceased @T@\'s Share shall be '
              'allocated to the @SUB@. The Trustee shall value assets at their values on the date '
              'or dates of allocation, and shall select assets that fairly represent appreciation '
              'and depreciation.')
    b.section('Disclaimer by the Surviving @T@',
              'Any portion of the Deceased @T@\'s Share passing to the Survivor\'s Trust that the '
              'Surviving @T@ effectively disclaims shall be added to the @SUB@ but held as a separate '
              'share over which the Surviving @T@ has no power of appointment or withdrawal right.')
    b.ctl('{%p endif %}')
    b.section('Portability Election',
              'The Trustee (or the Deceased @T@\'s executor) shall timely file a federal estate tax '
              'return electing portability of the Deceased @T@\'s unused exclusion amount under '
              'Section 2010(c)(5)(A) of the Internal Revenue Code, unless the Surviving @T@ directs '
              'otherwise in writing. The cost of the return shall be paid from the Survivor\'s Trust '
              'unless the Trustee determines that another allocation is fairer.')
    b.section('Tax Identification and Records',
              'After the Deceased @T@\'s death, the Trustee shall keep separate records for each '
              'trust and shall obtain a taxpayer identification number for any trust that becomes '
              'irrevocable. The Trustee may hold the trusts as a common fund for investment.')

    # ============================================================ ARTICLE 8 (optional)
    b.ctl('{%p if plan_type in ("ab", "disclaimer") %}')
    b.article('{{ art_title["subtrust"] }}')
    b.section('Irrevocability',
              'The @SUB@ is irrevocable and may not be amended by the Surviving @T@ or any other '
              'person.')
    b.section('Income',
              '{% if subtrust_income == "mandatory" %}During the Surviving @T@\'s lifetime, the '
              'Trustee shall pay to the Surviving @T@ the entire net income of the @SUB@ in '
              'convenient installments, at least quarterly.{% else %}During the Surviving @T@\'s '
              'lifetime, the Trustee may pay to or apply for the benefit of the Surviving @T@ as '
              'much of the net income of the @SUB@ as the Trustee considers necessary for the '
              'Surviving @T@\'s health, education, maintenance, and support, adding any '
              'undistributed income to principal.{% endif %}')
    b.section('Principal',
              'The Trustee may also pay to or apply for the benefit of the Surviving @T@ as much of '
              'the principal of the @SUB@ as the Trustee considers necessary for the Surviving '
              '@T@\'s health, education, maintenance, and support in the Surviving @T@\'s accustomed '
              'manner of living. In exercising this discretion, the Trustee may consider other '
              'income and resources known to the Trustee to be reasonably available to the '
              'Surviving @T@, and the @Ts@ intend that the Survivor\'s Trust be used first.')
    b.ctl('{%p if plan_type == "ab" and bypass_five_five %}')
    b.section('Annual Withdrawal Right',
              'In addition, in each calendar year the Surviving @T@ may withdraw from the principal '
              'of the @SUB@ (other than any separate share held for disclaimed property) an amount '
              'not exceeding the greater of five thousand dollars ($5,000) or five percent (5%) of '
              'the value of that principal on the last day of the year. This right is noncumulative, '
              'lapses at the end of each calendar year to the extent not exercised, and may be '
              'exercised only by a signed writing delivered to the Trustee.')
    b.ctl('{%p endif %}')
    b.ctl('{%p if plan_type == "ab" and bypass_lpoa %}')
    b.section('Limited Power of Appointment',
              'On the Surviving @T@\'s death, the Trustee shall distribute the remaining principal '
              'and undistributed income of the @SUB@ (other than any separate share held for '
              'disclaimed property) to such one or more of the issue of the @Ts@ and organizations '
              'described in Section 2055(a) of the Internal Revenue Code, outright or in further '
              'trust, as the Surviving @T@ appoints by a will, codicil, or signed writing delivered '
              'to the Trustee during the Surviving @T@\'s lifetime that specifically refers to this '
              'power. The Surviving @T@ may not appoint to the Surviving @T@, the Surviving @T@\'s '
              'estate, the Surviving @T@\'s creditors, or the creditors of the Surviving @T@\'s '
              'estate.')
    b.ctl('{%p endif %}')
    b.ctl('{%p if plan_type == "disclaimer" %}')
    b.section('Restrictions Required for a Qualified Disclaimer',
              'The Surviving @T@ shall have no power of appointment over the @SUB@ and no power to '
              'direct the beneficial enjoyment of its property, except a power limited by the '
              'standard of health, education, maintenance, and support. If the Surviving @T@ also '
              'disclaims an interest in the @SUB@, the disclaimed interest shall pass as though the '
              'Surviving @T@ had predeceased the Deceased @T@.')
    b.ctl('{%p endif %}')
    b.section('Residence',
              'If a residence is held in the @SUB@, the Surviving @T@ may occupy it rent free for '
              'life. The Trustee may pay its taxes, insurance, and major repairs from the @SUB@, and '
              'may sell it and buy a replacement residence at the Surviving @T@\'s request.')
    b.section('Surviving @T@ as Trustee',
              'When the Surviving @T@ serves as Trustee of the @SUB@, the Surviving @T@ may make '
              'discretionary distributions to the Surviving @T@ only for health, education, '
              'maintenance, and support, and may not participate in any decision to make a '
              'distribution that would discharge the Surviving @T@\'s legal obligation of support. '
              'The Surviving @T@ may appoint an independent co-Trustee to exercise any discretion '
              'that the Surviving @T@ cannot exercise.')
    b.section('Distribution on the Surviving @T@\'s Death',
              'On the Surviving @T@\'s death, the Trustee shall distribute any undistributed income '
              'to the Survivor\'s Trust, and shall distribute the remaining principal of the @SUB@ '
              '{% if plan_type == "ab" and bypass_lpoa %}(to the extent not effectively appointed) {% endif %}'
              'as provided in Article @ART:final@. No '
              'estate tax, debt, or expense of the Surviving @T@ shall be paid from the @SUB@.')
    b.ctl('{%p endif %}')

    # ============================================================ SURVIVOR'S TRUST
    b.article('{{ art_title["survivors_trust"] }}')
    b.section('Revocable Trust for the Surviving @T@',
              'The Survivor\'s Trust remains fully revocable and amendable by the Surviving @T@ '
              'as provided in Article @ART:rights@.')
    b.section('Income and Principal',
              'During the Surviving @T@\'s lifetime, the Trustee shall pay to or apply for the '
              'benefit of the Surviving @T@ the entire net income of the Survivor\'s Trust, at '
              'least quarterly, and as much of its principal as the Surviving @T@ requests or as '
              'the Trustee considers advisable for the Surviving @T@\'s health, support, '
              'maintenance, and comfort.')
    b.section('General Power of Appointment',
              'On the Surviving @T@\'s death, the Trustee shall distribute the remaining property '
              'of the Survivor\'s Trust to such persons or entities, including the Surviving @T@\'s '
              'estate or the creditors of the Surviving @T@\'s estate, as the Surviving @T@ '
              'appoints by a will, codicil, or signed writing delivered to the Trustee that '
              'specifically refers to this power.')
    b.section('Expenses at the Surviving @T@\'s Death',
              'On the Surviving @T@\'s death, the Trustee may pay from the Survivor\'s Trust the '
              'Surviving @T@\'s legally enforceable debts, last illness and funeral expenses, '
              'expenses of administration, and all estate and inheritance taxes payable by reason '
              'of the Surviving @T@\'s death on property passing under this instrument.')
    b.section('Unappointed Property',
              'The Trustee shall distribute any property of the Survivor\'s Trust not effectively '
              'appointed as provided in Article @ART:final@.')

    # ============================================================ FINAL DISTRIBUTION
    b.article('{{ art_title["final"] }}')
    b.section('Remaining Trust Estate',
              'On the death of the Surviving @T@, the property of every trust under this instrument '
              'that is directed to be distributed under this Article (the "Remaining Trust Estate") '
              'shall be distributed as provided below.')
    b.ctl('{%p if gifts_final | length or gifts_s1 | length or gifts_s2 | length %}')
    b.section('Specific Gifts',
              'The Trustee shall first make the following gifts, each free of estate tax and '
              'subject to Article @ART:beneficiary_trusts@:')
    b.ctl('{%p for g in gifts_final %}')
    b.sub('{{ g.as_clause(T) }}')
    b.ctl('{%p endfor %}')
    b.ctl('{%p if gifts_s1 | length %}')
    b.sub('If {{ s1_name }} is the Surviving @T@: {% for g in gifts_s1 %}{{ g.as_clause(T) }}'
          '{% if not loop.last %} {% endif %}{% endfor %}')
    b.ctl('{%p endif %}')
    b.ctl('{%p if gifts_s2 | length %}')
    b.sub('If {{ s2_name }} is the Surviving @T@: {% for g in gifts_s2 %}{{ g.as_clause(T) }}'
          '{% if not loop.last %} {% endif %}{% endfor %}')
    b.ctl('{%p endif %}')
    b.body('If the property that is the subject of a specific gift is not part of the Trust '
           'Estate, the gift lapses, and no other property shall be substituted for it.')
    b.ctl('{%p endif %}')
    b.section('Tangible Personal Property',
              'The Trustee shall distribute the @Ts@\' tangible personal property (including '
              'household furniture and furnishings, jewelry, clothing, books, art, and personal '
              'effects, but not cash or property used in a trade or business) in accordance with '
              'any signed and dated written memorandum left by either @T@, the most recent '
              'controlling in case of conflict. Property not effectively disposed of by a '
              'memorandum shall be distributed {% if residue_plan == "children" %}to the @Ts@\' '
              'children who survive the Surviving @T@, to be divided among them as they agree, or, '
              'if they do not agree within ninety days, as the Trustee determines in shares of '
              'substantially equal value{% else %}as part of the residue{% endif %}. The Trustee may '
              'sell any item not wanted by a beneficiary and add the proceeds to the residue, and '
              'may pay the reasonable costs of storing and delivering items as an administration '
              'expense.')
    b.ctl('{%p if has_pets %}')
    b.section('Care of Pets',
              'The Trustee shall deliver {{ pet_description | trim }} (the "Pets") to {{ pet_caretaker }}'
              '{% if pet_alt_caretaker %}, or if {{ pet_caretaker }} is unable or unwilling to care for '
              'them, to {{ pet_alt_caretaker }}{% endif %}, and if no named caretaker is able and willing, '
              'to a caretaker selected by the Trustee who will provide a loving home.'
              '{% if pet_fund %} The Trustee shall set aside {{ money(pet_fund) }} as a separate trust '
              'under Probate Code Section 15212 for the Pets\' care, and may pay the caretaker '
              'reasonable amounts for food, veterinary care, and other needs of the Pets. The pet '
              'trust terminates when no Pet covered by it is living, and the Trustee shall then add '
              'any balance to the residue. The caretaker may enforce this trust.{% endif %}')
    b.ctl('{%p endif %}')
    b.section('Residue',
              'The Trustee shall distribute the balance of the Remaining Trust Estate (the '
              '"residue") as follows:')
    b.ctl('{%p if residue_plan == "children" %}')
    b.body('The Trustee shall divide the residue into as many equal shares as there are (1) '
           'children of the @Ts@ who survive the Surviving @T@ and (2) children of the @Ts@ who '
           'do not survive the Surviving @T@ but leave issue who do. The @Ts@\' children are '
           '{{ join_list(children_takers_names) }}. Each '
           'share for a surviving child shall be held or distributed for that child under Article '
           '@ART:beneficiary_trusts@. Each share for a deceased child shall be distributed to that '
           'child\'s then living issue, by right of representation, subject to Article '
           '@ART:beneficiary_trusts@.')
    b.ctl('{%p else %}')
    b.ctl('{%p for r in residuary %}')
    b.sub('{% if residuary_share_method == "equal" %}{% if residuary | length == 1 %}All'
          '{% else %}An equal share{% endif %}{% else %}{{ pct(r.share) }}{% endif %} to '
          '<b>{{ r.name.text }}</b>{% if r.relationship %} ({{ r.relationship }}){% endif %}.'
          '{% if r.is_charity %} If this organization is not then in existence or is not then '
          'described in Section 2055(a) of the Internal Revenue Code, this share shall be '
          'distributed to one or more such organizations, selected by the Trustee, whose '
          'purposes most nearly resemble its purposes.{% elif r.lapse == "issue" %} If '
          '{{ r.name.text }} does not survive the Surviving @T@, this share shall be distributed '
          'to the then living issue of {{ r.name.text }}, by right of representation, or, if '
          'none, shall be added proportionately to the other shares under this Section.'
          '{% else %} If {{ r.name.text }} does not survive the Surviving @T@, this share shall '
          'be added proportionately to the other shares under this Section.{% endif %}')
    b.ctl('{%p endfor %}')
    b.body('Each share for an individual shall be held or distributed under Article '
           '@ART:beneficiary_trusts@.')
    b.ctl('{%p endif %}')
    b.section('Ultimate Distribution',
              'If at any time no beneficiary described above is living (or in existence) to take '
              'any part of the Remaining Trust Estate, that part shall be distributed '
              '{% if ultimate_plan == "heirs_split" %}one-half to the persons who would then be '
              'the heirs of {{ s1_name }}, and one-half to the persons who would then be the heirs '
              'of {{ s2_name }}, in each case determined as if that @T@ had died at that time, '
              'unmarried, under the California laws of intestate succession then in effect'
              '{% elif ultimate_plan == "heirs" %}to the persons who would then be the heirs of the '
              'Surviving @T@, determined as if the Surviving @T@ had died at that time, unmarried, '
              'under the California laws of intestate succession then in effect'
              '{% else %}as follows: {{ ultimate_named | trim | replace("\\n", "; ") }}{% endif %}.')

    # ============================================================ BENEFICIARY TRUSTS
    b.article('{{ art_title["beneficiary_trusts"] }}')
    b.section('Application',
              'This Article governs every share of the Trust Estate that becomes distributable '
              'outright to an individual beneficiary on or after the death of the Surviving @T@, '
              'or under Article @ART:first_death@. A share distributable to a charitable '
              'organization shall be distributed outright.')
    b.ctl('{%p if dist_method == "outright" %}')
    b.section('Outright Distribution',
              'Each share shall be distributed outright to the beneficiary, subject to the '
              'remaining Sections of this Article.')
    b.ctl('{%p elif dist_method == "staged" %}')
    b.section('Staged Distribution Trusts',
              'Each share for a beneficiary shall be held as a separate trust for that beneficiary. '
              'The Trustee may distribute to or for the beneficiary as much of the net income and '
              'principal as the Trustee considers advisable for the beneficiary\'s health, '
              'education, maintenance, and support, adding undistributed income to principal. In '
              'addition, the Trustee shall distribute principal to the beneficiary as follows:')
    b.ctl('{%p for s in stage_plan %}')
    b.sub('{% if s["last"] %}when the beneficiary reaches age {{ s["age"] }}, the entire remaining '
          'balance of the trust{% else %}when the beneficiary reaches age {{ s["age"] }}, '
          '{{ s["portion"] }} of the trust principal then on hand{% endif %}{% if s["last"] %}.{% else %};{% endif %}')
    b.ctl('{%p endfor %}')
    b.body('If the beneficiary has already reached an age stated above when the trust is funded, '
           'the Trustee shall promptly distribute the portion attributable to that age. If the '
           'beneficiary dies before full distribution, the Trustee shall distribute the remaining '
           'trust property to the beneficiary\'s then living issue, by right of representation, '
           'or, if none, to the then living issue of the @Ts@, by right of representation, in '
           'either case subject to this Article, or, if none, under the Ultimate Distribution '
           'Section of Article @ART:final@.')
    b.ctl('{%p else %}')
    b.section('Lifetime Protective Trusts',
              'Each share for a beneficiary shall be held as a separate trust for the beneficiary\'s '
              'lifetime. The Trustee may distribute to or for the beneficiary as much of the net '
              'income and principal as the Trustee considers advisable for the beneficiary\'s '
              'health, education, maintenance, and support, considering the beneficiary\'s other '
              'resources and adding undistributed income to principal. The @Ts@ intend these trusts '
              'to protect each beneficiary\'s inheritance from creditors, divorce, and '
              'mismanagement, and to keep it out of the beneficiary\'s taxable estate.')
    b.section('Beneficiary as Co-Trustee',
              'On reaching age {{ lifetime_cotrustee_age }}, a beneficiary may become a co-Trustee '
              'of the beneficiary\'s own trust, to serve with the then acting Trustee, by a signed '
              'writing delivered to the Trustee. A beneficiary serving as co-Trustee may participate '
              'only in distributions limited to the beneficiary\'s health, education, maintenance, '
              'and support.')
    b.section('Distribution on the Beneficiary\'s Death',
              'On the beneficiary\'s death, the Trustee shall distribute the remaining trust property '
              '{% if lifetime_lpoa %}to such one or more of the beneficiary\'s spouse, the issue of '
              'the @Ts@, and charitable organizations, outright or in further trust, as the '
              'beneficiary appoints by a will or signed writing that specifically refers to this '
              'power (but not to the beneficiary, the beneficiary\'s estate, or the creditors of '
              'either), and to the extent not effectively appointed, {% endif %}to the beneficiary\'s '
              'then living issue, by right of representation, or, if none, to the then living issue '
              'of the @Ts@, by right of representation, in each case to be held under this Article, '
              'or, if none, under the Ultimate Distribution Section of Article @ART:final@.')
    b.ctl('{%p endif %}')
    b.section('Young Beneficiaries',
              'If any property becomes distributable outright to a beneficiary who has not reached '
              'age {{ young_age }}, the Trustee may hold that property in a separate trust for the '
              'beneficiary, distributing as much of the income and principal as the Trustee '
              'considers advisable for the beneficiary\'s health, education, maintenance, and '
              'support, and shall distribute the balance to the beneficiary at age {{ young_age }}. '
              'If the beneficiary dies sooner, the balance shall be distributed to the beneficiary\'s '
              'estate. Instead of holding the property in trust, the Trustee may distribute it to a '
              'custodian for the beneficiary under the California Uniform Transfers to Minors Act, '
              'to be held until the beneficiary reaches the oldest age permitted (age 25 if '
              'permitted by Probate Code Section 3920.5).')
    b.ctl('{%p if has_special_needs %}')
    b.section('Supplemental Needs Trusts',
              'Any share or other property distributable to {{ join_list(special_needs_list, "or") }} '
              'shall not be distributed outright, but shall be held in a '
              'separate supplemental needs trust for that beneficiary under the next Section.')
    b.ctl('{%p endif %}')
    b.section('Supplemental Needs Trust Terms',
              'If a beneficiary is disabled, receives or may need means-tested public benefits '
              '(such as Supplemental Security Income or Medi-Cal), or would lose eligibility for '
              'them by receiving a distribution, the Trustee may{% if has_special_needs %} (and for a '
              'beneficiary named in the preceding Section shall){% endif %} hold that beneficiary\'s '
              'share in a separate '
              'supplemental needs trust on the following terms:')
    b.sub('The Trustee may distribute income and principal, in the Trustee\'s sole and absolute '
          'discretion, only to supplement, and never to supplant, benefits the beneficiary '
          'receives or may receive from any public or private source. The beneficiary has no '
          'right to compel any distribution, and no part of the trust shall be considered '
          'available to the beneficiary.')
    b.sub('The Trustee may make a distribution that reduces public benefits if the Trustee '
          'determines that the beneficiary\'s needs will be better met by it, and may fund an '
          'ABLE account for the beneficiary under Section 529A of the Internal Revenue Code.')
    b.sub('This trust is a third-party trust funded only with property of the @Ts@. It is not '
          'subject to any reimbursement or payback requirement in favor of any public agency.')
    b.sub('On the beneficiary\'s death, the Trustee may pay the beneficiary\'s funeral expenses '
          '(to the extent this does not create a claim by a public agency) and shall distribute '
          'the balance to the beneficiary\'s then living issue, by right of representation, or, '
          'if none, to the then living issue of the @Ts@, by right of representation, subject to '
          'this Article.')
    b.section('Discretion to Delay Distribution',
              'If the Trustee reasonably believes that a beneficiary is suffering from substance '
              'abuse, is the subject of a pending divorce, bankruptcy, or creditor claim, or would '
              'otherwise be unable to manage a distribution prudently, the Trustee may delay any '
              'outright distribution to that beneficiary and continue to hold the property in '
              'trust for the beneficiary\'s health, education, maintenance, and support until the '
              'Trustee determines that the circumstance no longer exists.')
    b.section('Facility of Payment',
              'The Trustee may make any distribution for a beneficiary directly to the beneficiary, '
              'to the beneficiary\'s guardian or conservator, to a custodian under any Uniform '
              'Transfers to Minors Act, or by paying the beneficiary\'s expenses directly. The '
              'receipt of the payee is a complete discharge of the Trustee.')

    # ============================================================ POWERS
    b.article('{{ art_title["powers"] }}')
    b.section('General Powers',
              'The Trustee has all powers conferred on trustees by California law, including '
              'Probate Code Sections 16200 through 16249, as amended, and in addition the powers '
              'stated below, all of which the Trustee shall exercise in a fiduciary capacity:')
    for txt in [
        'to retain any property received, including a residence and closely held business '
        'interests, for as long as the Trustee considers advisable, without regard to '
        'diversification;',
        'to invest and reinvest in any kind of property, subject to the Uniform Prudent Investor '
        'Act (Probate Code Section 16045 and following);',
        'to sell, exchange, grant options on, partition, or otherwise dispose of any property, '
        'publicly or privately, for cash or on credit;',
        'to manage, improve, subdivide, lease (for terms beyond the duration of any trust), and '
        'otherwise deal with real property;',
        'to borrow money for any trust purpose, from any lender, including a Trustee, and to '
        'encumber trust property;',
        'to hold securities in the name of a nominee or in street name;',
        'to open and maintain deposit, brokerage, and other accounts, and to employ and pay '
        'investment advisers, accountants, attorneys, and other agents;',
        'to continue, form, or participate in any business entity, and to vote and exercise all '
        'rights of an owner;',
        'to purchase and maintain insurance of any kind;',
        'to make, or refrain from making, any tax election, including elections to treat a trust '
        'as a qualified subchapter S trust or electing small business trust;',
        'to inspect and monitor trust property for environmental conditions and to take any '
        'action necessary to comply with environmental law;',
        'to prosecute, defend, compromise, or abandon claims in favor of or against the trust;',
        'to make loans to, purchase property from, or otherwise deal with the estate of either '
        '@T@ on fair terms;',
        'to divide any trust into separate trusts, or to combine trusts with substantially '
        'identical terms, when doing so will not materially impair any beneficiary\'s interests;',
        'to make distributions in cash or in kind, or partly in each, and on a non-pro-rata '
        'basis, valuing assets at their fair market values on the date of distribution;',
        'to allocate receipts and disbursements between income and principal under the '
        'California laws governing fiduciary income and principal in effect from time to time, '
        'and, when those laws do not provide a rule, in the Trustee\'s reasonable discretion;',
        'to terminate any trust whose value has become so low that continued administration is '
        'uneconomical, distributing the property to the persons then entitled to income;',
        'to change the situs of any trust to another jurisdiction if the Trustee determines that '
        'the change is in the beneficiaries\' best interests; and',
        'to do all other acts that a prudent owner of property would do, without the need for '
        'court authorization.',
    ]:
        b.sub(txt)
    b.section('Claims and Reassessment Exclusions',
              'The Trustee may file claims for any available exclusion from property tax '
              'reassessment, including the parent-child exclusion under Revenue and Taxation Code '
              'Section 63.2, and may allocate a residence to a beneficiary to preserve an '
              'exclusion.')

    # ============================================================ SPECIAL ASSETS
    b.article('{{ art_title["special_assets"] }}')
    b.section('Retirement Benefits',
              'If the Trustee is the beneficiary of an individual retirement account or qualified '
              'retirement plan ("Retirement Benefits"):')
    b.sub('the Trustee may exercise every payout election available and shall withdraw at least '
          'any required minimum distribution each year;')
    b.sub('the @Ts@ intend each trust that receives Retirement Benefits to qualify as a '
          '"see-through" trust under Section 401(a)(9) of the Internal Revenue Code and the '
          'Treasury Regulations, and the Trustee shall deliver the required trust documentation '
          'to the plan administrator by October 31 of the year following the year of death;')
    b.sub('no Retirement Benefits shall be used to pay debts, taxes, or expenses of a @T@\'s '
          'estate after September 30 of the year following the year of the @T@\'s death if '
          'doing so would cause a trust to fail to qualify as a see-through trust; and')
    b.sub('the Trustee may divide Retirement Benefits into separate shares for each beneficiary '
          'and may distribute any Retirement Benefits received to the beneficiary for whom they '
          'are held.')
    b.section('Digital Assets',
              'The Trustee may access, manage, copy, transfer, deactivate, and delete the @Ts@\' '
              'digital assets and electronic communications (including their content) and the '
              'devices and accounts on which they are stored. Each @T@ consents to the disclosure '
              'of the content of that @T@\'s electronic communications to the Trustee under the '
              'California Revised Uniform Fiduciary Access to Digital Assets Act (Probate Code '
              'Section 870 and following).')
    b.ctl('{%p if has_firearms %}')
    b.section('Firearms',
              'If the Trust Estate includes firearms or ammunition, the Trustee shall possess, '
              'store, transfer, and distribute them only in compliance with all applicable federal '
              'and California law, including the Penal Code requirements for transfers through a '
              'licensed dealer. No Trustee who is prohibited from possessing a firearm may take '
              'possession of one; such a Trustee shall appoint, in a signed writing, a special '
              'Trustee who may lawfully possess firearms to act with respect to them. The Trustee '
              'may sell any firearm that cannot lawfully be distributed to a beneficiary and add '
              'the proceeds to that beneficiary\'s share.')
    b.ctl('{%p endif %}')

    # ============================================================ GENERAL PROVISIONS
    b.article('{{ art_title["general"] }}')
    b.section('Spendthrift Provision',
              'No beneficiary may voluntarily or involuntarily anticipate, assign, or encumber any '
              'interest in income or principal before actual receipt, and no interest shall be '
              'subject to the claims of a beneficiary\'s creditors or to legal process, to the '
              'fullest extent permitted by Probate Code Sections 15300 through 15309. This Section '
              'does not apply to a @T@\'s interest in the trust.')
    b.ctl('{%p if include_no_contest %}')
    b.section('No-Contest Clause',
              'If any beneficiary, alone or with others, directly or indirectly brings or joins in '
              'any of the following, that beneficiary shall take nothing under this instrument, '
              'and the beneficiary\'s interest shall pass as though the beneficiary had predeceased '
              'both @Ts@ without issue:')
    b.sub('a direct contest, as defined in Probate Code Section 21310, of this instrument, any '
          'amendment to it, either @T@\'s will, or any other protected instrument, brought '
          'without probable cause;')
    b.sub('a pleading to challenge a transfer of property on the ground that it was not the '
          'transferor\'s property at the time of the transfer; or')
    b.sub('the filing of a creditor\'s claim or prosecution of an action based on it.')
    b.body('This Section shall be enforced only to the extent permitted by Probate Code Sections '
           '21310 through 21315. "Protected instrument" has the meaning given in Probate Code '
           'Section 21310 and includes every instrument signed by either @T@ that disposes of '
           'property or nominates a fiduciary.')
    b.ctl('{%p endif %}')
    b.section('Survivorship',
              '{% if survivorship_days > 0 %}A beneficiary (other than a @T@) who does not survive '
              'the person on whose death a distribution depends by {{ survivorship_days }} days '
              'shall be treated as having predeceased that person.{% else %}A beneficiary (other '
              'than a @T@) must survive the person on whose death a distribution depends, as '
              'provided in Probate Code Section 21109.{% endif %} No survivorship period applies '
              'between the @Ts@, and the Surviving @T@ need only survive the Deceased @T@.')
    b.section('Definitions',
              'In this instrument:')
    b.sub('"Issue" means lineal descendants of all degrees, including persons adopted before '
          'reaching age eighteen, and "children" means the first generation of issue.')
    b.sub('A distribution to issue "by right of representation" shall be divided in the manner '
          'provided in Probate Code Section {% if representation == "per_stirpes" %}246{% else %}247{% endif %}.')
    b.sub('"Education" includes tuition, books, room, board, and related expenses at any '
          'accredited school, college, graduate, vocational, or technical program.')
    b.sub('"Trustee" refers to the trustee or co-trustees serving at the time, whether original '
          'or successor, and the singular includes the plural and each gender includes the '
          'others.')
    b.sub('"Internal Revenue Code" means the Internal Revenue Code of 1986, as amended, and '
          'corresponding provisions of later law.')
    b.section('Accounts and Notices',
              'While both @Ts@ are living, the Trustee owes duties only to the @Ts@ and need not '
              'account to any other beneficiary (Probate Code Section 15800). After a trust or any '
              'part of it becomes irrevocable, the Trustee shall serve the notification required '
              'by Probate Code Section 16061.7 and shall account as required by Probate Code '
              'Section 16062, except to the extent a beneficiary waives the account in writing.')
    b.section('Perpetuities',
              'Unless sooner terminated, every trust created under this instrument shall terminate '
              'one day before the end of the period permitted by the California Uniform Statutory '
              'Rule Against Perpetuities (Probate Code Section 21200 and following), and the '
              'Trustee shall then distribute the property to the persons then entitled to receive '
              'income.')
    b.section('Governing Law',
              'This instrument shall be governed by the law of California, regardless of the situs '
              'of administration.')
    b.section('Severability and Headings',
              'If any provision of this instrument is unenforceable, the remaining provisions shall '
              'remain in effect. Headings are for convenience only and do not affect meaning.')

    # ------------------------------------------------------------ execution
    b.plain('<b>Execution.</b> The @Ts@ certify that they have read this Trust Agreement, that it '
            'correctly states the terms and conditions under which the Trust Estate is to be held, '
            'administered, and distributed, and that they approve it. The Trustees accept the '
            'trust and agree to administer it according to its terms.', before=12, keep=True)
    b.plain('Signed on @DATE@, at ' + '@COUNTY@' + ' County, California.', keep=True)
    b.plain('<b>TRUSTORS AND TRUSTEES:</b>', keep=True, before=6)
    b.sig('<b>{{ s1_name | upper }}</b>', '@T@ and Trustee')
    b.sig('<b>{{ s2_name | upper }}</b>', '@T@ and Trustee')
    b.ctl("{{p include_docx_template('notary_ack_ca.docx') }}")

    # ------------------------------------------------------------ schedules
    for letter, label, rows, owner in [
        ('A', 'Community Property of {{ s1_name }} and {{ s2_name }}', 'sched_cp', None),
        ('B', 'Separate Property of {{ s1_name }}', 'sched_s1', '{{ s1_name }}'),
        ('C', 'Separate Property of {{ s2_name }}', 'sched_s2', '{{ s2_name }}'),
    ]:
        raw.page_break()
        b.para('SCHEDULE ' + letter, 'Schedule Title')
        b.center('<b>' + label + '</b>', after=4)
        b.center('<i>{{ trust_title }}, ' + DATED + '</i>', after=18)
        if letter == 'A':
            b.plain('The @Ts@ declare that the following property is their community property and '
                    'transfer it to the Trustee:')
        else:
            b.plain(owner + ' declares that the following property is ' + owner + '\'s separate '
                    'property and transfers it to the Trustee:')
        b.ctl('{%p for a in ' + rows + ' %}')
        b.para('{{ loop.index }}.<tab>{{ a.schedule_text() }}{% if a.asset_type == "realprop" and '
               'a.legal_description %}, more particularly described as: {{ a.legal_description | trim | '
               'replace("\\n", " ") }}{% endif %}.', 'Hang')
        b.ctl('{%p endfor %}')
        if letter == 'A':
            b.para('{{ sched_cp | length + 1 }}.<tab>All of the @Ts@\' community property interest in '
                   'their household furniture and furnishings, jewelry, art, and other tangible '
                   'personal property, and all other community property assigned to the Trustee by '
                   'the @Ts@\' General Assignment of even date.', 'Hang')
        else:
            b.ctl('{%p if not ' + rows + ' | length %}')
            b.plain('None at the date of signing. Separate property of ' + owner + ' added later '
                    'shall be listed on an amended Schedule ' + letter + ' or identified in the '
                    'instrument of transfer.')
            b.ctl('{%p endif %}')

    raw.save(path)
