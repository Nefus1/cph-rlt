"""Headless driver for docassemble interviews (developer tool, not deployed).

Runs an interview with docassemble.base outside the web server by stubbing the
server hooks, answering each screen from a scenario, and assembling the
attachments with the real docassemble DOCX pipeline (docxtpl + LibreOffice).

    DA_CONFIG_FILE=config.yml python tests/da_harness.py scenario_name [outdir]
"""
import os
import shutil
import sys
import tempfile
import mimetypes
import importlib.resources

import locale

import pluggy

try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    pass

import docassemble.base.config as daconfig_mod
daconfig_mod.load()
from docassemble.base.plugin_manager import pm  # noqa: E402

hookimpl = pluggy.HookimplMarker("docassemble")
OUTDIR = os.environ.get('DA_HARNESS_OUT', tempfile.mkdtemp(prefix='daharness'))
os.makedirs(OUTDIR, exist_ok=True)
_counter = [100]
_files = {}
_last_status = None


def _package_path(ref, folder='templates'):
    if ':' in ref:
        package, path = ref.split(':', 1)
    else:
        package, path = 'docassemble.cphrlt', ref
    if not path.startswith('data/'):
        path = 'data/' + folder + '/' + path
    return str(importlib.resources.files(package).joinpath(path))


class FakeRedis:
    def __init__(self):
        self.d = {}

    def get(self, key):
        return self.d.get(key)

    def set(self, key, val, *args, **kwargs):
        self.d[key] = val

    def setex(self, key, ttl, val):
        self.d[key] = val

    def delete(self, *keys):
        for k in keys:
            self.d.pop(k, None)

    def expire(self, *args, **kwargs):
        return True

    def incr(self, key):
        self.d[key] = int(self.d.get(key, 0)) + 1
        return self.d[key]


_redis = FakeRedis()


class Stubs:
    @hookimpl
    def get_server_redis(self):
        return _redis

    @hookimpl
    def get_server_redis_user(self):
        return _redis

    @hookimpl
    def get_configuration(self):
        return daconfig_mod.daconfig

    @hookimpl
    def get_hostname(self):
        return 'localhost'

    @hookimpl
    def get_debug_status(self):
        return True

    @hookimpl
    def get_default_language(self):
        return 'en'

    @hookimpl
    def get_default_dialect(self):
        return 'us'

    @hookimpl
    def get_default_locale(self):
        return 'US.utf8'

    @hookimpl
    def get_default_voice(self):
        return None

    @hookimpl
    def get_default_timezone(self):
        return 'America/Los_Angeles'

    @hookimpl
    def get_default_country(self):
        return 'US'

    @hookimpl
    def get_button_class_prefix(self):
        return 'btn-'

    @hookimpl
    def get_default_table_class(self):
        return 'table table-striped'

    @hookimpl
    def get_default_thead_class(self):
        return 'table-dark'

    @hookimpl
    def url_for(self, endpoint, kwargs):
        return '/' + str(endpoint)

    @hookimpl
    def url_finder(self, file_reference, kwargs):
        return '/file/' + str(file_reference)

    @hookimpl
    def get_url(self):
        return 'http://localhost'

    @hookimpl
    def get_referer(self):
        return None

    @hookimpl
    def file_finder(self, file_reference, question, folder, package, filename, return_nonexistent, uids):
        ref = str(file_reference)
        if ref in _files:
            path = _files[ref]
        else:
            if package and ':' not in ref:
                ref = package + ':' + ref
            path = _package_path(ref, folder or 'templates')
        if not os.path.exists(path):
            return {'filename': os.path.basename(path)} if return_nonexistent else {}
        ext = os.path.splitext(path)[1][1:]
        return {'fullpath': path, 'path': os.path.splitext(path)[0], 'filename': os.path.basename(path),
                'extension': ext, 'mimetype': mimetypes.guess_type(path)[0] or 'application/octet-stream'}

    @hookimpl
    def save_numbered_file(self, filename, orig_path, yaml_file_name, uid):
        _counter[0] += 1
        dest = os.path.join(OUTDIR, filename)
        shutil.copyfile(orig_path, dest)
        _files[str(_counter[0])] = dest
        ext = os.path.splitext(filename)[1][1:]
        return (_counter[0], ext, mimetypes.guess_type(filename)[0])

    @hookimpl
    def get_ext_and_mimetype(self, filename):
        ext = os.path.splitext(filename)[1][1:]
        return (ext, mimetypes.guess_type(filename)[0])

    @hookimpl
    def secure_filename(self, filename):
        import werkzeug.utils
        return werkzeug.utils.secure_filename(filename)

    @hookimpl
    def secure_filename_unicode_ok(self, the_filename):
        import re as _re
        return _re.sub(r'[^\w.\- ]', '', the_filename).strip().replace(' ', '_')

    @hookimpl
    def secure_filename_spaces_ok(self, filename):
        import re as _re
        return _re.sub(r'[^\w.\- ]', '', filename).strip()

    @hookimpl
    def get_main_page_parts(self):
        return {}

    @hookimpl
    def server_sql_defined(self, key):
        return False

    @hookimpl
    def server_sql_get(self, key, secret):
        return None

    @hookimpl
    def server_sql_set(self, key, val, encrypted, secret, the_user_id):
        return None

    @hookimpl
    def server_sql_keys(self, prefix):
        return []

    @hookimpl
    def server_interview_menu(self, absolute_urls, start_new, tag):
        return []

    @hookimpl
    def to_text(self, html_doc):
        import re as _re
        return _re.sub(r'<[^>]+>', '', html_doc)

    @hookimpl
    def navigation_bar(self, nav, interview, wrapper, inner_div_class, inner_div_extra, show_links,
                       hide_inactive_subs, a_class, show_nesting, include_arrows, always_open,
                       return_dict, li_class):
        return ''


pm.register(Stubs())

import docassemble.base.parse  # noqa: E402
import subprocess  # noqa: E402

LO_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lo_update.py')


def _local_update_references(filename):
    subprocess.run(['/usr/bin/python3', LO_SCRIPT, filename], check=True)
    return True


def _local_word_to_pdf(in_file, in_format, out_file, pdfa=False, password=None, owner_password=None,
                       update_refs=False, tagged=False, filename=None, retry=True):
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, 'doc.' + in_format)
    shutil.copyfile(in_file, src)
    subprocess.run(['/usr/bin/python3', LO_SCRIPT, src, out_file], check=True)
    return True


docassemble.base.parse.update_references = _local_update_references
docassemble.base.parse.word_to_pdf = _local_word_to_pdf
from docassemble.base.interview_cache import get_interview  # noqa: E402
import docassemble.base.functions as fx  # noqa: E402
from docassemble.base.thread_context import global_context, empty_globals, user_dict_context  # noqa: E402

YAML = 'docassemble.cphrlt:data/questions/joint_rlt.yml'


def current_info(action=None, arguments=None):
    info = {'user': {'is_anonymous': True, 'is_authenticated': False, 'email': None, 'theid': 't1',
                     'the_user_id': 't1', 'roles': ['user'], 'firstname': None, 'lastname': None,
                     'nickname': None, 'country': None, 'subdivisionfirst': None,
                     'subdivisionsecond': None, 'subdivisionthird': None, 'organization': None,
                     'timezone': None, 'language': 'en', 'location': None, 'session_uid': 'abc',
                     'device_id': 'dev'},
            'session': 'sess1', 'secret': 'secret', 'yaml_filename': YAML, 'interface': 'web',
            'url': 'http://localhost/interview', 'url_root': 'http://localhost/',
            'encrypted': False, 'headers': {}, 'clientip': '127.0.0.1', 'method': 'GET'}
    if action:
        info.update({'action': action, 'arguments': arguments or {}, 'orig_action': action,
                     'orig_arguments': arguments or {}})
    return info


# ---------------------------------------------------------------- background tasks
# A stand-in for the Celery worker: background_action() queues the action, and
# the harness runs it on an isolated copy of the answers (a real worker's
# changes are not saved), then runs the background_response_action() callback
# on the real answers, exactly as the server does.
import pickle  # noqa: E402
import time  # noqa: E402

_pending_bg = []


class FakeTask:
    def __init__(self):
        self.done = False
        self.error = None

    def ready(self):
        return self.done

    def failed(self):
        return self.error is not None

    def get(self):
        return None

    def result(self):
        class R:
            pass
        r = R()
        r.error_type = 'Error' if self.error else None
        r.error_message = self.error
        r.value = None
        return r


def _fake_bg_action(action, ui_notification, **kwargs):
    task = FakeTask()
    _pending_bg.append((task, action, kwargs))
    return task


fx.bg_action = _fake_bg_action


def _assemble(interview, user_dict, action=None, arguments=None):
    status = docassemble.base.parse.InterviewStatus(current_info=current_info(action, arguments))
    fx.this_thread.current_info = status.current_info
    with user_dict_context(user_dict):
        interview.assemble(user_dict, status)
    return status


def _run_background(interview, user_dict, verbose):
    while _pending_bg:
        task, action, kwargs = _pending_bg.pop(0)
        bg_dict = pickle.loads(pickle.dumps(fx.pickleable_objects(user_dict)))
        started = time.time()
        try:
            status = _assemble(interview, bg_dict, action, kwargs)
            q = status.question
            resp = getattr(q, 'action', None) if q is not None else None
            if not resp:
                raise RuntimeError('background action ended without background_response_action '
                                   '(question %r)' % (q.id if q is not None else None))
            if verbose:
                print('     [worker] %s -> %s (%.0f s)' % (action, resp['action'], time.time() - started))
            _assemble(interview, user_dict, resp['action'], resp['arguments'])
        except Exception as err:  # the worker records the failure on the task
            task.error = '%s: %s' % (err.__class__.__name__, err)
            if verbose:
                print('     [worker] FAILED', task.error)
        task.done = True


def run(scenario, max_steps=200, verbose=True):
    with global_context(empty_globals()):
        return _run(scenario, max_steps, verbose)


def _run(scenario, max_steps, verbose):
    fx.this_thread.current_info = current_info()
    interview = get_interview(YAML)
    user_dict = docassemble.base.parse.get_initial_dict()
    user_dict['_internal']['steps'] = 1
    seen = []
    pending_action = None
    finals = 0
    for step in range(max_steps):
        started = time.time()
        if pending_action:
            status = _assemble(interview, user_dict, pending_action)
            pending_action = None
        else:
            status = _assemble(interview, user_dict)
        elapsed = time.time() - started
        if verbose and elapsed > 2:
            print('     [foreground request took %.1f s]' % elapsed)
        global _last_status
        _last_status = status
        q = status.question
        qid = q.id if q is not None else None
        seen.append(qid)
        if verbose:
            print("%3d  %-34s %s" % (step, qid, str(getattr(status, "question_text", "") or "").strip()[:70]))
        if qid == 'final screen':
            finals += 1
            if finals == 1 and scenario.get('_edit_after_final'):
                # Simulate "Review your answers" -> Continue -> documents rebuilt.
                first_files = [dict(att.get('file', {})) for att in status.attachments or []]
                user_dict['_first_files'] = first_files
                pending_action = 'edit_answers'
                continue
            return interview, user_dict, status, seen
        if qid == 'waiting screen':
            _run_background(interview, user_dict, verbose)
            continue
        action = scenario.get(qid)
        if action is None:
            raise SystemExit('No scenario answer for question id %r (seeking %r)' % (qid, getattr(q, 'fields_used', None)))
        statements = action(user_dict) if callable(action) else action
        for stmt in statements:
            exec(stmt, user_dict)
        user_dict['_internal']['steps'] += 1
    raise SystemExit('too many steps')


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from scenarios import SCENARIOS
    name = sys.argv[1] if len(sys.argv) > 1 else 'a'
    interview, user_dict, status, seen = run(SCENARIOS[name])
    print('\nReached final screen after %d screens.' % len(seen))
    for att in status.attachments or []:
        print('  attachment:', att.get('name'), {k: v for k, v in att.get('file', {}).items()})
    if '_first_files' in user_dict:
        now = [dict(att.get('file', {})) for att in status.attachments or []]
        print('Rebuilt after edit:', now != user_dict['_first_files'])
    print('Placeholders:')
    for p in user_dict['placeholders']:
        print('  -', p['item'])
    print('Output folder:', OUTDIR)


if __name__ == '__main__':
    main()
