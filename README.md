# docassemble.cphrlt: California Joint Revocable Living Trust

A Docassemble questionnaire that builds a **shared (joint) revocable living
trust for a married couple or registered domestic partners** under
California law, plus the documents that go with it. It is meant to sit
between a bare-bones form and a WealthCounsel-style system: a solid,
conventional California RLT with the plan choices most couples need.

> **Attorney review required.** The output is a draft for review by a
> California attorney before signing. Statutes and tax figures were checked
> in October 2026 (for example, the $15 million 2026 federal exclusion under
> P.L. 119-21).

## Documents produced

| Document | Template | Notes |
|---|---|---|
| Joint Revocable Living Trust Agreement | `joint_rlt_trust.docx` | 14 to 15 auto-numbered articles, list of articles (contents), Schedules A/B/C, notary acknowledgment |
| Certification of Trust | `certification_of_trust.docx` | Probate Code §18100.5 items (b)(1)–(8), signed under penalty of perjury and notarized |
| General Assignment of Assets | `general_assignment.docx` | Supports a Heggstad/§850 petition; excludes retirement accounts and insurance |
| Pour-Over Will (one per spouse) | `pour_over_will.docx` | Same template run twice through `field code`; executor, guardian, IAEA, attestation |
| Plan Summary and Funding Memo | `plan_summary.docx` | For the attorney: decisions, fiduciaries, **placeholder list**, review flags, funding checklist, signing and post-death steps |
| California notary acknowledgment | `notary_ack_ca.docx` | Civil Code §1189 form, inserted with `include_docx_template()` |

Every document is delivered as both PDF and editable DOCX. Sample output
for two fictional couples is in [`samples/`](samples/).

## Plan design

**At the first death** (the main design choice):

1. **All to Survivor:** the whole trust stays revocable by the survivor, with a portability election.
2. **Survivor's Trust plus optional Disclaimer Trust** (the default): the survivor can disclaim into an irrevocable HEMS trust within nine months (IRC §2518, Prob. Code §§275–295). The disclaimer trust carries the §2518 restrictions: no power of appointment and no 5-and-5 power.
3. **Mandatory A/B:** the Bypass Trust is funded with the exclusion amount. Options: mandatory or discretionary income, a 5-and-5 power, and a limited power of appointment. Disclaimed property goes into a separate share.

**After both deaths:** specific gifts (cash, items, or real property; timed
at either spouse's death or the survivor's death; lapse to issue or to the
residue; charity fallback), a tangible personal property memorandum, a pet
trust (Prob. Code §15212), and the residue to the children equally or to
named beneficiaries (equal shares or percentages that must total 100%).
Representation follows Prob. Code §246 (per stirpes) or §247 (per capita at
each generation). The ultimate backstop is one-half to each spouse's heirs,
the survivor's heirs, or named takers.

**Beneficiary shares:** outright (held in trust until a chosen age, with a
CUTMA option), staged (one to three ages), or lifetime protective trusts
(beneficiary co-trustee age, optional limited power of appointment). Also
included: third-party supplemental needs trusts (mandatory for named
people, discretionary for anyone), a discretionary holdback, and facility
of payment.

**Also covered:**
- community/separate property character (Fam. Code §761) and an optional Fam. Code §852 community property agreement
- revocation and amendment rules for a joint trust (Prob. Code §4264 limits on agents)
- the residence right (homeowners' exemption, IRC §121, R&T §62(d))
- trustees: either-may-act, successor order or co-trustees, vacancy, resignation, removal, bond, compensation
- incapacity by one or two physicians, with HIPAA/CMIA release
- non-pro-rata division and portability
- the trustee powers list and the Prop 19 claim power
- retirement benefits (see-through trust), RUFADAA digital assets, firearms
- spendthrift, no-contest (Prob. Code §§21310–21315), survivorship, §16061.7 notices, USRAP

## Docassemble features used

- `sections` navigation, `progress` with a percentage, `question help button`, `help` and `interview help`, and `auto terms` (a glossary)
- Lists in three styles:
  - `list collect` (successor trustees, beneficiaries, guardians, executors)
  - one item per screen with `complete_attribute` (children, gifts, assets)
  - `.revisit` edit screens and `table` blocks with `edit`
- A `review` screen with `need`, `follow up`, and `show if`, opened from a `menu_items` action
- Field options:
  - `show if` and `hide if` in variable and code forms, plus `js show if`
  - `validation code` (ages ascending, shares totaling 100%, California residence, special needs selections)
  - field `datatype`s and `input type`s including `combobox`, `checkboxes` from code with defaults, and choices with per-choice `help`
- Question modifiers: `if:` (alternate questions), `reconsider`, `imports`, and `modules` with custom classes (`RLTPerson`, `Beneficiary`, `SpecificGift`, `TrustAsset`)
- Attachments:
  - standalone `attachment` blocks with `variable name`, shown through `attachment code`, with `allow downloading` and `zip filename` for a ZIP
  - `valid formats` set by code (Word only, or Word plus PDF), and `field code` (one will template for both spouses)
  - `include_docx_template()` for the notary acknowledgment
- Custom CSS (`data/static/rlt.css`) and `metadata` exit options

## Placeholders

Only these items can print as **yellow-highlighted blanks**. The interview's
final screen and section 3 of the memo list the ones that apply to each
matter.

| Placeholder | When it appears |
|---|---|
| Trust signing date | When "Do you know the date you will sign?" is No |
| County of execution | When the signing county is left blank |
| Trust taxpayer identification number (Certification, paragraph 7) | When "leave blank" is chosen (the recommended choice, for privacy) |
| Real property legal description (Certification, paragraph 9) | When an asset is real property and no legal description was entered |
| Attorney and firm name (memo header) | When the preparer screen is left blank |
| Guardian "None nominated" (memo) | When there are minor children but no guardian nominee |

These are intentional blank lines, not placeholders: notary acknowledgment
fields, the will attestation (witness names, addresses, date and place), and
the signature lines. A missing APN is flagged in the memo but not printed
as a blank.

## Avoiding gateway timeouts

Converting each document to PDF runs LibreOffice, and doing that for six
documents inside one web request can exceed nginx's timeout (a **504
Gateway Time-out**). So:

- **By default only Word files are built.** They are rendered directly from
  the templates, with no LibreOffice, and finish in a few seconds. The trust's
  contents list is generated text, not a Word field, so it never needs a
  LibreOffice update.
- **PDF copies are opt-in** ("Also create PDF copies?" on the documents
  screen). When chosen, the documents are built by a Celery background task:
  1. `background_action('assemble_documents_bg', 'refresh')` starts the task,
     and a "Preparing your documents" screen refreshes until it finishes.
  2. The task hands the files back through
     `background_response_action('documents_ready', ...)`.
  3. If the task fails, an error screen offers **Try again**. If the server
     has no working background queue (RabbitMQ/Celery), the waiting screen
     links to `build_documents_now`, which delivers the Word files instead.
- **Review answers** (on the final screen or in the menu) runs `edit_answers`,
  which discards the old files and rebuilds them. A `doc_generation` counter
  makes the interview ignore a late result from an earlier background run.

## Installing

1. Push this repository to GitHub, or download it as a ZIP.
2. In Docassemble, open **Package Management** and install from the GitHub URL or the ZIP.
3. Run the interview at `/interview?i=docassemble.cphrlt:data/questions/joint_rlt.yml`.

To use the Playground instead, upload:
- the four YAML files to Questions
- the `.docx` files to Templates
- `rlt_helpers.py` to Modules
- `rlt.css` to Static

## Editing the templates

The DOCX templates are generated. Edit the content in `tools/build_trust.py`
or `tools/build_ancillary.py`, then run:

```bash
python3 tools/build_all.py
```

The trust uses real Word multilevel numbering ("ARTICLE ONE", "1.1",
"(a)"), so removing a conditional article or section renumbers everything
automatically. Cross-references to articles come from
`rlt_helpers.article_map()`. Keep it in sync if you add or remove an
article. You can also edit the generated `.docx` directly in Word, but the
next build will overwrite your changes.

## Testing

`tests/da_harness.py` runs the real interview headlessly with
`docassemble.base` (server hooks stubbed). It answers every screen from
`tests/scenarios.py` and assembles every document through docassemble's own
DOCX pipeline and LibreOffice:

```bash
pip install docassemble.base
pip install -e .
DA_CONFIG_FILE=tests/config.example.yml LANG=en_US.UTF-8 python tests/da_harness.py a   # a, b, or c
```

The harness also needs LibreOffice with Python-UNO (`tests/lo_update.py`
stands in for the server's table-of-contents macro), an `en_US.UTF-8`
locale, and the `zbar` shared library, which `docassemble.base` imports.

The three scenarios cover:
- **a:** blended family, disclaimer plan, gifts, pets, staged trusts, special needs, assets, guardians, firearms
- **b:** restatement, registered domestic partners, "Settlor" wording, A/B plan with 5-and-5 and LPOA, co-trustees, percentage residue with the 100% check, lifetime trusts, CP agreement
- **c:** simple all-to-survivor plan

Static checks:

```bash
dayamlchecker --no-url-check docassemble/cphrlt/data/questions/*.yml
```

The only items it reports are EA510 (optional yes/no shorthand style).
