"""Extract CSS/JS from index.html to static files."""
import sys
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'D:/bookMaker_Deepseek/src/bookmaker/studio/templates/index.html'
css_path = r'D:/bookMaker_Deepseek/src/bookmaker/studio/static/styles.css'
js_path = r'D:/bookMaker_Deepseek/src/bookmaker/studio/static/app.js'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Extract CSS
start_css = html.find('<style>')
end_css = html.find('</style>') + len('</style>')
css_raw = html[start_css:end_css]
css_clean = css_raw.replace('<style>', '').replace('</style>', '')

# Only write if CSS file is placeholder (< 500 chars)
with open(css_path, 'r', encoding='utf-8') as f:
    existing_css = f.read()

if len(existing_css) < 500:
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css_clean)
    print(f'CSS written: {len(css_clean):,} chars')
else:
    print(f'CSS already exists: {len(existing_css):,} chars (skipped)')

# 2. Remove CSS from HTML
html_body = html[:start_css] + html[end_css:]

# 3. Add link tag after </title>
link_tag = '<link rel="stylesheet" href="/static/styles.css">'
html_body = html_body.replace('</title>', '</title>\n' + link_tag)

# 4. Extract JS
start_js = html_body.find('<script>')
end_js = html_body.find('</script>', start_js) + len('</script>')
js_raw = html_body[start_js:end_js]
js_clean = js_raw.replace('<script>', '').replace('</script>', '')

# Write JS
with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js_clean)
print(f'JS written: {len(js_clean):,} chars')

# 5. Replace inline JS with script src
html_final = html_body[:start_js] + '<script src="/static/app.js"></script>' + html_body[end_js:]

# 6. Save updated HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_final)

print(f'\nFinal sizes:')
print(f'  index.html: {len(html_final):,} chars (HTML only)')
print(f'  styles.css: {len(css_clean):,} chars')
print(f'  app.js: {len(js_clean):,} chars')
print(f'  Total savings: {len(css_clean) + len(js_clean):,} chars moved from index.html')
