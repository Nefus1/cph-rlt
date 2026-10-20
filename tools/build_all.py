"""Regenerate every DOCX template in docassemble/cphrlt/data/templates.

    python3 tools/build_all.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import build_ancillary  # noqa: E402
import build_trust  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'docassemble', 'cphrlt',
                   'data', 'templates')


def main():
    os.makedirs(OUT, exist_ok=True)
    targets = {
        'joint_rlt_trust.docx': build_trust.build,
        'notary_ack_ca.docx': build_ancillary.build_notary,
        'certification_of_trust.docx': build_ancillary.build_certification,
        'general_assignment.docx': build_ancillary.build_assignment,
        'pour_over_will.docx': build_ancillary.build_will,
        'plan_summary.docx': build_ancillary.build_summary,
    }
    for name, fn in targets.items():
        fn(os.path.join(OUT, name))
        print('wrote', name)


if __name__ == '__main__':
    main()
