
import os, time, json, pathlib, datetime as dt, requests, random
from urllib.parse import quote_plus

CFG = json.load(open('.env.json'))
LANGS = ["en","es","pt","fr","de","it","pl"]

def log(msg): print(dt.datetime.now().strftime('%H:%M:%S'), msg)

def keywords():
    base = random.choice(["best ai tool","free seo checklist","prompt engineering","open source llm guide"])
    return [f"{base} {random.randint(100,999)}"]

def translate(txt, lang):
    if lang=="en": return txt
    try:
        r = requests.post("https://libretranslate.de/translate",
                          data={"q":txt,"source":"en","target":lang})
        if r.ok:
            return r.json().get("translatedText", txt)
    except Exception:
        pass
    return txt

AMP = """<!doctype html><html amp lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,minimum-scale=1">
<meta name="google-adsense-account" content="{adsense}">
<title>{title}</title>
<script async src="https://cdn.ampproject.org/v0.js"></script>
<script async custom-element="amp-ad" src="https://cdn.ampproject.org/v0/amp-ad-0.1.js"></script>
<style amp-custom>body{{font-family:sans-serif;padding:16px}}</style></head><body>
<h1>{title}</h1><p>{descr}</p>
<amp-ad width=468 height=60 type="adsense" data-ad-client="{adsense}" data-ad-slot="1234567890"></amp-ad>
<h2>{cta}</h2>
<iframe src="{form}" width="100%" height="500" style="border:none;"></iframe>
</body></html>"""

def forge():
    p = pathlib.Path("pages"); p.mkdir(exist_ok=True)
    for kw in keywords():
        for lang in LANGS:
            fname = f"{lang}_{quote_plus(kw)}.html".replace('%','')
            path = p/fname
            if path.exists(): continue
            html = AMP.format(
                lang=lang,
                adsense=CFG["ADSENSE_ID"],
                title=translate(kw.title(), lang),
                descr=translate("Auto generated guide about "+kw, lang),
                cta=translate("Get the free toolkit", lang),
                form=CFG["FORM_URLS"][lang]
            )
            path.write_text(html)
            log(f"Created {fname}")

def deploy():
    os.system("git add pages && git commit -m auto -q && git push -q")
    log("Deployed")

if __name__=="__main__":
    while True:
        forge()
        deploy()
        time.sleep(1800)
