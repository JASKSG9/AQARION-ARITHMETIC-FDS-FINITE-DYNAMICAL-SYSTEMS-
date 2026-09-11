Welcome to Termux

Docs:       https://doc.termux.com
Community:  https://community.termux.com

Working with packages:
 - Search:  pkg search <query>
 - Install: pkg install <package>
 - Upgrade: pkg upgrade

Report issues at https://bugs.termux.com
~ $ #!/usr/bin/env python3
on, sys, pathlib, datetime, mimetypes
from collections import Counter

SUSPICIOUS_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"send\s+your\s+credentials",
    r"execute\s+this\s+command",
    r"download\s+this\s+payload",
    r"paste\s+your\s+API\s+key",
    r"disable\s+security",
    r"os\.system\(",
    r"subprocess\.",
    r"requests\.(get|post)\(",
    r"socket\.",
    r"eval\(",
    r"base64\.b64decode",
]

CLAIM_PATTERNS = [
    r"THEOREM\s+PROVEN",
    r"PROOF\s+COMPLETE",
    r"publication\s+candidate",
    r"world[- ]class",
    r"production\s+certified",
    r"CLOSED\s+—\s+explicit",
]

def sha256_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def scan_repo(root):
    root=pathlib.Path(root)
    files=list(root.rglob('*'))
    file_types=Counter()
    exec_files=[]
    for f in files:
        if f.is_dir(): continue
        ext=f.suffix.lower()
        if ext in ['.py','.sh','.js','.ts']:
            exec_files.append(f)
            file_types['python' if ext=='.py' else ext]+=1
        elif ext in ['.ipynb']: file_typ~ $ """
es['notebooks']+=1
        elif ext in ['.bin','.pt','.onnx','.safetensors']: file_types['models']+=1
        elif ext in ['.csv','.jsonl','.parquet','.npy']: file_types['data']+=1
        else: file_types['other']+=1
    return file_types, exec_files

def audit_file(path):
    text=path.read_text(errors='ignore')[:200000]
    flags=[]
    for pat in SUSPICIOUS_PATTERNS:
        if re.search(pat, text, re.I):
            flags.append(pat)
    return flags

def cl> QUANTARION RESEARCH FIREWALL v0.1 — READ-ONLY PROTOTYPE
utbound HTTP detected: {'requests.' in str(exec_flags)}
  ⚠ subprocess detected: > Android-friendly (Termux), no auto-exec, no deletion, no creds.
rgv[2]
    src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"> Commands: scan, hash, provenance, claims, audit
    e> """

QUANTARION RESEARCH FIREWALL v0.1 — READ-ONLY PROTOTYPE
Android-friendly (Termux), no auto-exec, no deletion, no creds.
Commands: scan, hash, provenance, claims, audit
: command not found
~ $ import hashlib, os, re, json, sys, pathlib, datetime, mimetypes
The program import is not installed. Install it by executing:
 pkg install imagemagick
~ $ from collections import Counter
The program from is not installed. Install it by executing:
 pkg install mailutils
~ $
~ $ SUSPICIOUS_PATTERNS = [
SUSPICIOUS_PATTERNS: command not found
~ $     r"ignore\s+previous\s+instructions",
rignore\s+previous\s+instructions,: command not found
~ $     r"send\s+your\s+credentials",
rsend\s+your\s+credentials,: command not found
~ $     r"execute\s+this\s+command",
rexecute\s+this\s+command,: command not found
~ $     r"download\s+this\s+payload",
       print(json.dumps(provenancerdownload\s+this\s+payload,: command not found
~ $     r"paste\s+your\s+API\s+key",
rpaste\s+your\s+API\s+key,: command not found
~ $     r"disable\s+security",
=="report":
     rdisable\s+security,: command not found
~ $     r"os\.system\(",
ros\.system\(,: command not found
~ $     r"subprocess\.",
c, path)
    else:
  rsubprocess\.,: command not found
~ $     r"requests\.(get|post)\(",
      print("unknown cmd")
rrequests\.(get|post)\(,: command not found
~ $     r"socket\.",
rsocket\.,: command not found
~ $     r"eval\(",
reval\(,: command not found
~ $     r"base64\.b64decode",
rbase64\.b64decode,: command not found
~ $ ]
No command ] found, did you mean:
 Command [ in package coreutils
 Command k in package kona
 Command o in package orbiton
 Command q in package q-dns-client
 Command X in package xorg-server from the x11-repo repository
~ $
~ $ CLAIM_PATTERNS = [
CLAIM_PATTERNS: command not found
~ $     r"THEOREM\s+PROVEN",
rTHEOREM\s+PROVEN,: command not found
~ $     r"PROOF\s+COMPLETE",
rPROOF\s+COMPLETE,: command not found
~ $     r"publication\s+candidate",
rpublication\s+candidate,: command not found
~ $     r"world[- ]class",
rworld[- ]class,: command not found
~ $     r"production\s+certified",
rproduction\s+certified,: command not found
~ $     r"CLOSED\s+—\s+explicit",
rCLOSED\s+—\s+explicit,: command not found
~ $ ]
No command ] found, did you mean:
 Command [ in package coreutils
 Command k in package kona
 Command o in package orbiton
 Command q in package q-dns-client
 Command X in package xorg-server from the x11-repo repository
~ $
~ $ def sha256_file(p):
bash: syntax error near unexpected token `('
~ $     h=hashlib.sha256()
bash: syntax error near unexpected token `('
~ $     with open(p,'rb') as f:
bash: syntax error near unexpected token `('
~ $         for chunk in iter(lambda: f.read(8192), b''):
bash: syntax error near unexpected token `('
~ $             h.update(chunk)
bash: syntax error near unexpected token `chunk'
~ $     return h.hexdigest()
bash: syntax error near unexpected token `('
~ $
~ $ def scan_repo(root):
bash: syntax error near unexpected token `('
~ $     root=pathlib.Path(root)
bash: syntax error near unexpected token `('
~ $     files=list(root.rglob('*'))
bash: syntax error near unexpected token `('
~ $     file_types=Counter()
bash: syntax error near unexpected token `('
~ $     exec_files=[]
~ $     for f in files:
>         if f.is_dir(): continue
bash: syntax error near unexpected token `if'
~ $         ext=f.suffix.lower()
bash: syntax error near unexpected token `('
~ $         if ext in ['.py','.sh','.js','.ts']:
>             exec_files.append(f)
bash: syntax error near unexpected token `f'
~ $             file_types['python' if ext=='.py' else ext]+=1
bash: 'python' if ext=='.py' else ext: arithmetic syntax error: operand expected (error token is "'python' if ext=='.py' else ext")
~ $         elif ext in ['.ipynb']: file_types['notebooks']+=1
bash: syntax error near unexpected token `elif'
~ $         elif ext in ['.bin','.pt','.onnx','.safetensors']: file_types['models']+=1
bash: syntax error near unexpected token `elif'
~ $         elif ext in ['.csv','.jsonl','.parquet','.npy']: file_types['data']+=1
bash: syntax error near unexpected token `elif'
~ $         else: file_types['other']+=1
No command else: found, did you mean:
 Command plser in package libgnustep-base
~ $     return file_types, exec_files
bash: return: file_types,: numeric argument required
bash: return: can only `return' from a function or sourced script
~ $
~ $ def audit_file(path):
bash: syntax error near unexpected token `('
~ $     text=path.read_text(errors='ignore')[:200000]
bash: syntax error near unexpected token `('
~ $     flags=[]
~ $     for pat in SUSPICIOUS_PATTERNS:
>         if re.search(pat, text, re.I):
bash: syntax error near unexpected token `if'
~ $             flags.append(pat)
bash: syntax error near unexpected token `pat'
~ $     return flags
bash: return: flags: numeric argument required
bash: return: can only `return' from a function or sourced script
~ $
~ $ def claims_scan(path):
bash: syntax error near unexpected token `('
~ $     text=path.read_text(errors='ignore')
bash: syntax error near unexpected token `('
~ $     found=[]
~ $     for pat in CLAIM_PATTERNS:
>         m=re.findall(pat, text, re.I)
bash: syntax error near unexpected token `m=re.findall'
~ $         if m: found.extend(m)
bash: syntax error near unexpected token `('
~ $     return found
bash: return: found: numeric argument required
bash: return: can only `return' from a function or sourced script
~ $
~ $ def provenance_record(source_url, root):
bash: syntax error near unexpected token `('
~ $     root=pathlib.Path(root)
bash: syntax error near unexpected token `('
~ $     manifest={
~ $         "source": source_url,
No command source: found, did you mean:
 Command bounce in package mesa-demos from the x11-repo repository
 Command pounce in package pounce
 Command sorter in package sleuthkit
~ $         "timestamp": datetime.datetime.utcnow().isoformat()+"Z",
bash: syntax error near unexpected token `('
~ $         "root": str(root),
bash: syntax error near unexpected token `('
~ $         "files": [],
No command files: found, did you mean:
 Command file in package file
~ $         "sha256_root": "",
sha256_root:: command not found
~ $     }
bash: syntax error near unexpected token `}'
~ $     all_hashes=[]
~ $     for f in root.rglob('*'):
bash: syntax error near unexpected token `('
~ $         if f.is_file():
bash: syntax error near unexpected token `:'
~ $             try:
No command try: found, did you mean:
 Command tr in package coreutils
 Command tred in package graphviz
 Command tri in package mesa-demos from the x11-repo repository
 Command tree in package tree
 Command trz in package trzsz-go
 Command ttyc in package ttyc
 Command ttyd in package ttyd
 Command ty in package ty
~ $                 h=sha256_file(f)
bash: syntax error near unexpected token `('
~ $                 all_hashes.append(h)
bash: syntax error near unexpected token `h'
~ $                 manifest["files"].append({"path": str(f.relative_to(root)), "sha256": h, "size": f.stat().st_size})
bash: syntax error near unexpected token `{"path":'
~ $             except: pass
No command except: found, did you mean:
 Command expect in package expect
 Command exceltex in package texlive-bin
~ $     manifest["sha256_root"]=hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()[:16]
bash: syntax error near unexpected token `('
~ $     return manifest
bash: return: manifest: numeric argument required
bash: return: can only `return' from a function or sourced script
~ $
~ $ def firewall_report(source, root):
bash: syntax error near unexpected token `('
~ $     ftypes, exec_files = scan_repo(root)
bash: syntax error near unexpected token `('
~ $     prov = provenance_record(source, root)
bash: syntax error near unexpected token `('
~ $     # aggregate flags
~ $     exec_flags=[]
~ $     injection_flags=0
~ $     for ef in exec_files[:50]:  # sample first 50 for speed
>         fl=audit_file(ef)
bash: syntax error near unexpected token `fl=audit_file'
~ $         if fl: exec_flags.extend(fl)
bash: syntax error near unexpected token `('
~ $     claim_counts=0
~ $     for f in pathlib.Path(root).rglob('*.md'):
bash: syntax error near unexpected token `('
~ $         claim_counts+=len(claims_scan(f))
bash: syntax error near unexpected token `('
~ $
~ $     print(f"""
> QUANTARION FIREWALL REPORT
> SOURCE
>   {source}
>
> INTEGRITY
>   SHA-256 root: {prov['sha256_root']}....
>   files indexed: {len(prov['files'])}
>   timestamp: {prov['timestamp']}
>
> FILES
>   Python: {ftypes.get('python',0)}
>   notebooks: {ftypes.get('notebooks',0)}
>   models: {ftypes.get('models',0)}
>   data: {ftypes.get('data',0)}
>   other: {ftypes.get('other',0)}
>
> EXECUTABLE CODE
>   ⚠ {len(exec_files)} files
>   ⚠ outbound HTTP detected: {'requests.' in str(exec_flags)}
>   ⚠ subprocess detected: {'subprocess' in str(exec_flags)}
>
> PROMPT-INJECTION SIGNALS
>   {len([f for f in exec_flags if 'ignore' in f or 'credentials' in f])} flagged strings
>
> SCIENTIFIC CLAIMS
>   {claim_counts} identified in README/docs
>
> VERDICT
>   🟠 READABLE
>   🔴 DO NOT EXECUTE AUTOMATICALLY
> """)
bash: syntax error near unexpected token `$'f"""\nQUANTARION FIREWALL REPORT\nSOURCE\n  {source}\n\nINTEGRITY\n  SHA-256 root: {prov[\'sha256_root\']}....\n  files indexed: {len(prov[\'files\'])}\n  timestamp: {prov[\'timestamp\']}\n\nFILES\n  Python: {ftypes.get(\'python\',0)}\n  notebooks: {ftypes.get(\'notebooks\',0)}\n  models: {ftypes.get(\'models\',0)}\n  data: {ftypes.get(\'data\',0)}\n  other: {ftypes.get(\'other\',0)}\n\nEXECUTABLE CODE\n  ⚠ {len(exec_files)} files\n  ⚠ outbound HTTP detected: {\'requests.\' in str(exec_flags)}\n  ⚠ subprocess detected: {\'subprocess\' in str(exec_flags)}\n\nPROMPT-INJECTION SIGNALS\n  {len([f for f in exec_flags if \'ignore\' in f or \'credentials\' in f])} flagged strings\n\nSCIENTIFIC CLAIMS\n  {claim_counts} identified in README/docs\n\nVERDICT\n  🟠 READABLE\n  🔴 DO NOT EXECUTE AUTOMATICALLY\n"""''
~ $     return prov
bash: return: prov: numeric argument required
bash: return: can only `return' from a function or sourced script
~ $
~ $ if __name__=="__main__":
>     if len(sys.argv)<3:
bash: syntax error near unexpected token `sys.argv'
~ $         print("Usage: qrf_scanner.py [scan|hash|claims|audit|provenance] <path> [source_url]")
bash: syntax error near unexpected token `"Usage: qrf_scanner.py [scan|hash|claims|audit|provenance] <path> [source_url]"'
~ $         sys.exit(1)
bash: syntax error near unexpected token `1'
~ $     cmd=sys.argv[1]
~ $     path=sys.argv[2]
~ $     src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"
bash: syntax error near unexpected token `('
~ $     if cmd=="scan":
>         ft,_=scan_repo(path)
bash: syntax error near unexpected token `path'
~ $         print(ft)
bash: syntax error near unexpected token `ft'
~ $     elif cmd=="hash":
bash: syntax error near unexpected token `elif'
~ $         print(sha256_file(pathlib.Path(path)))
bash: syntax error near unexpected token `sha256_file'
~ $     elif cmd=="claims":
bash: syntax error near unexpected token `elif'
~ $         print(claims_scan(pathlib.Path(path)))
bash: syntax error near unexpected token `claims_scan'
~ $     elif cmd=="audit":
bash: syntax error near unexpected token `elif'
~ $         print(audit_file(pathlib.Path(path)))
bash: syntax error near unexpected token `audit_file'
~ $     elif cmd=="provenance":
bash: syntax error near unexpected token `elif'
~ $         print(json.dumps(provenance_record(src, path), indent=2))
bash: syntax error near unexpected token `json.dumps'
~ $     elif cmd=="report":
bash: syntax error near unexpected token `elif'
~ $         firewall_report(src, path)
bash: syntax error near unexpected token `src,'
~ $     else:
No command else: found, did you mean:
 Command plser in package libgnustep-base
~ $         print("unknown cmd")
bash: syntax error near unexpected token `"unknown cmd"'
~ $
~ $ unknown cmd
unknown: command not found
~ $ python qrf_scanner.py report ./downloaded_repo hf://quantarion-ai
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ python qrf_scanner.py provenance ./repo hf://...
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ python qrf_scanner.py scan ./repo
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ python qrf_scanner.py report ./downloaded_repo hf://quantarion-ai
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ python qrf_scanner.py provenance ./repo hf://...
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ python qrf_scanner.py scan ./repo
/data/data/com.termux/files/usr/bin/python: can't open file '/data/data/com.termux/files/home/qrf_scanner.py': [Errno 2] No such file or directory
~ $ pkg update -y && pkg upgrade -y
Hit:1 https://termux.net stable InRelease
All packages are up to date.
Hit:1 https://termux.net stable InRelease
All packages are up to date.
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
~ $ pkg install -y python git nano termux-tools
python is already the newest version (3.13.13-1).
git is already the newest version (2.54.0).
nano is already the newest version (9.1).
termux-tools is already the newest version (3.0.9).
Summary:
  Upgrading: 0, Installing: 0, Removing: 0, Not Upgrading: 0
~ $ termux-setup-storage

It appears that directory '~/storage' already exists.
This script is going to rebuild its structure from
scratch, wiping all dangling files. The actual storage
content IS NOT going to be deleted.

Do you want to continue? (y/n) mkdir -p ~/qrf ~/qrf/repos ~/qrf/ledger
Aborting configuration and leaving directory '~/storage' intact.
~ $ cd ~/qrfnano qrf_scanner.py
bash: cd: too many arguments
~ $ # paste the file I gave you, Ctrl+O, Enter, Ctrl+X~ $ chmod +x qrf_scanner.py
chmod: cannot access 'qrf_scanner.py': No such file or directory
~ $ curl -L https://your-raw-url/qrf_scanner.py -o qrf_scanner.py
curl: (6) Could not resolve host: your-raw-url
~ $ chmod +x qrf_scanner.py
chmod: cannot access 'qrf_scanner.py': No such file or directory
~ $ python -m py_compile qrf_scanner.py
[Errno 2] No such file or directory: 'qrf_scanner.py'~~ $ cat > qrf <<'EOF'
h
python ~/qrf/qrf_scanner.py "$@"
EOF
chmod +x qrf
mkdir -p ~/.termux/bin
mv qrf ~/.termux/bin/
# restart Termux or:
source ~/.bashrc> #!/data/data/com.termux/files/usr/bin/bash
> python ~/qrf/qrf_scanner.py "$@"
> EOF
~ $ chmod +x qrf
~ $ mkdir -p ~/.termux/bin
~ $ mv qrf ~/.termux/bin/
~ $ # restart Termux or:
~ $ source ~/.bashrc
bash: /data/data/com.termux/files/home/.bashrc: No such file or directory
~ $ cd ~
~ $ mkdir -p ~/qrf ~/qrf/repos ~/qrf/ledger ~/bin
~ $ cd ~/qrf
~/qrf $ pwd
/data/data/com.termux/files/home/qrf
~/qrf $ ls -la
total 14
drwx------.  4 u0_a352 u0_a352 3452 Sep 11 03:25 .
drwx------. 18 u0_a352 u0_a352 3452 Sep 11 03:25 ..
drwx------.  2 u0_a352 u0_a352 3452 Sep 11 03:25 ledger
drwx------.  2 u0_a352 u0_a352 3452 Sep 11 03:25 repos
~/qrf $ nano qrf_scanner.py
~/qrf $ ls -lh qrf_scanner.py
-rw-------. 1 u0_a352 u0_a352 3.7K Sep 11 03:27 qrf_scanner.py
~/qrf $ python qrf_scanner.py
Usage: python qrf_scanner.py [scan|hash|claims|audit|provenance|report] <path> [source_url]
~/qrf $ # should print Usage:...
~/qrf $ echo 'export PATH=$PATH:~/bin' >> ~/.bashrc
~/qrf $ echo 'export PATH=$PATH:~/bin' >> ~/.profile
~/qrf $ export PATH=$PATH:~/bin
~/qrf $ qrf report ~/qrf hf://test
No command qrf found, did you mean:
 Command arj in package arj
 Command ark in package ark from the x11-repo repository
 Command buf in package buf
 Command pr in package coreutils
 Command r8 in package d8
 Command duf in package duf
 Command ef in package electric-fence
 Command erl in package erlang
 Command fff in package fff
 Command fzf in package fzf
 Command era in package geth-utils
 Command grn in package groff
 Command gsf in package gsf-tools
 Command krfb in package krfb from the x11-repo repository
 Command lf in package lf
 Command ar in package llvm
 Command lr in package lr
 Command lrb in package lrzsz
 Command frm in package mailutils
 Command tri in package mesa-demos from the x11-repo repository
 Command mrd in package mtools
 Command mr in package myrepos
 Command arp in package net-tools
 Command rmf in package nmh
 Command q in package q-dns-client
 Command qpdf in package qpdf
 Command qml in package qt5-qtdeclarative from the x11-repo repository
 Command qev in package qt5-qttools from the x11-repo repository
 Command qjs in package quickjs-ng
 Command qs in package quickshell from the x11-repo repository
 Command r2 in package radare2
 Command rc in package rc
 Command qcp in package renameutils
 Command rg in package ripgrep
 Command rq in package rq
 Command erb in package ruby
 Command ri in package ruby-ri
 Command srm in package secure-delete
 Command surf in package surf from the x11-repo repository
 Command sr in package surfraw
 Command df in package termux-tools
 Command mf in package texlive-bin
 Command tf in package tinyfugue
 Command trz in package trzsz-go
 Command wrk in package wrk
~/qrf $ cd ~/qrf
~/qrf $ cat > ~/bin/qrf <<'ENDOFFILE'
> #!/data/data/com.termux/files/usr/bin/bash
> python ~/qrf/qrf_scanner.py "$@"
> ENDOFFILE
~/qrf $ chmod +x ~/bin/qrf
~/qrf $ ls -lh ~/bin/qrf
-rwx------. 1 u0_a352 u0_a352 76 Sep 11 03:29 /data/data/com.termux/files/home/bin/qrf
~/qrf $ ~/bin/qrf report ~/qrf hf://test
/data/data/com.termux/files/home/qrf/qrf_scanner.py:38: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  root=pathlib.Path(root); manifest={"source":source_url,"timestamp":datetime.datetime.utcnow().isoformat()+"Z","root":str(root),"files":[]}

QUANTARION FIREWALL REPORT
SOURCE hf://test
INTEGRITY SHA-256 root: e4c1784f868d7f62 files:1
FILES Python:1 notebooks:0 models:0 data:0
EXEC CODE 1 files outbound:False subprocess:False
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf $ cd ~/qrf/repos
~/qrf/repos $ git clone --depth 1 https://github.com/psf/requests
Cloning into 'requests'...
remote: Enumerating objects: 153, done.
remote: Counting objects: 100% (153/153), done.
remote: Compressing objects: 100% (135/135), done.
Receiving objects:  48% (74/153), 596.00 KiB | 1.13 MiReceiving objects:  48% (74/153), 1.50 MiB | 1.48 MiB/Receiving objects:  49% (75/153), 1.50 MiB | 1.48 MiB/Receiving objects:  50% (77/153), 1.50 MiB | 1.48 MiB/Receiving objects:  51% (79/153), 1.50 MiB | 1.48 MiB/Receiving objects:  52% (80/153), 1.50 MiB | 1.48 MiB/Receiving objects:  53% (82/153), 1.50 MiB | 1.48 MiB/Receiving objects:  54% (83/153), 1.50 MiB | 1.48 MiB/Receiving objects:  55% (85/153), 1.50 MiB | 1.48 MiB/Receiving objects:  56% (86/153), 1.50 MiB | 1.48 MiB/Receiving objects:  57% (88/153), 1.50 MiB | 1.48 MiB/Receiving objects:  58% (89/153), 1.50 MiB | 1.48 MiB/Receiving objects:  59% (91/153), 1.50 MiB | 1.48 MiB/Receiving objects:  60% (92/153), 1.50 MiB | 1.48 MiB/Receiving objects:  61% (94/153), 1.50 MiB | 1.48 MiB/Receiving objects:  62% (95/153), 1.50 MiB | 1.48 MiB/Receiving objects:  63% (97/153), 1.50 MiB | 1.48 MiB/Receiving objects:  64% (98/153), 1.50 MiB | 1.48 MiB/Receiving objects:  65% (100/153), 1.50 MiB | 1.48 MiBReceiving objects:  66% (101/153), 1.50 MiB | 1.48 MiBReceiving objects:  67% (103/153), 1.50 MiB | 1.48 MiBReceiving objects:  68% (105/153), 1.50 MiB | 1.48 MiBReceiving objects:  69% (106/153), 1.50 MiB | 1.48 MiBReceiving objects:  70% (108/153), 1.50 MiB | 1.48 MiBReceiving objects:  71% (109/153), 1.50 MiB | 1.48 MiBReceiving objects:  72% (111/153), 1.50 MiB | 1.48 MiBReceiving objects:  73% (112/153), 1.50 MiB | 1.48 MiBReceiving objects:  74% (114/153), 1.50 MiB | 1.48 MiBReceiving objects:  75% (115/153), 1.50 MiB | 1.48 MiBReceiving objects:  76% (117/153), 1.50 MiB | 1.48 MiBReceiving objects:  77% (118/153), 1.50 MiB | 1.48 MiBReceiving objects:  78% (120/153), 1.50 MiB | 1.48 MiBremote: Total 153 (delta 7), reused 72 (delta 7), pack-reused 0 (from 0)
Receiving objects:  79% (121/153), 1.50 MiB | 1.48 MiBReceiving objects:  80% (123/153), 1.50 MiB | 1.48 MiBReceiving objects:  81% (124/153), 1.50 MiB | 1.48 MiBReceiving objects:  82% (126/153), 1.50 MiB | 1.48 MiBReceiving objects:  83% (127/153), 1.50 MiB | 1.48 MiBReceiving objects:  84% (129/153), 1.50 MiB | 1.48 MiBReceiving objects:  85% (131/153), 1.50 MiB | 1.48 MiBReceiving objects:  86% (132/153), 1.50 MiB | 1.48 MiBReceiving objects:  87% (134/153), 1.50 MiB | 1.48 MiBReceiving objects:  88% (135/153), 1.50 MiB | 1.48 MiBReceiving objects:  89% (137/153), 1.50 MiB | 1.48 MiBReceiving objects:  90% (138/153), 1.50 MiB | 1.48 MiBReceiving objects:  91% (140/153), 1.50 MiB | 1.48 MiBReceiving objects:  92% (141/153), 1.50 MiB | 1.48 MiBReceiving objects:  93% (143/153), 1.50 MiB | 1.48 MiBReceiving objects:  94% (144/153), 1.50 MiB | 1.48 MiBReceiving objects:  95% (146/153), 1.50 MiB | 1.48 MiBReceiving objects:  96% (147/153), 1.50 MiB | 1.48 MiBReceiving objects:  97% (149/153), 1.50 MiB | 1.48 MiBReceiving objects:  98% (150/153), 1.50 MiB | 1.48 MiBReceiving objects:  99% (152/153), 1.50 MiB | 1.48 MiBReceiving objects: 100% (153/153), 1.50 MiB | 1.48 MiBReceiving objects: 100% (153/153), 3.01 MiB | 2.02 MiB/s, done.
Resolving deltas: 100% (7/7), done.
~/qrf/repos $ ~/bin/qrf report ./requests https://github.com/psf/requests > ~/qrf/ledger/requests_$(date +%F).txt
/data/data/com.termux/files/home/qrf/qrf_scanner.py:38: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  root=pathlib.Path(root); manifest={"source":source_url,"timestamp":datetime.datetime.utcnow().isoformat()+"Z","root":str(root),"files":[]}
~/qrf/repos $ cat ~/qrf/ledger/requests_*.txt

QUANTARION FIREWALL REPORT
SOURCE https://github.com/psf/requests
INTEGRITY SHA-256 root: 61d029cd257ebb4c files:157
FILES Python:37 notebooks:0 models:0 data:0
EXEC CODE 37 files outbound:False subprocess:False
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf/repos $ cd ~/qrf
y:
                h=sha256_file(f); all_hashes.append(h)
                manifest["files"].append({"path":str(f.relative_to(root)),"sha256":h,"size":f.stat().st_size})
            except: pass
    manifest["sha256_root"]=hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()[:16]
    return manifest
def firewall_report(source, root):
    ft, exec_files = scan_repo(root)
    prov = provenance_record(source, root)
    exec_flags=[]
    for ef in exec_files[:100]:
        exec_flags.extend(audit_file(ef))
    claim_counts=sum(len(claims_scan(f)) for f in pathlib.Path(root).rglob('*.md'))
    print(f"\nQUANTARION FIREWALL REPORT\nSOURCE {source}\nINTEGRITY SHA-256 root: {prov['sha256_root']} files:{len(prov['files'])}\nFILES Python:{ft.get('python',0)} notebooks:{ft.get('notebooks',0)} models:{ft.get('models',0)} data:{ft.get('data',0)}\nEXEC CODE {len(exec_files)} files\nPROMPT-INJECTION {len([f for f in exec_flags if 'ignore' in f])}\nCLAIMS {claim_counts}\nVERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY\n")
    return prov
if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: python qrf_scanner.py [scan|hash|claims|audit|provenance|report] <path> [source_url]")
        sys.exit(1)
    cmd=sys.argv[1]; path=sys.argv[2]; src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"
    p=pathlib.Path(path)
    if cmd=="scan": print(scan_repo(path)[0])
    elif cmd=="hash": print(sha256_file(p))
    elif cmd=="claims": print(claims_scan(p))
    elif cmd=="audit": print(audit_file(p))
    elif cmd=="provenance": print(json.dumps(provenance_record(src, path), indent=2))
    elif cmd=="report": firewall_report(src, path)
PYEOF
chmod +x qrf_scanner.py
python qrf_scanner.py report ~/qrf hf://test~/qrf $ rm -f qrf_scanner.py
~/qrf $ cat > qrf_scanner.py <<'PYEOF'
> #!/usr/bin/env python3
> import hashlib, re, json, sys, pathlib, datetime
> from collections import Counter
> SUSPICIOUS = [r"ignore\s+previous\s+instructions", r"send\s+your\s+credentials", r"execute\s+this\s+command", r"download\s+this\s+payload", r"paste\s+your\s+API\s+key", r"disable\s+security", r"os\.system\(", r"subprocess\.", r"requests\.(get|post)\(", r"socket\.", r"eval\(", r"base64\.b64decode"]
> CLAIMS = [r"THEOREM\s+PROVEN", r"PROOF\s+COMPLETE", r"publication\s+candidate", r"world[- ]class", r"production\s+certified"]
> def sha256_file(p):
>     h=hashlib.sha256()
>     with open(p,'rb') as f:
>         for c in iter(lambda: f.read(8192), b''): h.update(c)
>     return h.hexdigest()
> def scan_repo(root):
>     root=pathlib.Path(root); ft=Counter(); exec_files=[]
>     for f in root.rglob('*'):
>         if f.is_dir(): continue
>         ext=f.suffix.lower()
>         if ext in ['.py','.sh','.js','.ts']: exec_files.append(f); ft['python' if ext=='.py' else ext]+=1
>         elif ext=='.ipynb': ft['notebooks']+=1
>         elif ext in ['.bin','.pt','.onnx','.safetensors']: ft['models']+=1
>         elif ext in ['.csv','.jsonl','.parquet','.npy']: ft['data']+=1
>         else: ft['other']+=1
>     return ft, exec_files
> def audit_file(path):
>     try: text=path.read_text(errors='ignore')[:200000]
>     except: return []
>     return [pat for pat in SUSPICIOUS if re.search(pat, text, re.I)]
> def claims_scan(path):
>     try: text=path.read_text(errors='ignore')
>     except: return []
>     found=[]
>     for pat in CLAIMS:
>         m=re.findall(pat, text, re.I)
>         if m: found.extend(m)
>     return found
> def provenance_record(source_url, root):
>     root=pathlib.Path(root)
>     manifest={"source":source_url,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"root":str(root),"files":[]}
>     all_hashes=[]
>     for f in root.rglob('*'):
>         if f.is_file():
>             try:
>                 h=sha256_file(f); all_hashes.append(h)
>                 manifest["files"].append({"path":str(f.relative_to(root)),"sha256":h,"size":f.stat().st_size})
>             except: pass
>     manifest["sha256_root"]=hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()[:16]
>     return manifest
> def firewall_report(source, root):
>     ft, exec_files = scan_repo(root)
>     prov = provenance_record(source, root)
>     exec_flags=[]
>     for ef in exec_files[:100]:
>         exec_flags.extend(audit_file(ef))
>     claim_counts=sum(len(claims_scan(f)) for f in pathlib.Path(root).rglob('*.md'))
>     print(f"\nQUANTARION FIREWALL REPORT\nSOURCE {source}\nINTEGRITY SHA-256 root: {prov['sha256_root']} files:{len(prov['files'])}\nFILES Python:{ft.get('python',0)} notebooks:{ft.get('notebooks',0)} models:{ft.get('models',0)} data:{ft.get('data',0)}\nEXEC CODE {len(exec_files)} files\nPROMPT-INJECTION {len([f for f in exec_flags if 'ignore' in f])}\nCLAIMS {claim_counts}\nVERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY\n")
>     return prov
> if __name__=="__main__":
>     if len(sys.argv)<3:
>         print("Usage: python qrf_scanner.py [scan|hash|claims|audit|provenance|report] <path> [source_url]")
>         sys.exit(1)
>     cmd=sys.argv[1]; path=sys.argv[2]; src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"
>     p=pathlib.Path(path)
>     if cmd=="scan": print(scan_repo(path)[0])
>     elif cmd=="hash": print(sha256_file(p))
>     elif cmd=="claims": print(claims_scan(p))
>     elif cmd=="audit": print(audit_file(p))
>     elif cmd=="provenance": print(json.dumps(provenance_record(src, path), indent=2))
>     elif cmd=="report": firewall_report(src, path)
> PYEOF
~/qrf $ chmod +x qrf_scanner.py
~/qrf $ python qrf_scanner.py report ~/qrf hf://test

QUANTARION FIREWALL REPORT
SOURCE hf://test
INTEGRITY SHA-256 root: a3afdaa41651e9c9 files:159
FILES Python:38 notebooks:0 models:0 data:0
EXEC CODE 38 files
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf $ /rag
bash: /rag: No such file or directory
~/qrf $ update
No command update found, did you mean:
 Command lupdate in package qt5-qttools from the x11-repo repository
~/qrf $ y
No command y found, did you mean:
 Command [ in package coreutils
 Command k in package kona
 Command o in package orbiton
 Command q in package q-dns-client
 Command ty in package ty
 Command X in package xorg-server from the x11-repo repository
 Command ya in package yazi
 Command yq in package yq
~/qrf $ ya
The program ya is not installed. Install it by executing:
 pkg install yazi
~/qrf $ y
No command y found, did you mean:
 Command [ in package coreutils
 Command k in package kona
 Command o in package orbiton
 Command q in package q-dns-client
 Command ty in package ty
 Command X in package xorg-server from the x11-repo repository
 Command ya in package yazi
 Command yq in package yq
~/qrf $ y
No command y found, did you mean:
 Command [ in package coreutils
 Command k in package kona
 Command o in package orbiton
 Command q in package q-dns-client
 Command ty in package ty
 Command X in package xorg-server from the x11-repo repository
 Command ya in package yazi
 Command yq in package yq
~/qrf $ yq
The program yq is not installed. Install it by executing:
 pkg install yq
~/qrf $ cd ~/qrf
 [r"ignore\s+previous\s+instructions", r"send\s+your\s+credentials", r"execute\s+this\s+command", r"download\s+this\s+payload", r"paste\s+your\s+API\s+key", r"disable\s+security", r"os\.system\(", r"subprocess\.", r"requests\.(get|post)\(", r"socket\.", r"eval\(", r"base64\.b64decode"]
CLAIMS = [r"THEOREM\s+PROVEN", r"PROOF\s+COMPLETE", r"publication\s+candidate", r"world[- ]class", r"production\s+certified"]
def sha256_file(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for c in iter(lambda: f.read(8192), b''): h.update(c)
    return h.hexdigest()
def scan_repo(root):
    root=pathlib.Path(root); ft=Counter(); exec_files=[]
    for f in root.rglob('*'):
        if f.is_dir(): continue
        ext=f.suffix.lower()
        if ext in ['.py','.sh','.js','.ts']: exec_files.append(f); ft['python' if ext=='.py' else ext]+=1
        elif ext=='.ipynb': ft['notebooks']+=1
        elif ext in ['.bin','.pt','.onnx','.safetensors']: ft['models']+=1
        elif ext in ['.csv','.jsonl','.parquet','.npy']: ft['data']~/qrf $ rm -f qrf_scanner.py
ath.read_text(errors='ignore')
    except: return []
    found=[]
    for pat in CLAIMS:
        m=re.findall(pat, text, re.I)
        if m: found.extend(m)
    return found
def provenance_record(source_url, root):
    root=pathlib.Path(root)
    manifest={"source":source_url,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"root":str(root),"files":[]}
    all_hashes=[]
    for f in root.rglob('*'):
        if f.is_file():
            try:
                h=sha256_file(f); all_hashes.append(h)
                manifest["files"].append({"path":str(f.relative_to(root)),"sha256":h,"size":f.stat().st_size})
            except: pass
    manifest["sha256_root"]=hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()[:16]
    return manifest
def firewall_report(source, root):
    ft, exec_files = scan_repo(root)
    prov = provenance_record(source, root)
    exec_flags=[]
    for ef in exec_files[:100]:
        exec_flags.extend(audit_file(ef))
    claim_counts=sum(len(claims_scan(f)) for f in pathlib.Path(root).rglob('*.md'))
    print(f"\nQUANTARION FIREWALL REPORT\nSOURCE {source}\nINTEGRITY SHA-256 root: {prov['sha256_root']} files:{len(prov['files'])}\nFILES Python:{ft.get('python',0)} notebooks:{ft.get('notebooks',0)} models:{ft.get('models',0)} data:{ft.get('data',0)}\nEXEC CODE {len(exec_files)} files\nPROMPT-INJECTION {len([f for f in exec_flags if 'ignore' in f])}\nCLAIMS {claim_counts}\nVERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY\n")
    return prov
if __name__=="__main__":
    if len(sys.argv)<3:
        print("Usage: python qrf_scanner.py [scan|hash|claims|audit|provenance|report] <path> [source_url]")
        sys.exit(1)
    cmd=sys.argv[1]; path=sys.argv[2]; src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"
    p=pathlib.Path(path)
    if cmd=="scan": print(scan_repo(path)[0])
    elif cmd=="hash": print(sha256_file(p))
    elif cmd=="claims": print(claims_scan(p))
    elif cmd=="audit": print(audit_file(p))
    elif cmd=="provenance": print(json.dumps(provenance_record(src, path), indent=2))
    elif cmd=="report": firewall_report(src, path)
PYEOF
chmod +x qrf_scanner.py
python qrf_scanner.py report ~/qrf hf://test~/qrf $ cat > qrf_scanner.py <<'PYEOF'
> #!/usr/bin/env python3
> import hashlib, re, json, sys, pathlib, datetime
> from collections import Counter
> SUSPICIOUS = [r"ignore\s+previous\s+instructions", r"send\s+your\s+credentials", r"execute\s+this\s+command", r"download\s+this\s+payload", r"paste\s+your\s+API\s+key", r"disable\s+security", r"os\.system\(", r"subprocess\.", r"requests\.(get|post)\(", r"socket\.", r"eval\(", r"base64\.b64decode"]
> CLAIMS = [r"THEOREM\s+PROVEN", r"PROOF\s+COMPLETE", r"publication\s+candidate", r"world[- ]class", r"production\s+certified"]
> def sha256_file(p):
>     h=hashlib.sha256()
>     with open(p,'rb') as f:
>         for c in iter(lambda: f.read(8192), b''): h.update(c)
>     return h.hexdigest()
> def scan_repo(root):
>     root=pathlib.Path(root); ft=Counter(); exec_files=[]
>     for f in root.rglob('*'):
>         if f.is_dir(): continue
>         ext=f.suffix.lower()
>         if ext in ['.py','.sh','.js','.ts']: exec_files.append(f); ft['python' if ext=='.py' else ext]+=1
>         elif ext=='.ipynb': ft['notebooks']+=1
>         elif ext in ['.bin','.pt','.onnx','.safetensors']: ft['models']+=1
>         elif ext in ['.csv','.jsonl','.parquet','.npy']: ft['data']+=1
>         else: ft['other']+=1
>     return ft, exec_files
> def audit_file(path):
>     try: text=path.read_text(errors='ignore')[:200000]
>     except: return []
>     return [pat for pat in SUSPICIOUS if re.search(pat, text, re.I)]
> def claims_scan(path):
>     try: text=path.read_text(errors='ignore')
>     except: return []
>     found=[]
>     for pat in CLAIMS:
>         m=re.findall(pat, text, re.I)
>         if m: found.extend(m)
>     return found
> def provenance_record(source_url, root):
>     root=pathlib.Path(root)
>     manifest={"source":source_url,"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"root":str(root),"files":[]}
>     all_hashes=[]
>     for f in root.rglob('*'):
>         if f.is_file():
>             try:
>                 h=sha256_file(f); all_hashes.append(h)
>                 manifest["files"].append({"path":str(f.relative_to(root)),"sha256":h,"size":f.stat().st_size})
>             except: pass
>     manifest["sha256_root"]=hashlib.sha256("".join(sorted(all_hashes)).encode()).hexdigest()[:16]
>     return manifest
> def firewall_report(source, root):
>     ft, exec_files = scan_repo(root)
>     prov = provenance_record(source, root)
>     exec_flags=[]
>     for ef in exec_files[:100]:
>         exec_flags.extend(audit_file(ef))
>     claim_counts=sum(len(claims_scan(f)) for f in pathlib.Path(root).rglob('*.md'))
>     print(f"\nQUANTARION FIREWALL REPORT\nSOURCE {source}\nINTEGRITY SHA-256 root: {prov['sha256_root']} files:{len(prov['files'])}\nFILES Python:{ft.get('python',0)} notebooks:{ft.get('notebooks',0)} models:{ft.get('models',0)} data:{ft.get('data',0)}\nEXEC CODE {len(exec_files)} files\nPROMPT-INJECTION {len([f for f in exec_flags if 'ignore' in f])}\nCLAIMS {claim_counts}\nVERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY\n")
>     return prov
> if __name__=="__main__":
>     if len(sys.argv)<3:
>         print("Usage: python qrf_scanner.py [scan|hash|claims|audit|provenance|report] <path> [source_url]")
>         sys.exit(1)
>     cmd=sys.argv[1]; path=sys.argv[2]; src=sys.argv[3] if len(sys.argv)>3 else "PUBLIC INTERNET"
>     p=pathlib.Path(path)
>     if cmd=="scan": print(scan_repo(path)[0])
>     elif cmd=="hash": print(sha256_file(p))
>     elif cmd=="claims": print(claims_scan(p))
>     elif cmd=="audit": print(audit_file(p))
>     elif cmd=="provenance": print(json.dumps(provenance_record(src, path), indent=2))
>     elif cmd=="report": firewall_report(src, path)
> PYEOF
~/qrf $ chmod +x qrf_scanner.py
~/qrf $ python qrf_scanner.py report ~/qrf hf://test

QUANTARION FIREWALL REPORT
SOURCE hf://test
INTEGRITY SHA-256 root: a3afdaa41651e9c9 files:159
FILES Python:38 notebooks:0 models:0 data:0
EXEC CODE 38 files
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf $ cat > ~/bin/qrf <<'ENDOFFILE'
> #!/data/data/com.termux/files/usr/bin/bash
> python ~/qrf/qrf_scanner.py "$@"
> ENDOFFILE
~/qrf $ chmod +x ~/bin/qrf
~/qrf $ ~/bin/qrf report ~/qrf/repos/requests https://github.com/psf/requests

QUANTARION FIREWALL REPORT
SOURCE https://github.com/psf/requests
INTEGRITY SHA-256 root: 61d029cd257ebb4c files:157
FILES Python:37 notebooks:0 models:0 data:0
EXEC CODE 37 files
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf $ cd ~/qrf/repos
~/qrf/repos $ git clone --depth 1 https://github.com/Aqarion13/Quantarion 2>/dev/null || git -C Quantarion pull
Username for 'https://github.com': jasksg9
Password for 'https://~%2Fbin%2Fqrf%20report.%2FQuantarion%20https%3A%2F%2Fgithub.com%2FAqarion13%2FQuantarion%20%3E%20~%2Fqrf%2Fledger%2Fquantarion_%24%28date%20%2B%25F%29.txt%0D%0D%23%20HF%20read-only%2C%20no%20exec%0Dpip%20install%20-q%20huggingface_hub%0Dhf%20download%20Aqarion%2FQuantarion-ai%20--local-dir.%2FQuantarion-ai%20--local-dir-use-symlinks%20False%0D~%2Fbin%2Fqrf%20report.%2FQuantarion-ai%20hf%3A%2F%2FAqarion%2FQuantarion-ai%20%3E%20~%2Fqrf%2Fledger%2Fqrf_hf_%24%28date%20%2B%25F%29.txt%0D%0Dls%20-lh%20~%2Fqrf%2Fledger%2F%0Dcat%20~%2Fqrf%2Fledger%2F%2A.txtjasksg9@github.com':
fatal: cannot change to 'Quantarion': No such file or directory
~/qrf/repos $
~/qrf/repos $ # 2. Clear any cached attempt
~/qrf/repos $ git credential-cache exit 2>/dev/null
~/qrf/repos $ rm -f ~/.git-credentials
~/qrf/repos $ cd ~/qrf/repos
~/qrf/repos $ rm -rf Quantarion
~/qrf/repos $
~/qrf/repos $ # 3. Clone the REAL public repo with prompts disabled (it will fail instead of asking)
~/qrf/repos $ GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/Quantarion13/Quantarion
Cloning into 'Quantarion'...
fatal: could not read Username for 'https://github.com': terminal prompts disabled
~/qrf/repos $ GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
Cloning into 'AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-'...
remote: Enumerating objects: 582, done.
remote: Counting objects: 100% (582/582), done.
remote: Compressing objects: 100% (479/479), done.
Receiving objects:  35% (204/582), 5.90 MiB | 11.78 MiReceiving objects:  36% (210/582), 5.90 MiB | 11.78 MiReceiving objects:  37% (216/582), 5.90 MiB | 11.78 MiReceiving objects:  38% (222/582), 5.90 MiB | 11.78 MiReceiving objects:  39% (227/582), 5.90 MiB | 11.78 MiReceiving objects:  40% (233/582), 5.90 MiB | 11.78 MiReceiving objects:  41% (239/582), 5.90 MiB | 11.78 MiReceiving objects:  42% (245/582), 5.90 MiB | 11.78 MiReceiving objects:  43% (251/582), 5.90 MiB | 11.78 MiReceiving objects:  44% (257/582), 5.90 MiB | 11.78 MiReceiving objects:  45% (262/582), 5.90 MiB | 11.78 MiReceiving objects:  46% (268/582), 5.90 MiB | 11.78 MiReceiving objects:  47% (274/582), 5.90 MiB | 11.78 MiReceiving objects:  48% (280/582), 5.90 MiB | 11.78 MiReceiving objects:  49% (286/582), 5.90 MiB | 11.78 MiReceiving objects:  50% (291/582), 5.90 MiB | 11.78 MiReceiving objects:  51% (297/582), 5.90 MiB | 11.78 MiReceiving objects:  52% (303/582), 5.90 MiB | 11.78 MiReceiving objects:  53% (309/582), 5.90 MiB | 11.78 MiReceiving objects:  54% (315/582), 5.90 MiB | 11.78 MiReceiving objects:  55% (321/582), 5.90 MiB | 11.78 MiReceiving objects:  56% (326/582), 5.90 MiB | 11.78 MiReceiving objects:  57% (332/582), 5.90 MiB | 11.78 MiReceiving objects:  58% (338/582), 5.90 MiB | 11.78 MiReceiving objects:  59% (344/582), 5.90 MiB | 11.78 MiReceiving objects:  60% (350/582), 5.90 MiB | 11.78 MiReceiving objects:  60% (352/582), 15.84 MiB | 15.83 MReceiving objects:  61% (356/582), 15.84 MiB | 15.83 MReceiving objects:  62% (361/582), 15.84 MiB | 15.83 MReceiving objects:  63% (367/582), 15.84 MiB | 15.83 MReceiving objects:  64% (373/582), 15.84 MiB | 15.83 MReceiving objects:  65% (379/582), 15.84 MiB | 15.83 MReceiving objects:  66% (385/582), 15.84 MiB | 15.83 MReceiving objects:  67% (390/582), 15.84 MiB | 15.83 MReceiving objects:  68% (396/582), 15.84 MiB | 15.83 MReceiving objects:  69% (402/582), 15.84 MiB | 15.83 MReceiving objects:  70% (408/582), 15.84 MiB | 15.83 MReceiving objects:  71% (414/582), 15.84 MiB | 15.83 MReceiving objects:  72% (420/582), 15.84 MiB | 15.83 MReceiving objects:  73% (425/582), 15.84 MiB | 15.83 MReceiving objects:  74% (431/582), 15.84 MiB | 15.83 MReceiving objects:  75% (437/582), 15.84 MiB | 15.83 MReceiving objects:  76% (443/582), 15.84 MiB | 15.83 MReceiving objects:  77% (449/582), 15.84 MiB | 15.83 MReceiving objects:  78% (454/582), 15.84 MiB | 15.83 MReceiving objects:  79% (460/582), 15.84 MiB | 15.83 MReceiving objects:  80% (466/582), 15.84 MiB | 15.83 MReceiving objects:  81% (472/582), 15.84 MiB | 15.83 MReceiving objects:  82% (478/582), 15.84 MiB | 15.83 MReceiving objects:  83% (484/582), 15.84 MiB | 15.83 MReceiving objects:  84% (489/582), 15.84 MiB | 15.83 MReceiving objects:  85% (495/582), 15.84 MiB | 15.83 MReceiving objects:  86% (501/582), 15.84 MiB | 15.83 MReceiving objects:  87% (507/582), 15.84 MiB | 15.83 MReceiving objects:  88% (513/582), 15.84 MiB | 15.83 MReceiving objects:  89% (518/582), 15.84 MiB | 15.83 MReceiving objects:  90% (524/582), 15.84 MiB | 15.83 MReceiving objects:  91% (530/582), 15.84 MiB | 15.83 MReceiving objects:  92% (536/582), 23.98 MiB | 15.98 MReceiving objects:  93% (542/582), 23.98 MiB | 15.98 MReceiving objects:  94% (548/582), 23.98 MiB | 15.98 MReceiving objects:  95% (553/582), 23.98 MiB | 15.98 MReceiving objects:  96% (559/582), 23.98 MiB | 15.98 MReceiving objects:  97% (565/582), 23.98 MiB | 15.98 MReceiving objects:  98% (571/582), 23.98 MiB | 15.98 MReceiving objects:  99% (577/582), 23.98 MiB | 15.98 Mremote: Total 582 (delta 50), reused 522 (delta 45), pack-reused 0 (from 0)
Receiving objects: 100% (582/582), 23.98 MiB | 15.98 MReceiving objects: 100% (582/582), 27.93 MiB | 16.46 MiB/s, done.
Resolving deltas: 100% (50/50), done.
~/qrf/repos $
~/qrf/repos $ # 4. Now scan — ONE command at a time, don't paste the block
~/qrf/repos $ ~/bin/qrf report ~/qrf/repos/Quantarion https://github.com/Quantarion13/Quantarion > ~/qrf/ledger/quantarion_$(date +%F).txt
~/qrf/repos $ cat ~/qrf/ledger/quantarion_*.txt

QUANTARION FIREWALL REPORT
SOURCE https://github.com/Quantarion13/Quantarion
INTEGRITY SHA-256 root: e3b0c44298fc1c14 files:0
FILES Python:0 notebooks:0 models:0 data:0
EXEC CODE 0 files
PROMPT-INJECTION 0
CLAIMS 0
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf/repos $ cd ~/qrf/repos
-DYNAMICS-
GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/JASKSG9/MANDELBROT-INFINITE-DYNAMICS

~/bin/qrf report ./KAPREKAR-SPECTRAL-GEOMETRY https://github.com/JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY > ~/qrf/ledger/kaprekar_$(date +%F).txt
ls -lh ~/qrf/ledger/~/qrf/repos $ ls -lh
total 7.0K
drwx------. 16 u0_a352 u0_a352 3.4K Sep 11 04:17 AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
drwx------.  8 u0_a352 u0_a352 3.4K Sep 11 03:31 requests
~/qrf/repos $ # you should see AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
~/qrf/repos $
~/qrf/repos $ ~/bin/qrf report ./AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS- > ~/qrf/ledger/aqarion-arithmetic_$(date +%F).txt
~/qrf/repos $ cat ~/qrf/ledger/aqarion-arithmetic_*.txt

QUANTARION FIREWALL REPORT
SOURCE https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-
INTEGRITY SHA-256 root: 39286a58c81ed870 files:482
FILES Python:155 notebooks:0 models:0 data:0
EXEC CODE 164 files
PROMPT-INJECTION 0
CLAIMS 4
VERDICT 🟠 READABLE 🔴 DO NOT EXECUTE AUTOMATICALLY

~/qrf/repos $
~/qrf/repos $ # now grab the rest of your public research stack
~/qrf/repos $ GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY
Cloning into 'KAPREKAR-SPECTRAL-GEOMETRY'...

remote: Enumerating objects: 311, done.
remote: Counting objects: 100% (311/311), done.
remote: Compressing objects: 100% (256/256), done.
Receiving objects:   3% (10/311), 524.00 KiB | 1012.00Receiving objects:   4% (13/311), 524.00 KiB | 1012.00Receiving objects:   5% (16/311), 524.00 KiB | 1012.00Receiving objects:   6% (19/311), 524.00 KiB | 1012.00Receiving objects:   6% (21/311), 1.39 MiB | 1.36 MiB/Receiving objects:   7% (22/311), 1.39 MiB | 1.36 MiB/Receiving objects:   8% (25/311), 1.39 MiB | 1.36 MiB/Receiving objects:   9% (28/311), 1.39 MiB | 1.36 MiB/Receiving objects:  10% (32/311), 1.39 MiB | 1.36 MiB/Receiving objects:  11% (35/311), 1.39 MiB | 1.36 MiB/Receiving objects:  12% (38/311), 1.39 MiB | 1.36 MiB/Receiving objects:  13% (41/311), 1.39 MiB | 1.36 MiB/Receiving objects:  14% (44/311), 2.88 MiB | 1.90 MiB/Receiving objects:  15% (47/311), 2.88 MiB | 1.90 MiB/Receiving objects:  16% (50/311), 2.88 MiB | 1.90 MiB/Receiving objects:  17% (53/311), 2.88 MiB | 1.90 MiB/Receiving objects:  18% (56/311), 2.88 MiB | 1.90 MiB/Receiving objects:  18% (56/311), 5.34 MiB | 2.64 MiB/Receiving objects:  19% (60/311), 5.34 MiB | 2.64 MiB/Receiving objects:  20% (63/311), 5.34 MiB | 2.64 MiB/Receiving objects:  21% (66/311), 5.34 MiB | 2.64 MiB/Receiving objects:  22% (69/311), 5.34 MiB | 2.64 MiB/Receiving objects:  23% (72/311), 5.34 MiB | 2.64 MiB/Receiving objects:  24% (75/311), 5.34 MiB | 2.64 MiB/Receiving objects:  25% (78/311), 5.34 MiB | 2.64 MiB/Receiving objects:  26% (81/311), 5.34 MiB | 2.64 MiB/Receiving objects:  27% (84/311), 5.34 MiB | 2.64 MiB/Receiving objects:  28% (88/311), 5.34 MiB | 2.64 MiB/Receiving objects:  29% (91/311), 5.34 MiB | 2.64 MiB/Receiving objects:  30% (94/311), 5.34 MiB | 2.64 MiB/Receiving objects:  31% (97/311), 5.34 MiB | 2.64 MiB/Receiving objects:  32% (100/311), 5.34 MiB | 2.64 MiBReceiving objects:  33% (103/311), 5.34 MiB | 2.64 MiBReceiving objects:  34% (106/311), 5.34 MiB | 2.64 MiBReceiving objects:  35% (109/311), 5.34 MiB | 2.64 MiBReceiving objects:  36% (112/311), 5.34 MiB | 2.64 MiBReceiving objects:  37% (116/311), 5.34 MiB | 2.64 MiBReceiving objects:  38% (119/311), 5.34 MiB | 2.64 MiBReceiving objects:  39% (122/311), 5.34 MiB | 2.64 MiBReceiving objects:  40% (125/311), 5.34 MiB | 2.64 MiBReceiving objects:  41% (128/311), 5.34 MiB | 2.64 MiBReceiving objects:  42% (131/311), 5.34 MiB | 2.64 MiBReceiving objects:  43% (134/311), 5.34 MiB | 2.64 MiBReceiving objects:  44% (137/311), 5.34 MiB | 2.64 MiBReceiving objects:  45% (140/311), 5.34 MiB | 2.64 MiBReceiving objects:  46% (144/311), 5.34 MiB | 2.64 MiBReceiving objects:  47% (147/311), 5.34 MiB | 2.64 MiBReceiving objects:  48% (150/311), 5.34 MiB | 2.64 MiBReceiving objects:  49% (153/311), 5.34 MiB | 2.64 MiBReceiving objects:  50% (156/311), 5.34 MiB | 2.64 MiBReceiving objects:  51% (159/311), 5.34 MiB | 2.64 MiBReceiving objects:  52% (162/311), 5.34 MiB | 2.64 MiBReceiving objects:  53% (165/311), 5.34 MiB | 2.64 MiBReceiving objects:  54% (168/311), 5.34 MiB | 2.64 MiBReceiving objects:  55% (172/311), 5.34 MiB | 2.64 MiBReceiving objects:  56% (175/311), 5.34 MiB | 2.64 MiBReceiving objects:  57% (178/311), 5.34 MiB | 2.64 MiBReceiving objects:  58% (181/311), 5.34 MiB | 2.64 MiBReceiving objects:  59% (184/311), 5.34 MiB | 2.64 MiBReceiving objects:  60% (187/311), 5.34 MiB | 2.64 MiBReceiving objects:  61% (190/311), 5.34 MiB | 2.64 MiBReceiving objects:  62% (193/311), 5.34 MiB | 2.64 MiBReceiving objects:  63% (196/311), 5.34 MiB | 2.64 MiBReceiving objects:  64% (200/311), 5.34 MiB | 2.64 MiBReceiving objects:  65% (203/311), 5.34 MiB | 2.64 MiBReceiving objects:  66% (206/311), 5.34 MiB | 2.64 MiBReceiving objects:  67% (209/311), 5.34 MiB | 2.64 MiBReceiving objects:  68% (212/311), 5.34 MiB | 2.64 MiBReceiving objects:  69% (215/311), 5.34 MiB | 2.64 MiBReceiving objects:  70% (218/311), 5.34 MiB | 2.64 MiBReceiving objects:  71% (221/311), 5.34 MiB | 2.64 MiBReceiving objects:  72% (224/311), 5.34 MiB | 2.64 MiBReceiving objects:  73% (228/311), 5.34 MiB | 2.64 MiBReceiving objects:  74% (231/311), 9.54 MiB | 3.79 MiBReceiving objects:  75% (234/311), 9.54 MiB | 3.79 MiBReceiving objects:  76% (237/311), 9.54 MiB | 3.79 MiBReceiving objects:  77% (240/311), 9.54 MiB | 3.79 MiBReceiving objects:  78% (243/311), 9.54 MiB | 3.79 MiBReceiving objects:  79% (246/311), 9.54 MiB | 3.79 MiBReceiving objects:  80% (249/311), 9.54 MiB | 3.79 MiBReceiving objects:  81% (252/311), 9.54 MiB | 3.79 MiBReceiving objects:  82% (256/311), 9.54 MiB | 3.79 MiBReceiving objects:  83% (259/311), 9.54 MiB | 3.79 MiBReceiving objects:  84% (262/311), 9.54 MiB | 3.79 MiBReceiving objects:  85% (265/311), 9.54 MiB | 3.79 MiBReceiving objects:  86% (268/311), 9.54 MiB | 3.79 MiBReceiving objects:  87% (271/311), 9.54 MiB | 3.79 MiBReceiving objects:  88% (274/311), 9.54 MiB | 3.79 MiBReceiving objects:  88% (275/311), 15.91 MiB | 5.27 MiReceiving objects:  89% (277/311), 15.91 MiB | 5.27 MiReceiving objects:  90% (280/311), 15.91 MiB | 5.27 MiReceiving objects:  91% (284/311), 15.91 MiB | 5.27 MiReceiving objects:  92% (287/311), 15.91 MiB | 5.27 MiReceiving objects:  93% (290/311), 24.09 MiB | 6.85 MiReceiving objects:  94% (293/311), 24.09 MiB | 6.85 MiReceiving objects:  95% (296/311), 24.09 MiB | 6.85 MiReceiving objects:  96% (299/311), 24.09 MiB | 6.85 MiReceiving objects:  97% (302/311), 24.09 MiB | 6.85 Miremote: Total 311 (delta 29), reused 262 (delta 25), pack-reused 0 (from 0)
Receiving objects:  98% (305/311), 24.09 MiB | 6.85 MiReceiving objects:  99% (308/311), 24.09 MiB | 6.85 MiReceiving objects: 100% (311/311), 24.09 MiB | 6.85 MiReceiving objects: 100% (311/311), 25.93 MiB | 7.13 MiB/s, done.
Resolving deltas: 100% (29/29), done.
~/qrf/repos $ GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/JASKSG9/FIBONACCI-SPECTRAL-DYNAMICS-
Cloning into 'FIBONACCI-SPECTRAL-DYNAMICS-'...
remote: Enumerating objects: 56, done.
remote: Counting objects: 100% (56/56), done.
remote: Compressing objects: 100% (46/46), done.
Receiving objects:  12% (7/56), 336.00 KiB | 656.00 KiReceiving objects:  12% (7/56), 1004.00 KiB | 991.00 KReceiving objects:  14% (8/56), 1004.00 KiB | 991.00 KReceiving objects:  16% (9/56), 1004.00 KiB | 991.00 KReceiving objects:  17% (10/56), 1004.00 KiB | 991.00 Receiving objects:  19% (11/56), 1004.00 KiB | 991.00 Receiving objects:  21% (12/56), 1004.00 KiB | 991.00 Receiving objects:  23% (13/56), 1004.00 KiB | 991.00 Receiving objects:  25% (14/56), 1004.00 KiB | 991.00 Receiving objects:  26% (15/56), 1004.00 KiB | 991.00 Receiving objects:  28% (16/56), 1004.00 KiB | 991.00 Receiving objects:  30% (17/56), 1004.00 KiB | 991.00 Receiving objects:  32% (18/56), 1004.00 KiB | 991.00 Receiving objects:  33% (19/56), 1004.00 KiB | 991.00 Receiving objects:  35% (20/56), 1004.00 KiB | 991.00 Receiving objects:  37% (21/56), 1004.00 KiB | 991.00 Receiving objects:  39% (22/56), 1004.00 KiB | 991.00 Receiving objects:  41% (23/56), 1004.00 KiB | 991.00 Receiving objects:  42% (24/56), 1004.00 KiB | 991.00 Receiving objects:  44% (25/56), 1004.00 KiB | 991.00 Receiving objects:  46% (26/56), 1004.00 KiB | 991.00 Receiving objects:  48% (27/56), 1004.00 KiB | 991.00 Receiving objects:  50% (28/56), 1004.00 KiB | 991.00 Receiving objects:  51% (29/56), 1004.00 KiB | 991.00 Receiving objects:  53% (30/56), 1004.00 KiB | 991.00 Receiving objects:  55% (31/56), 2.14 MiB | 1.41 MiB/sremote: Total 56 (delta 5), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (56/56), 4.78 MiB | 2.21 MiB/s, done.
Resolving deltas: 100% (5/5), done.
~/qrf/repos $ GIT_TERMINAL_PROMPT=0 git clone --depth 1 https://github.com/JASKSG9/MANDELBROT-INFINITE-DYNAMICS
Cloning into 'MANDELBROT-INFINITE-DYNAMICS'...
remote: Enumerating objects: 37, done.
remote: Counting objects: 100% (37/37), done.
remote: Compressing objects: 100% (33/33), done.
remote: Total 37 (delta 4), reused 0 (delta 0), pack-reused 0 (from 0)
Receiving objects: 100% (37/37), 1.10 MiB | 4.30 MiB/s, done.
Resolving deltas: 100% (4/4), done.
~/qrf/repos $
~/qrf/repos $ ~/bin/qrf report ./KAPREKAR-SPECTRAL-GEOMETRY https://github.com/JASKSG9/KAPREKAR-SPECTRAL-GEOMETRY > ~/qrf/ledger/kaprekar_$(date +%F).txt
~/qrf/repos $ ls -lh ~/qrf/ledger/
total 16K
-rw-------. 1 u0_a352 u0_a352 312 Sep 11 04:19 aqarion-arithmetic_2026-09-11.txt
-rw-------. 1 u0_a352 u0_a352 289 Sep 11 04:19 kaprekar_2026-09-11.txt
-rw-------. 1 u0_a352 u0_a352 273 Sep 11 04:17 quantarion_2026-09-11.txt
-rw-------. 1 u0_a352 u0_a352 298 Sep 11 03:31 requests_2026-09-11.txt
~/qrf/repos $

https://github.com/JASKSG9/AQARION-ARITHMETIC-FDS-FINITE-DYNAMICAL-SYSTEMS-/blob/main/LIBRARY/SEPTEMBER/AQ-S11-SUPPORT.TS
