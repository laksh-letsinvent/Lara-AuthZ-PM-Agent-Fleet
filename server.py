#!/usr/bin/env python3
"""
AuthZ Pipeline Dashboard — Local Server

Run:  python server.py
Open: http://localhost:8000
"""

import http.server
import json
import re
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).parent
PORT = 8000

SKILL_NAMES = {
    1: 'spec-writer',
    2: 'rule-lister',
    3: 'scenario-builder',
    4: 'schema-handoff',
    5: 'schema-sketch',
}

# ─── Parsers ──────────────────────────────────────────────────────────────────

def parse_frontmatter(content):
    fm = {}
    if content.startswith('---'):
        try:
            end = content.index('---', 3)
            for line in content[3:end].strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip()
        except ValueError:
            pass
    return fm


def parse_pipeline_steps(content):
    steps = []
    in_pipeline = False
    for line in content.split('\n'):
        if '## Pipeline status' in line:
            in_pipeline = True
            continue
        if in_pipeline and line.startswith('## '):
            break
        if in_pipeline and line.startswith('|') and '---' not in line and 'Step' not in line:
            cols = [c.strip() for c in line.split('|')[1:-1]]
            if len(cols) >= 4:
                try:
                    step_num = int(cols[0])
                    steps.append({
                        'step': step_num,
                        'specialist': cols[1],
                        'output': cols[2].strip('`'),
                        'status': cols[3],
                    })
                except ValueError:
                    pass
    return steps


def parse_open_issues(content):
    issues = []
    in_issues = False
    for line in content.split('\n'):
        if '## Open issues' in line:
            in_issues = True
            continue
        if in_issues and line.startswith('## '):
            break
        if in_issues and line.startswith('- **'):
            m = re.match(r'- \*\*([^*]+)\*\*\s*[—–-]\s*(.*)', line)
            if m:
                issues.append({'title': m.group(1).strip(), 'detail': m.group(2).strip()})
    return issues


def parse_decisions(content):
    decisions = []
    in_log = False
    for line in content.split('\n'):
        if '## Decisions log' in line:
            in_log = True
            continue
        if in_log and line.startswith('## '):
            break
        if in_log and line.startswith('- **'):
            m = re.match(r'- \*\*([^*]+)\*\*\s*[—–-]\s*(.*)', line)
            if m:
                decisions.append({'date': m.group(1).strip(), 'note': m.group(2).strip()})
    return decisions


def extract_section(content, heading):
    m = re.search(rf'## {re.escape(heading)}\n\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    return m.group(1).strip() if m else ''


# ─── Data loaders ─────────────────────────────────────────────────────────────

def get_runs():
    runs = []
    runs_dir = BASE / 'runs'
    if not runs_dir.exists():
        return runs
    for folder in sorted(runs_dir.iterdir(), reverse=True):
        if folder.name.startswith('_') or not folder.is_dir():
            continue
        rc = folder / '00-run-card.md'
        if not rc.exists():
            continue
        content = rc.read_text()
        fm = parse_frontmatter(content)
        steps = parse_pipeline_steps(content)
        signed_off = sum(1 for s in steps if s['status'] == 'signed-off')
        runs.append({
            'name': folder.name,
            'title': fm.get('title', folder.name),
            'domain': fm.get('domain', ''),
            'status': fm.get('status', ''),
            'opened': fm.get('opened', ''),
            'steps_done': signed_off,
            'steps_total': len(steps),
        })
    return runs


def get_run_detail(run_name):
    rc = BASE / 'runs' / run_name / '00-run-card.md'
    if not rc.exists():
        return None
    content = rc.read_text()
    fm = parse_frontmatter(content)
    steps = parse_pipeline_steps(content)
    issues = parse_open_issues(content)
    decisions = parse_decisions(content)
    summary = extract_section(content, 'What this run is')

    for step in steps:
        skill = SKILL_NAMES.get(step['step'], '')
        step['command'] = f'Run Skill {skill} — for {run_name}'
        step['has_output'] = (BASE / 'runs' / run_name / step['output']).exists()

    return {
        'name': run_name,
        'frontmatter': fm,
        'steps': steps,
        'issues': issues,
        'decisions': decisions,
        'summary': summary,
    }


def get_file_content(run_name, filename):
    p = BASE / 'runs' / run_name / filename
    if p.exists():
        return {'content': p.read_text(), 'exists': True}
    return {'content': '', 'exists': False}


def get_inbox():
    inbox = BASE / 'inbox'
    files = []
    if inbox.exists():
        for f in sorted(inbox.glob('*.md')):
            files.append({'name': f.name, 'size': f.stat().st_size})
    return files


# ─── HTTP Handler ─────────────────────────────────────────────────────────────

class Handler(http.server.BaseHTTPRequestHandler):

    def log_message(self, *args):
        pass  # quiet

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, path):
        body = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        p = urlparse(self.path).path

        if p in ('/', '/index.html'):
            self.send_html(BASE / 'dashboard.html')
        elif p == '/api/runs':
            self.send_json(get_runs())
        elif p == '/api/inbox':
            self.send_json(get_inbox())
        elif p.startswith('/api/run/'):
            data = get_run_detail(p[9:])
            self.send_json(data if data else {'error': 'not found'}, 200 if data else 404)
        elif p.startswith('/api/file/'):
            parts = p[10:].split('/', 1)
            self.send_json(get_file_content(*parts) if len(parts) == 2 else {'error': 'bad path'})
        else:
            self.send_response(404)
            self.end_headers()


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    server = http.server.HTTPServer(('localhost', PORT), Handler)
    print(f'\n  AuthZ Pipeline Dashboard')
    print(f'  → http://localhost:{PORT}\n')
    print(f'  Ctrl+C to stop\n')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopped.')
