import json, os, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "boards")
os.makedirs(ROOT, exist_ok=True)

# Breeze Dark tokens
BG = "#202326"; HEAD = "#282c30"; VIEW = "#141618"; CARD = "#1b1e21"
LINE = "#3a3f44"; TEXT = "#fcfcfc"; DIM = "#a1a9b1"; ACC = "#3daee9"; ACCD = "#1d6fa5"
WARN = "#f67400"; OK = "#3dd68c"

P = {
 "back": '<path d="M19 12H5"></path><path d="M12 19l-7-7 7-7"></path>',
 "refresh": '<path d="M21 12a9 9 0 1 1-3-6.7L21 8"></path><path d="M21 3v5h-5"></path>',
 "gear": '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
 "globe": '<circle cx="12" cy="12" r="10"></circle><path d="M2 12h20"></path><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>',
 "copy": '<rect x="9" y="9" width="13" height="13" rx="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>',
 "lock": '<rect x="3" y="11" width="18" height="11" rx="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path>',
 "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><path d="M14 2v6h6"></path>',
 "search": '<circle cx="11" cy="11" r="7"></circle><path d="M21 21l-4.35-4.35"></path>',
 "pencil": '<path d="M17 3a2.83 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"></path>',
 "check": '<path d="M20 6L9 17l-5-5"></path>',
 "x": '<path d="M18 6L6 18"></path><path d="M6 6l12 12"></path>',
 "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>',
 "code": '<path d="M16 18l6-6-6-6"></path><path d="M8 6l-6 6 6 6"></path>',
 "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><path d="M12 9v4"></path><path d="M12 17h.01"></path>',
 "key": '<circle cx="7.5" cy="15.5" r="5.5"></circle><path d="M21 2l-9.6 9.6"></path><path d="M15.5 7.5l3 3L22 7l-3-3"></path>',
 "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle>',
 "msg": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>',
}

def ic(name, size=16, color="currentColor", extra=""):
    return ('<svg viewBox="0 0 24 24" aria-hidden="true" style="width: %dpx; height: %dpx; fill: none; stroke: %s; '
            'stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex-shrink: 0; %s">%s</svg>') % (size, size, color, extra, P[name])

def gi(color=TEXT, size=22):
    # The applet's own icon (package/contents/icons/hicolor/scalable), filled with the text colour.
    return ('<svg viewBox="0 0 22 22" aria-hidden="true" style="width: %dpx; height: %dpx; flex-shrink: 0">'
            '<path fill-rule="evenodd" style="fill: %s" d="M 4 2 H 13 L 18 7 V 20 H 4 Z M 7 7 H 15 V 9 H 7 Z M 7 11 H 14 V 13 H 7 Z M 7 15 H 12 V 17 H 7 Z"></path></svg>' % (size, size, color))

def ib(name, label, active=False):
    st = "background: rgba(61,174,233,0.18); border-color: rgba(61,174,233,0.6);" if active else ""
    return '<button class="ib" type="button" aria-label="%s" title="%s" style="%s">%s</button>' % (label, label, st, ic(name))

HELMET = """<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;600;700&amp;family=Noto+Sans+Mono:wght@400;600&amp;display=swap" rel="stylesheet">
<style>
body{margin:0;background:#101214}
a{color:#3daee9}a:hover{color:#7cc8f0}
.ib{width:32px;height:32px;display:inline-flex;align-items:center;justify-content:center;border:1px solid transparent;border-radius:4px;background:transparent;color:#fcfcfc;padding:0;cursor:pointer}
.ib:hover{background:rgba(61,174,233,0.18);border-color:rgba(61,174,233,0.6)}
.btn{height:32px;display:inline-flex;align-items:center;gap:6px;padding:0 12px;border-radius:4px;border:1px solid #4d5359;background:#31363b;color:#fcfcfc;font:inherit;font-size:13px;cursor:pointer}
.btn:hover{border-color:#3daee9}
.btn.primary{background:#1d6fa5;border-color:#3daee9}
.field{height:32px;box-sizing:border-box;border-radius:4px;border:1px solid #4d5359;background:#141618;color:#fcfcfc;font:inherit;font-size:13px;padding:0 10px}
.mono{font-family:'Noto Sans Mono',Hack,monospace}
</style>
</helmet>"""

def page(title, w, h, body):
    return """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>%s</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
%s
%s
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{"$preview":{"width":%d,"height":%d}}'>
class Component extends DCLogic {
renderVals() {
return {};
}
}
</script>
</body>
</html>
""" % (title, HELMET, body, w, h)

def popup(w, h, header, content, footer=""):
    return ('<div style="width: %dpx; height: %dpx; box-sizing: border-box; display: flex; flex-direction: column; '
            'background: %s; color: %s; font-family: \'Noto Sans\', sans-serif; font-size: 13px; border: 1px solid %s; '
            'border-radius: 8px; overflow: hidden">' % (w, h, BG, TEXT, LINE)
            + '<div style="display: flex; flex-direction: column; gap: 8px; padding: 8px 8px 8px 12px; background: %s; border-bottom: 1px solid %s">%s</div>' % (HEAD, LINE, header)
            + '<div style="flex-grow: 1; min-height: 0; display: flex; flex-direction: column; overflow: hidden">%s</div>' % content
            + (('<div style="display: flex; align-items: center; gap: 8px; min-height: 32px; padding: 0 12px; background: %s; border-top: 1px solid %s; font-size: 12px; color: %s">%s</div>' % (HEAD, LINE, DIM, footer)) if footer else "")
            + '</div>')

def hrow(*parts):
    return '<div style="display: flex; align-items: center; gap: 4px">%s</div>' % "".join(parts)

def htitle(t):
    return '<h1 style="margin: 0; flex-grow: 1; font-size: 15px; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">%s</h1>' % t

def seg(items):
    # items: (icon or None, label, active)
    out = '<div role="group" style="display: flex; border: 1px solid #4d5359; border-radius: 4px; overflow: hidden; flex-shrink: 0">'
    for i, (icn, label, act) in enumerate(items):
        st = "background: %s; color: #ffffff;" % ACCD if act else "background: #31363b; color: %s;" % TEXT
        sep = "" if i == 0 else "border-left: 1px solid #4d5359;"
        out += ('<button type="button" aria-pressed="%s" style="height: 28px; display: flex; align-items: center; gap: 6px; padding: 0 10px; border: 0; %s %s font: inherit; font-size: 12px; cursor: pointer">%s%s</button>'
                % ("true" if act else "false", st, sep, ic(icn, 14) if icn else "", label))
    return out + '</div>'

def tabs(items):
    out = '<div role="tablist" style="display: flex; gap: 2px; flex-grow: 1; min-width: 0">'
    for label, act, dirty in items:
        st = ("color: %s; border-bottom: 2px solid %s;" % (TEXT, ACC)) if act else ("color: %s; border-bottom: 2px solid transparent;" % DIM)
        dot = ('<span aria-label="unsaved" style="width: 7px; height: 7px; border-radius: 4px; background: %s"></span>' % WARN) if dirty else ""
        out += ('<button type="button" role="tab" aria-selected="%s" style="height: 30px; display: flex; align-items: center; gap: 6px; padding: 0 10px; background: transparent; border: 0; %s font: inherit; font-size: 12px; cursor: pointer">%s%s%s</button>'
                % ("true" if act else "false", st, ic("file", 13), label, dot))
    return out + '</div>'

GISTS = [
    ("Arch post-install notes", "Markdown · 2 files · 3 comments", "2h ago", True),
    ("kwin script: tile to thirds", "JavaScript · 1 file", "Yesterday", True),
    ("Plasma widget QML snippets", "QML · 4 files", "3 days ago", False),
    ("Home server docker-compose", "YAML · 2 files", "Sep 21", False),
    ("init.lua", "Lua · 1 file · 1 comment", "Sep 14", True),
    ("journalctl one-liners", "Markdown · 1 file", "Sep 9", True),
    ("pacman hooks", "Shell · 3 files", "Aug 30", True),
]

def row(t, sub, when, public, hover=False, dim=False):
    icon = ic("file", 20, DIM) if public else ic("lock", 20, DIM)
    right = (ib("globe", "View on web") + ib("copy", "Copy URL")) if hover else ('<span style="font-size: 12px; color: %s; white-space: nowrap">%s</span>' % (DIM, when))
    bg = "background: rgba(61,174,233,0.14); border: 1px solid rgba(61,174,233,0.55);" if hover else "border: 1px solid transparent;"
    op = "opacity: 0.45;" if dim else ""
    badge = "" if public else '<span style="font-size: 11px; color: %s; border: 1px solid #4d5359; border-radius: 3px; padding: 0 5px; margin-left: 6px">Secret</span>' % DIM
    return ('<div style="display: flex; align-items: center; gap: 10px; min-height: 50px; box-sizing: border-box; padding: 4px 8px; border-radius: 4px; %s %s">' % (bg, op)
            + icon
            + '<div style="flex-grow: 1; min-width: 0; display: flex; flex-direction: column; gap: 1px">'
            + '<div style="display: flex; align-items: center; font-size: 13px; white-space: nowrap; overflow: hidden">%s%s</div>' % (t, badge)
            + '<div style="font-size: 12px; color: %s; white-space: nowrap; overflow: hidden; text-overflow: ellipsis">%s</div></div>' % (DIM, sub)
            + '<div style="display: flex; align-items: center; gap: 2px">%s</div></div>' % right)

def listbody(hover_idx=None, dim=False, count=7):
    return ('<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 1px; padding: 6px">'
            + "".join(row(*g, hover=(i == hover_idx), dim=dim) for i, g in enumerate(GISTS[:count])) + '</div>')

def search(value=""):
    ph = "" if value else ' placeholder="Filter by description or filename"'
    val = (' value="%s"' % value) if value else ""
    return ('<label style="flex-grow: 1; position: relative; display: flex; align-items: center">'
            '<span style="position: absolute; left: 9px; display: flex; color: %s">%s</span>' % (DIM, ic("search", 14))
            + '<input class="field" type="search" aria-label="Filter gists"%s%s style="width: 100%%; padding-left: 30px"></label>' % (ph, val))

boards = {}

# 1. List
W, H = 560, 520
hdr = hrow(htitle("My Gists"), ib("refresh", "Refresh"), ib("gear", "Configure…")) + \
      '<div style="display: flex; gap: 8px; align-items: center; padding-right: 4px">' + search() + seg([(None, "All", True), (None, "Public", False), (None, "Secret", False)]) + '</div>'
boards["Main.dc.html"] = ("Gist list", W, H, page("Gist list", W, H, popup(W, H, hdr, listbody(hover_idx=1), "<span>Updated 14:32</span><span style=\"flex-grow: 1\"></span><span>42 gists</span>")))

# 2. Viewer, rendered
def viewer_header(active_rendered, title="Arch post-install notes"):
    return hrow(ib("back", "Back to list"), htitle(title), ib("pencil", "Edit"), ib("copy", "Copy contents"), ib("globe", "View on web")) + \
        '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: -8px">' + \
        tabs([("README.md", True, False), ("setup.sh", False, False)]) + \
        '<div style="padding-bottom: 6px">' + seg([("eye", "Rendered", active_rendered), ("code", "Source", not active_rendered)]) + '</div></div>'

MONO = "font-family: 'Noto Sans Mono', Hack, monospace;"
def chk(on):
    inner = ic("check", 12, "#ffffff") if on else ""
    st = ("background: %s; border: 1px solid %s;" % (ACCD, ACC)) if on else "background: transparent; border: 1px solid #6b7278;"
    return '<span style="width: 14px; height: 14px; border-radius: 3px; display: inline-flex; align-items: center; justify-content: center; box-sizing: border-box; %s">%s</span>' % (st, inner)
def ccode(t):
    return '<code style="%s font-size: 12px; background: %s; border: 1px solid %s; border-radius: 3px; padding: 0 4px">%s</code>' % (MONO, VIEW, LINE, t)

md = ('<div style="flex-grow: 1; overflow: hidden; padding: 16px 22px; display: flex; flex-direction: column; gap: 10px; line-height: 1.5">'
      '<h2 style="margin: 0; font-size: 21px; font-weight: 700; padding-bottom: 6px; border-bottom: 1px solid %s">Arch post-install</h2>' % LINE
      + '<p style="margin: 0">Everything I run on a fresh install before touching dotfiles. Tested on Plasma 6.7.</p>'
      + '<h3 style="margin: 4px 0 0 0; font-size: 16px; font-weight: 600">Packages</h3>'
      + '<pre style="margin: 0; padding: 10px 12px; background: %s; border: 1px solid %s; border-radius: 4px; %s font-size: 12px; line-height: 1.6; color: #cfcfc2; white-space: pre"><span style="color: #fdbc4b">sudo</span> pacman -S --needed base-devel git plasma-sdk\n<span style="color: #fdbc4b">paru</span> -S visual-studio-code-bin</pre>' % (VIEW, LINE, MONO)
      + '<h3 style="margin: 4px 0 0 0; font-size: 16px; font-weight: 600">Checklist</h3>'
      + '<div style="display: flex; flex-direction: column; gap: 4px">'
      + '<div style="display: flex; align-items: center; gap: 8px">%sEnable %s</div>' % (chk(True), ccode("fstrim.timer"))
      + '<div style="display: flex; align-items: center; gap: 8px">%sSet up zram</div>' % chk(True)
      + '<div style="display: flex; align-items: center; gap: 8px">%sRestore KWallet</div></div>' % chk(False)
      + '<blockquote style="margin: 4px 0 0 0; padding: 2px 12px; border-left: 3px solid #4d5359; color: %s">Run %s after the first reboot, not before. <a href="#">Why?</a></blockquote>' % (DIM, ccode("setup.sh"))
      + '</div>')
foot_v = '<span>Markdown · 1.8 KB</span><span style="flex-grow: 1"></span>%s<span>3 comments · updated 2h ago</span>' % ic("msg", 13)
W, H = 560, 560
boards["Viewer-Rendered.dc.html"] = ("Viewer · rendered Markdown", W, H, page("Viewer rendered", W, H, popup(W, H, viewer_header(True), md, foot_v)))

# 3. Viewer, source
SRC = [
 ('<span style="color: #3daee9; font-weight: 600"># Arch post-install</span>'),
 (''),
 ('Everything I run on a fresh install before touching'),
 ('dotfiles. Tested on Plasma 6.7.'),
 (''),
 ('<span style="color: #3daee9; font-weight: 600">## Packages</span>'),
 (''),
 ('<span style="color: #7a7c7d">```sh</span>'),
 ('<span style="color: #fdbc4b">sudo</span> pacman -S --needed base-devel git plasma-sdk'),
 ('<span style="color: #fdbc4b">paru</span> -S visual-studio-code-bin'),
 ('<span style="color: #7a7c7d">```</span>'),
 (''),
 ('<span style="color: #3daee9; font-weight: 600">## Checklist</span>'),
 (''),
 ('<span style="color: #f67400">- [x]</span> Enable <span style="color: #27aeae">`fstrim.timer`</span>'),
 ('<span style="color: #f67400">- [x]</span> Set up zram'),
 ('<span style="color: #f67400">- [ ]</span> Restore KWallet'),
 (''),
 ('<span style="color: #a1a9b1; font-style: italic">&gt; Run <span style="color: #27aeae">`setup.sh`</span> after the first reboot, not before.</span>'),
]
def codeview(lines, hl=None, caret=None):
    nums = "\n".join(str(i + 1) for i in range(len(lines)))
    body = ""
    for i, l in enumerate(lines):
        st = "background: rgba(61,174,233,0.10);" if hl == i else ""
        c = '<span style="display: inline-block; width: 2px; height: 15px; background: %s; vertical-align: -3px"></span>' % TEXT if caret == i else ""
        body += '<div style="%s min-height: 19px">%s%s</div>' % (st, l, c)
    return ('<div style="flex-grow: 1; overflow: hidden; display: flex; background: %s; %s font-size: 12px; line-height: 19px; color: #cfcfc2">' % (VIEW, MONO)
            + '<pre aria-hidden="true" style="margin: 0; padding: 10px 10px 10px 12px; text-align: right; color: #5c6166; border-right: 1px solid %s; user-select: none">%s</pre>' % (LINE, nums)
            + '<div style="flex-grow: 1; padding: 10px 12px; white-space: pre">%s</div></div>' % body)
foot_s = '<span>Markdown · 19 lines · UTF-8</span><span style="flex-grow: 1"></span><span>Select text to copy, or use the copy button above</span>'
boards["Viewer-Source.dc.html"] = ("Viewer · source", W, H, page("Viewer source", W, H, popup(W, H, viewer_header(False), codeview(SRC), foot_s)))

# 4. Edit
EDIT = list(SRC)
EDIT[16] = '<span style="color: #f67400">- [x]</span> Restore KWallet'
hdr_e = hrow(ib("x", "Discard changes"), htitle("Editing “Arch post-install notes”"),
             '<button class="btn" type="button">Cancel</button>', '<button class="btn primary" type="button">%sSave</button>' % ic("check", 14)) + \
    '<label style="display: flex; align-items: center; gap: 8px; padding-right: 4px"><span style="color: %s; font-size: 12px; width: 76px">Description</span><input class="field" type="text" value="Arch post-install notes" style="flex-grow: 1"></label>' % DIM + \
    '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: -8px">' + tabs([("README.md", True, True), ("setup.sh", False, False)]) + \
    '<div style="padding-bottom: 6px">' + seg([("pencil", "Write", True), ("eye", "Preview", False)]) + '</div></div>'
foot_e = ('<span style="width: 8px; height: 8px; border-radius: 4px; background: %s"></span><span style="color: %s">Unsaved changes</span>' % (WARN, TEXT)
          + '<span style="flex-grow: 1"></span><span>Ctrl+S save · Esc cancel · Ln 17, Col 6</span>')
boards["Edit.dc.html"] = ("Inline editing", W, H, page("Edit gist", W, H, popup(W, H, hdr_e, codeview(EDIT, hl=16, caret=16), foot_e)))

# 5. Setup / first run
W, H = 560, 520
hdr_s = hrow(htitle("GitHub Gists"), ib("gear", "Configure…"))
setup = ('<div style="flex-grow: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 14px; padding: 32px 48px; text-align: center">'
         + '<div style="width: 64px; height: 64px; border-radius: 32px; background: %s; border: 1px solid %s; display: flex; align-items: center; justify-content: center">%s</div>' % (CARD, LINE, gi(ACC, 34))
         + '<h2 style="margin: 0; font-size: 18px; font-weight: 600">Connect to GitHub</h2>'
         + '<p style="margin: 0; color: %s; line-height: 1.5; max-width: 380px">Sign in with a personal access token to list, read and edit your own gists, including secret ones. Or browse anyone’s public gists by username.</p>' % DIM
         + '<div style="display: flex; flex-direction: column; gap: 8px; width: 280px; margin-top: 6px">'
         + '<button class="btn primary" type="button" style="justify-content: center">%sUse an access token…</button>' % ic("key", 14)
         + '<button class="btn" type="button" style="justify-content: center">%sBrowse a username…</button></div>' % ic("user", 14)
         + '<a href="https://github.com/settings/personal-access-tokens/new" style="font-size: 12px; margin-top: 4px">Create a token with Gists read and write access</a>'
         + '</div>')
boards["State-Setup.dc.html"] = ("First run · not configured", W, H, page("Not configured", W, H, popup(W, H, hdr_s, setup)))

# 6. Error with stale list
hdr_err = hrow(htitle("My Gists"), ib("refresh", "Refresh"), ib("gear", "Configure…")) + \
    '<div style="display: flex; gap: 8px; align-items: center; padding-right: 4px">' + search() + seg([(None, "All", True), (None, "Public", False), (None, "Secret", False)]) + '</div>'
banner = ('<div role="alert" style="display: flex; align-items: center; gap: 10px; margin: 8px 8px 0 8px; padding: 8px 8px 8px 12px; border-radius: 4px; background: rgba(246,116,0,0.14); border: 1px solid rgba(246,116,0,0.6)">'
          + ic("alert", 18, WARN)
          + '<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 1px"><span style="font-weight: 600">GitHub rate limit reached</span>'
          + '<span style="font-size: 12px; color: %s">Resets at 15:10. Showing the list from 14:32. Add a token to raise the limit.</span></div>' % DIM
          + '<button class="btn" type="button">Retry</button></div>')
boards["State-Error.dc.html"] = ("Error · stale list kept", W, H, page("Rate limited", W, H, popup(W, H, hdr_err, banner + listbody(dim=True, count=6), "<span>Updated 14:32 · not current</span>")))

# 7. Settings
W, H = 680, 560
def frow(label, ctrl, top=False):
    return ('<div style="display: flex; gap: 12px; align-items: %s">' % ("flex-start" if top else "center")
            + '<span style="width: 170px; text-align: right; flex-shrink: 0; %s">%s</span>' % ("padding-top: 6px;" if top else "", label)
            + '<div style="flex-grow: 1; display: flex; flex-direction: column; gap: 6px">%s</div></div>' % ctrl)
def radio(label, on):
    dot = '<span style="width: 8px; height: 8px; border-radius: 4px; background: #ffffff"></span>' if on else ""
    st = "background: %s; border: 1px solid %s;" % (ACCD, ACC) if on else "border: 1px solid #6b7278;"
    return '<label style="display: flex; align-items: center; gap: 8px"><span style="width: 16px; height: 16px; box-sizing: border-box; border-radius: 8px; display: flex; align-items: center; justify-content: center; %s">%s</span>%s</label>' % (st, dot, label)
def cbox(label, on):
    return '<label style="display: flex; align-items: center; gap: 8px">%s%s</label>' % (chk(on).replace("14px", "16px"), label)
def help_(t):
    return '<span style="font-size: 12px; color: %s; line-height: 1.45; max-width: 380px">%s</span>' % (DIM, t)
def combo(v, w=180):
    return '<button class="btn" type="button" style="width: %dpx; justify-content: space-between">%s<svg viewBox="0 0 24 24" aria-hidden="true" style="width: 12px; height: 12px; fill: none; stroke: currentColor; stroke-width: 2"><path d="M6 9l6 6 6-6"></path></svg></button>' % (w, v)
sep = '<div style="height: 1px; background: %s; margin: 4px 0"></div>' % LINE
settings = ('<div style="width: %dpx; height: %dpx; box-sizing: border-box; display: flex; background: %s; color: %s; font-family: \'Noto Sans\', sans-serif; font-size: 13px; border: 1px solid %s; border-radius: 8px; overflow: hidden">' % (W, H, BG, TEXT, LINE)
    + '<nav style="width: 120px; flex-shrink: 0; background: %s; border-right: 1px solid %s; padding: 10px 6px; display: flex; flex-direction: column; gap: 4px">' % (HEAD, LINE)
    + '<a href="#" style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 4px; border-radius: 4px; background: rgba(61,174,233,0.18); color: %s; text-decoration: none; font-size: 12px">%sGeneral</a>' % (TEXT, ic("gear", 24))
    + '<a href="#" style="display: flex; flex-direction: column; align-items: center; gap: 4px; padding: 10px 4px; border-radius: 4px; color: %s; text-decoration: none; font-size: 12px">%sKeyboard Shortcuts</a></nav>' % (TEXT, ic("key", 24))
    + '<div style="flex-grow: 1; display: flex; flex-direction: column">'
    + '<div style="flex-grow: 1; padding: 20px 24px 12px 12px; display: flex; flex-direction: column; gap: 12px">'
    + frow("Show:", radio("My gists (public and secret)", True) + radio("Public gists of a user:", False)
           + '<input class="field" type="text" placeholder="octocat" aria-label="Username" disabled style="width: 220px; margin-left: 24px; opacity: 0.5">', top=True)
    + frow("Access token:", '<div style="display: flex; gap: 6px"><input class="field" type="password" value="github_pat_xxxxxxxxxxxx" aria-label="Access token" style="width: 260px"><button class="btn" type="button">Test</button></div>'
           + '<span style="display: flex; align-items: center; gap: 6px; font-size: 12px; color: %s">%sSigned in as nmartin867 · Gists: read and write</span>' % (OK, ic("check", 13, OK))
           + help_("Editing needs a fine-grained token with Gists read and write access. It is stored in the widget’s plain-text config file."), top=True)
    + sep
    + frow("Open Markdown as:", combo("Rendered"))
    + frow("Gists to show:", '<input class="field" type="number" value="30" aria-label="Gists to show" style="width: 90px">')
    + frow("Refresh every:", combo("15 minutes", 150))
    + frow("Tooltips:", cbox("Show full description on hover", True))
    + '</div>'
    + '<div style="display: flex; gap: 8px; padding: 10px 12px; border-top: 1px solid %s; background: %s"><button class="btn" type="button">Defaults</button><span style="flex-grow: 1"></span>' % (LINE, HEAD)
    + '<button class="btn primary" type="button">OK</button><button class="btn" type="button">Apply</button><button class="btn" type="button">Cancel</button></div>'
    + '</div></div>')
boards["Settings.dc.html"] = ("Settings page", W, H, page("Settings", W, H, settings))

# 8. Panel icon states
W, H = 560, 300
def pstate(caption, sub, badge="", hover=False):
    b = ""
    if badge == "dot":
        b = '<span style="position: absolute; right: 3px; bottom: 3px; width: 9px; height: 9px; border-radius: 5px; background: %s; border: 2px solid #1b1e21"></span>' % WARN
    elif badge:
        b = '<span style="position: absolute; right: 0; bottom: 1px; min-width: 15px; height: 15px; padding: 0 3px; box-sizing: border-box; border-radius: 8px; background: %s; color: #ffffff; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center">%s</span>' % (ACCD, badge)
    hv = "background: rgba(255,255,255,0.10);" if hover else ""
    return ('<div style="flex-grow: 1; flex-basis: 0; display: flex; flex-direction: column; align-items: center; gap: 10px">'
            + '<div style="width: 100%%; height: 44px; background: #1b1e21; border: 1px solid %s; border-radius: 6px; display: flex; align-items: center; justify-content: center">' % LINE
            + '<div style="position: relative; width: 34px; height: 34px; border-radius: 4px; display: flex; align-items: center; justify-content: center; %s">%s%s</div></div>' % (hv, gi(), b)
            + '<span style="font-weight: 600">%s</span><span style="font-size: 12px; color: %s; text-align: center; line-height: 1.4">%s</span></div>' % (caption, DIM, sub))
panel = ('<div style="width: %dpx; height: %dpx; box-sizing: border-box; padding: 24px; display: flex; flex-direction: column; gap: 22px; background: %s; color: %s; font-family: \'Noto Sans\', sans-serif; font-size: 13px; border: 1px solid %s; border-radius: 8px">' % (W, H, BG, TEXT, LINE)
    + '<div style="display: flex; gap: 16px">'
    + pstate("Idle", "No badge. The total count is noise in a panel.")
    + pstate("Updated", "Badge counts gists changed since the popup was last opened.", "2")
    + pstate("Error", "Orange dot; tooltip carries the message.", "dot")
    + '</div>'
    + '<div style="align-self: center; display: flex; flex-direction: column; gap: 2px; padding: 8px 12px; background: %s; border: 1px solid %s; border-radius: 6px; box-shadow: 0 4px 14px rgba(0,0,0,0.4)">' % (HEAD, LINE)
    + '<span style="font-weight: 600">GitHub Gists</span><span style="font-size: 12px; color: %s">42 gists · 2 updated · checked 14:32</span></div>' % DIM
    + '</div>')
boards["Panel.dc.html"] = ("Panel icon and tooltip", W, H, page("Panel icon", W, H, panel))

# layout
row1 = ["Main.dc.html", "Viewer-Rendered.dc.html", "Viewer-Source.dc.html", "Edit.dc.html"]
row2 = ["State-Setup.dc.html", "State-Error.dc.html", "Settings.dc.html", "Panel.dc.html"]
layout = {}
x = 0
for n in row1:
    _, w, h, _ = boards[n]; layout[n] = (x, 0, w, h); x += w + 80
row1w = x - 80
y2 = 560 + 120 + 260
x = 0
for n in row2:
    _, w, h, _ = boards[n]; layout[n] = (x, y2, w, h); x += w + 80
row2w = x - 80

idx = {
    "v": 3,
    "createdOnFiles": {"v": 1, "at": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")},
    "title": "Gist Widget Mockups",
    "launch": {"view": "canvas"},
    "pages": [],
    "boards": {n: {"x": layout[n][0], "y": layout[n][1], "w": layout[n][2], "h": layout[n][3], "title": boards[n][0]} for n in row1 + row2},
    "order": row1 + row2,
    "notes": {
        "flow": {"x": 0, "y": -260, "text": "Browse, read, edit", "kind": "title1", "maxW": row1w},
        "states": {"x": 0, "y": y2 - 260, "text": "States, settings and panel", "kind": "title1", "maxW": row2w},
    },
    "designSystems": [],
}
with open(os.path.join(ROOT, "canvas.json"), "w") as f:
    json.dump(idx, f, indent=1)
for n, (_, _, _, src) in boards.items():
    with open(os.path.join(ROOT, n), "w") as f:
        f.write(src)
print("ok", list(boards))
