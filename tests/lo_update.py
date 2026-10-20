"""Update indexes (TOC) and fields in a DOCX with LibreOffice, optionally export PDF.

Local stand-in for the PysIndexer macro that docassemble servers use for
`update references: True`.  Run with a Python that has the `uno` module:

    python3 tests/lo_update.py in.docx [out.pdf]
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def prop(name, value):
    p = PropertyValue()
    p.Name = name
    p.Value = value
    return p


def main(path, pdf=None):
    pipe = 'lo_update_%d' % os.getpid()
    profile = '/tmp/lo_update_profile'
    proc = subprocess.Popen(['soffice', '--headless', '--invisible', '--nologo', '--norestore',
                             '-env:UserInstallation=file://' + profile,
                             '--accept=pipe,name=%s;urp;' % pipe])
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
        for _ in range(60):
            try:
                ctx = resolver.resolve('uno:pipe,name=%s;urp;StarOffice.ComponentContext' % pipe)
                break
            except Exception:
                time.sleep(0.5)
        desktop = ctx.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', ctx)
        url = uno.systemPathToFileUrl(os.path.abspath(path))
        doc = desktop.loadComponentFromURL(url, '_blank', 0, (prop('Hidden', True),))
        indexes = doc.getDocumentIndexes()
        for idx in range(indexes.getCount()):
            indexes.getByIndex(idx).update()
        doc.getTextFields().refresh()
        doc.storeToURL(url, (prop('FilterName', 'MS Word 2007 XML'),))
        if pdf:
            doc.storeToURL(uno.systemPathToFileUrl(os.path.abspath(pdf)), (prop('FilterName', 'writer_pdf_Export'),))
        doc.close(True)
    finally:
        try:
            desktop.terminate()
        except Exception:
            pass
        proc.wait(timeout=30)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
