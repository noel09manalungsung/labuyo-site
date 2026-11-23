"""Turn the SpiceStack legal markdown into pages on the Labuyo studio site.

Source: apollo-exporter/docs/terms-of-service.md and privacy-policy.md. Run after editing
either file or the header/style of index.html: python3 tools/build_legal.py
"""
import html
import os
import re

HOME = os.path.expanduser('~')
SITE = HOME + '/Documents/Github/labuyo-site'
DOCS = HOME + '/Documents/Github/apollo-exporter/docs'
LINKS = ' · <a href="/terms/">Terms</a> · <a href="/privacy/">Privacy</a>'


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = text.replace('support@labuyo.app',
                        '<a href="mailto:support@labuyo.app">support@labuyo.app</a>')
    text = text.replace('labuyo.app/privacy', '<a href="/privacy/">labuyo.app/privacy</a>')
    return text


def convert(md):
    out = []
    for block in md.strip().split('\n\n'):
        lines = block.split('\n')
        if block.startswith('# '):
            continue
        if block.startswith('## '):
            out.append('<h2>%s</h2>' % inline(block[3:]))
        elif block.startswith('- '):
            items = []
            for line in lines:
                if line.startswith('- '):
                    items.append(line[2:])
                else:
                    items[-1] += ' ' + line.strip()
            out.append('<ul>' + ''.join('<li>%s</li>' % inline(i) for i in items) + '</ul>')
        elif block.startswith('Noel Manalungsung, trading as Labuyo\n'):
            out.append('<p>' + '<br>'.join(inline(l) for l in lines) + '</p>')
        else:
            out.append('<p>%s</p>' % inline(' '.join(l.strip() for l in lines)))
    return '\n'.join(out)


def main():
    index_path = SITE + '/index.html'
    template = open(index_path).read()
    style = template[template.index('<style>'):template.index('</style>') + 8]
    extra = ('  .doc { background: #fff; border: 1px solid var(--line); border-radius: 16px;\n'
             '    padding: 32px; margin: 8px 0 48px; }\n'
             '  .doc h1 { margin: 0 0 4px; font-size: 30px; letter-spacing: -0.5px; }\n'
             '  .doc h2 { font-size: 19px; margin: 28px 0 8px; }\n</style>')
    style = style.replace('</style>', extra)
    header = template[template.index('<header'):template.index('</header>') + 9]
    pages = [('privacy-policy.md', 'privacy', 'SpiceStack privacy policy'),
             ('terms-of-service.md', 'terms', 'SpiceStack Terms of Service')]
    for source, folder, title in pages:
        body = convert(open(DOCS + '/' + source).read())
        page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Labuyo</title>
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{style}
</head>
<body>
{header}
<main class="wrap" style="background:var(--ground);border-radius:20px;padding-top:24px;padding-bottom:8px">
<article class="doc">
<h1>{title}</h1>
{body}
</article>
</main>
<footer class="wrap">
  Labuyo · <a href="mailto:support@labuyo.app">support@labuyo.app</a>{LINKS}
</footer>
</body>
</html>
'''
        os.makedirs(SITE + '/' + folder, exist_ok=True)
        open(SITE + '/' + folder + '/index.html', 'w').write(page)
    plain = 'Labuyo · <a href="mailto:support@labuyo.app">support@labuyo.app</a>\n'
    if plain in template:
        open(index_path, 'w').write(template.replace(plain, plain[:-1] + LINKS + '\n'))


main()
