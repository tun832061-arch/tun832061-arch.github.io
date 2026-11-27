# make_calendar.py — rebuilds posts.json, UPLOAD_CALENDAR.md and upload-calendar.ics from UPLOAD.md.
#   python3 tools/make_calendar.py [path/to/upload-desk.html]   (run from channel/)
# Schedule: Ep1 Sat Nov 28 2026, then Tue/Fri in episode order (skipping Dec 18, 22, 25; Ep7 on Sat Dec 26).
# Each Short goes 2 days after its episode (1 day for Ep1). Shorts' tags = episode's top 4 + "shorts".
import re, json, sys, datetime as dt
D = dt.date
up = open('UPLOAD.md').read()
eps = {int(m.group(1)): dict(title=m.group(2).strip(), desc=m.group(3).strip(), tags=m.group(4).strip(), pin=m.group(5).strip())
       for m in re.finditer(r'## Episode (\d+):[^\n]*\n\n\*\*Title:\*\* (.*?)\n\n\*\*Description:\*\*\n```\n(.*?)```\n\*\*Tags:\*\* (.*?)\n\n\*\*Pinned comment:\*\* `(.*?)`', up, re.S)}
shorts = {int(m.group(1)): dict(title=m.group(2).strip(), desc=m.group(3).strip())
          for m in re.finditer(r'\*\*`ep(\d\d)-short/build/video\.mp4`\*\*[^\n]*\n- \*\*Title:\*\* (.*?)\n- \*\*Description:\*\* `(.*?)`', up)}
m = re.search(r'## Short: `ep01-short.*?\*\*Title:\*\* (.*?)\n\*\*Description:\*\* `(.*?)`', up, re.S)
shorts[1] = dict(title=m.group(1).strip(), desc=m.group(2).strip())
N = max(eps); assert sorted(eps) == list(range(1, N + 1)), 'missing episode in UPLOAD.md'
sched = {1: D(2026, 11, 28)}; d = D(2026, 12, 1); slots = []
while len(slots) < N + 5:
    if d.weekday() in (1, 4) and d not in {D(2026, 12, 18), D(2026, 12, 22), D(2026, 12, 25)}: slots.append(d)
    d += dt.timedelta(1)
it = iter(slots)
for n in range(2, N + 1): sched[n] = D(2026, 12, 26) if n == 7 else next(it)
posts = []
for n, d in sched.items():
    e = eps[n]; tags = [t.strip() for t in e['tags'].split(',')]
    posts.append(dict(id=f"ep{n:02d}", date=d.isoformat(), kind="Episode", n=n, file=f"channel/ep{n:02d}/build/video.mp4", thumb=f"channel/ep{n:02d}/build/thumbnail.png",
                      captions=f"channel/ep{n:02d}/build/video.srt", title=e['title'], desc=e['desc'], tags=', '.join(tags), pin=e['pin']))
    if n in shorts:
        s = shorts[n]
        posts.append(dict(id=f"short{n:02d}", date=(d + dt.timedelta(1 if n == 1 else 2)).isoformat(), kind="Short", n=n, file=f"channel/ep{n:02d}-short/build/video.mp4",
                          title=s['title'], desc=s['desc'], tags=', '.join(tags[:4] + ['shorts']), related=f"Episode {n}: {e['title']}"))
posts.sort(key=lambda p: (p['date'], p['kind'] != 'Episode'))
for p in posts: assert len(p['title']) <= 100 and len(p['tags']) <= 500, p['id']
json.dump(posts, open('posts.json', 'w'), indent=1, ensure_ascii=False)
F = dt.date.fromisoformat
md = ["# Upload calendar (with titles, descriptions and tags)", "",
      "Every post in order, with everything to paste into YouTube Studio. Upload, choose **Schedule**, and use the date shown. Keep one posting time (4 PM your local time is a reasonable default).", "",
      "Before posting: replace `[PLANNER LINK]` with your store link (or delete that sentence until the planner is listed), upload the thumbnail and the `.srt` captions file, and for Shorts set **Related video** to the episode named.", "",
      "| Date | Post | Title |", "|---|---|---|"]
for p in posts:
    d = F(p['date']); md.append(f"| {d:%a %b} {d.day} | {('**Episode ' + str(p['n']) + '**') if p['kind'] == 'Episode' else 'Short ' + str(p['n'])} | [{p['title']}](#{p['id']}) |")
md.append("")
for p in posts:
    d = F(p['date'])
    md += ["---", "", f'<a id="{p["id"]}"></a>', f"## {d:%a %b} {d.day}, {d.year} · {p['kind']} {p['n']}", "", f"**File:** `{p['file']}`"]
    md.append(f"**Thumbnail:** `{p['thumb']}` · **Captions:** `{p['captions']}`" if p['kind'] == 'Episode' else f"**Related video:** {p['related']}")
    md += ["", "**Title**", "```", p['title'], "```", "**Description**", "```", p['desc'], "```", "**Tags**", "```", p['tags'], "```"]
    if p['kind'] == 'Episode': md += ["**Pinned comment**", "```", p['pin'], "```"]
    md.append("")
open('UPLOAD_CALENDAR.md', 'w').write('\n'.join(md))
esc = lambda s: s.replace('\\', '\\\\').replace(',', r'\,').replace(';', r'\;')
ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Paycheck Math//Upload Calendar//EN", "CALSCALE:GREGORIAN"]
for p in posts:
    d = F(p['date'])
    ics += ["BEGIN:VEVENT", f"UID:pm-{p['id']}@paycheckmath", "DTSTAMP:20261127T000000Z", f"DTSTART;VALUE=DATE:{d:%Y%m%d}", f"DTEND;VALUE=DATE:{d + dt.timedelta(1):%Y%m%d}",
            "SUMMARY:" + esc(f"Post {p['kind']} {p['n']}: {p['title']}"), "DESCRIPTION:" + esc(f"File: {p['file']}. Full text in UPLOAD_CALENDAR.md."), "END:VEVENT"]
ics.append("END:VCALENDAR"); open('upload-calendar.ics', 'w').write('\r\n'.join(ics) + '\r\n')
if len(sys.argv) > 1:
    h = open(sys.argv[1]).read()
    h = re.sub(r'const POSTS = .*?;\n', lambda _: 'const POSTS = ' + json.dumps(posts, ensure_ascii=False).replace('</', '<\\/') + ';\n', h, count=1, flags=re.S)
    h = re.sub(r'All \d+ posts in order, from Nov 28 to [A-Za-z]+ \d+', f"All {len(posts)} posts in order, from Nov 28 to {F(posts[-1]['date']):%b} {F(posts[-1]['date']).day}", h)
    h = re.sub(r'of \d+ posted', f'of {len(posts)} posted', h)
    open(sys.argv[1], 'w').write(h)
print(len(posts), 'posts,', N, 'episodes, last', posts[-1]['date'])
