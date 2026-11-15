#!/usr/bin/env python3
"""Génère les pages HTML statiques du site RCMEC-CI. Usage : python3 build.py

RÈGLE : tout texte vient des informations fournies par RCMEC-CI (fiche, affiches,
site officiel rcmec-ci.com). Aucune information inventée.
"""
import html, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
FB = "https://web.facebook.com/p/R%C3%A9seau-des-Caisses-Mutuelles-dEpargne-et-de-Cr%C3%A9dit-de-C%C3%B4te-dIvoire-61587044378852/"
LI = "https://www.linkedin.com/company/rcmec-ci/"
IG = "https://www.instagram.com/rcmecci/"
TEL, TEL_HREF, MAIL = "+225 27 22 50 12 85", "+2252722501285", "contact@rcmec.ci"
OSM = "https://www.openstreetmap.org/search?query=Carrefour%20Duncan%20Cocody%20Abidjan"
SLOGAN = "Avec vous au quotidien pour garantir votre épargne et assurer votre avenir"
FULL = "Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire"

NAV = [("index.html", "Accueil"), ("a-propos.html", "À propos"), ("services.html", "Nos services"),
       ("caisses.html", "Nos caisses"), ("simulateur.html", "Simulateur"), ("contact.html", "Contact")]

# Services : libellés et descriptions issus de la fiche, des affiches et du site officiel.
SERVICES = [
 dict(id="epargne", ico="piggy-bank", t="Épargne", img="femme-sourire.jpg",
      d="Comptes d'épargne sécurisés pour les particuliers, les groupements et les professionnels.",
      q="Avec nous, votre épargne est en sécurité."),
 dict(id="parts-sociales", ico="users", t="Parts sociales rémunérées", img="reunion-equipe.jpg",
      d="Participation au capital mutualiste permettant de devenir membre sociétaire et de percevoir des dividendes."),
 dict(id="depot-a-terme", ico="lock", t="Dépôts à terme (DAT)", img="equipe-bureau.jpg",
      d="Placement d'une somme bloquée sur une durée définie avec un taux d'intérêt avantageux."),
 dict(id="credit", ico="hand-coins", t="Crédit", img="vendeur-banane.jpg",
      d="Financement de projets, fonds de roulement, crédits agricoles et soutien aux activités génératrices de revenus. Des crédits adaptés, à moindre coût."),
 dict(id="credit-agricole", ico="sprout", t="Crédit agricole", img="agricultrice.jpg",
      d="Votre projet agricole mérite un coup de pouce !", q="La référence en milieu rural et défavorisé."),
 dict(id="pret-scolaire", ico="graduation-cap", t="Prêt scolaire", img="ecoliere.jpg",
      d="Le prêt scolaire : la clé d'une rentrée réussie."),
 dict(id="securite-etude", ico="shield-check", t="RCMEC Sécurité Étude",
      d="RCMEC Sécurité Étude : l'assurance qui protège chaque parcours scolaire."),
 dict(id="transfert", ico="send", t="Transfert rapide d'argent", img="client-telephone.jpg",
      d="Envoi et réception de fonds sécurisés sur l'ensemble du territoire.", q="Transférez votre argent en toute sécurité."),
 dict(id="micro-assurance", ico="umbrella", t="Micro-assurance",
      d="Des solutions de micro-assurance."),
]
HOME_SERVICES = ["epargne", "parts-sociales", "depot-a-terme", "credit", "transfert", "micro-assurance"]

# Caisses : liste telle que publiée sur la page « Nos caisses » du site officiel (localité entre parenthèses).
CAISSES = {
 "Vallée du Bandama": [("Katiola", "Katiola"), ("Boniérédougou", "Dabakala")],
 "Lagunes": [("Macory", "Abidjan"), ("Koumassi", "Abidjan"), ("Yopougon Millionnaire", "Abidjan"), ("Bingerville", "Abidjan"), ("Ahouanou", "Grand-Lahou")],
 "Agnéby": [("Tiassalé", "Agboville"), ("N'Zianouan", "Agboville"), ("Bacon", "Bacon")],
 "Zanzan": [("Bondoukou", "Bondoukou"), ("Tabagne", "Bondoukou"), ("Gouméré", "Bondoukou"), ("Assuéfry", "Tanda"), ("Transua", "Tanda")],
 "Sud-Comoé": [("Aboisso", "Aboisso"), ("Affiénou", "Aboisso"), ("Koffikro", "Aboisso"), ("N'Zikro", "Aboisso")],
}


def e(s):
    return html.escape(s, quote=True)


def svc(sid):
    return next(s for s in SERVICES if s["id"] == sid)


def head(title, desc, page, og_img="assets/img/femme-sourire.jpg", ld=False):
    ldjson = ""
    if ld:
        ldjson = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "FinancialService",
            "name": "RCMEC-CI - " + FULL, "url": "https://rcmec-ci.com/", "logo": "assets/logo.png",
            "foundingDate": "1995", "slogan": SLOGAN, "telephone": TEL, "email": MAIL, "areaServed": "CI", "sameAs": [LI, IG],
            "address": {"@type": "PostalAddress",
                        "streetAddress": "Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bât. A, 3e étage",
                        "postOfficeBoxNumber": "05 BP 822", "addressLocality": "Abidjan", "addressCountry": "CI"}},
            ensure_ascii=False) + "</script>"
    items = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == page else ""}>{l}</a>' for h, l in NAV)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0a2342">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="canonical" href="https://rcmec-ci.com/{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&family=Source+Sans+3:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{ldjson}
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="progress" id="progress" aria-hidden="true"></div>
<div class="util">
  <div class="container util__in">
    <ul class="util__info">
      <li><i data-lucide="phone"></i><a href="tel:{TEL_HREF}">{TEL}</a></li>
      <li class="hide-sm"><i data-lucide="mail"></i><a href="mailto:{MAIL}">{MAIL}</a></li>
    </ul>
    <div class="util__soc"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></div>
  </div>
</div>
<header class="nav" id="nav">
  <div class="container nav__in">
    <a class="brand" href="index.html" aria-label="RCMEC-CI, accueil"><img src="assets/logo.png" alt="RCMEC-CI" width="150" height="58"></a>
    <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="menu" id="menu" aria-label="Navigation principale">
      {items}
      <a class="btn menu__cta" href="contact.html">Ouvrir un compte<i data-lucide="arrow-right"></i></a>
    </nav>
  </div>
</header>
<main id="main">
'''


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''</main>
<footer class="footer">
  <div class="container footer__grid">
    <div class="footer__brand">
      <div class="logo-card"><img src="assets/logo.png" alt="RCMEC-CI" width="150" height="58" loading="lazy"></div>
      <p>{FULL}. {SLOGAN}.</p>
      <ul class="soc">
        <li><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a></li>
        <li><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a></li>
        <li><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></li>
      </ul>
    </div>
    <div><h4>Navigation</h4><ul>{links}</ul></div>
    <div><h4>Siège (Direction Générale)</h4>
      <ul class="fcontact"><li><i data-lucide="map-pin"></i><span>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</span></li>
      <li><i data-lucide="phone"></i><a href="tel:{TEL_HREF}">{TEL}</a></li><li><i data-lucide="mail"></i><a href="mailto:{MAIL}">{MAIL}</a></li></ul>
    </div>
  </div>
  <div class="container legal">
    <p>RCMEC-CI, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire.</p>
    <p>Photos : <a href="https://www.pexels.com" target="_blank" rel="noopener">Pexels</a> (licence libre), illustrations à remplacer par des photos du réseau. © <span id="y"></span> RCMEC-CI. Tous droits réservés.</p>
  </div>
</footer>
<script src="js/lucide.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>
'''


def pagehead(title, sub, img):
    return f'''<section class="pagehead" style="--img:url(../assets/img/{img})">
  <div class="container">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a><i data-lucide="chevron-right"></i><span>{e(title)}</span></nav>
    <h1>{e(title)}</h1>
    {f"<p>{e(sub)}</p>" if sub else ""}
  </div>
</section>
'''


def ctaband():
    return f'''<section class="ctaband">
  <div class="container ctaband__in">
    <div><h2>Ouvrir un compte chez RCMEC-CI</h2></div>
    <a class="btn btn--ghost" href="contact.html">Ouvrir un compte <i data-lucide="arrow-right"></i></a>
  </div>
</section>
'''


def svc_card(s):
    return f'''<a class="card" href="services.html#{s["id"]}">
  <span class="card__ico"><i data-lucide="{s["ico"]}"></i></span><h3>{s["t"]}</h3>
  <p>{e(s["d"])}</p><span class="card__go">En savoir plus<i data-lucide="arrow-right"></i></span></a>'''


def sec_head(label, title, sub="", center=True):
    return f'<header class="sec-head{" sec-head--l" if not center else ""}"><span class="eyebrow">{e(label)}</span><h2>{title}</h2>{f"<p>{e(sub)}</p>" if sub else ""}</header>'


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("écrit", name)


def cs_items():
    items = ""
    for r, lst in CAISSES.items():
        for n, v in lst:
            items += f'<div class="cs" data-region="{e(r)}" data-q="{e((n + " " + v + " " + r).lower())}"><em>Région {e(r)}</em><strong>Caisse de {e(n)}</strong><small>({e(v)})</small></div>\n'
    return items


# ---------------------------------------------------------------- ACCUEIL
def page_index():
    cards = "".join(svc_card(svc(i)) for i in HOME_SERVICES)
    return head("RCMEC-CI | " + FULL, f"RCMEC-CI, faîtière de microfinance (SFD agréé) créée en 1995. 18 caisses dans plus de 10 régions de Côte d'Ivoire. {SLOGAN}.",
                "index.html", ld=True) + f'''
<section class="hero hero--one" style="--img:url(../assets/img/femme-sourire.jpg)">
  <div class="container hero__in">
    <p class="chip-label">{FULL}</p>
    <h1>{SLOGAN}</h1>
    <p class="lead">Faîtière de microfinance, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire, depuis 1995.</p>
    <div class="btns"><a class="btn" href="contact.html">Ouvrir un compte <i data-lucide="arrow-right"></i></a><a class="btn btn--ghost" href="services.html">Nos services</a></div>
  </div>
</section>

<section class="needs">
  <div class="container"><div class="needs__box facts">
    <div class="fact"><b data-count="1995" data-plain="1">0</b><span>Année de création</span></div>
    <div class="fact"><b data-count="18">0</b><span>Caisses de base</span></div>
    <div class="fact"><b data-count="10" data-prefix="+">0</b><span>Régions</span></div>
  </div></div>
</section>

<section class="section">
  <div class="container">
    {sec_head("Nos services", "Nos produits et services")}
    <div class="cards cards--3">{cards}</div>
    <p class="center"><a class="btn btn--outline" href="services.html">Tous nos services <i data-lucide="arrow-right"></i></a></p>
  </div>
</section>

<section class="section section--tint">
  <div class="container split">
    <div class="split__img"><img src="assets/img/vendeur-banane.jpg" alt="Commerçant sur un marché" loading="lazy"></div>
    <div>
      {sec_head("À propos de nous", "Une faîtière de microfinance", center=False)}
      <p class="muted">Nous représentons une solution durable d'offre de services financiers aux populations qui n'ont pas accès aux produits des banques classiques. Depuis 1995, nous accompagnons ces populations vulnérables dans la réalisation de leurs projets et le développement de leur environnement.</p>
      <a class="btn" href="a-propos.html">En savoir plus <i data-lucide="arrow-right"></i></a>
    </div>
  </div>
</section>
''' + ctaband() + footer()


# --------------------------------------------------------------- A PROPOS
def page_apropos():
    vals = [("handshake", "Solidarité"), ("home", "Proximité"), ("landmark", "Inclusion financière"), ("trending-up", "Autonomisation économique"), ("shield-check", "Confiance")]
    vh = "".join(f'<article><span class="ico"><i data-lucide="{i}"></i></span><h3>{t}</h3></article>' for i, t in vals)
    cible = ["Populations vulnérables ou exclues des banques classiques", "Opérateurs économiques du secteur informel", "Agriculteurs", "Commerçants", "Artisans", "Entrepreneurs et PME"]
    ch = "".join(f"<li>{e(c)}</li>" for c in cible)
    return head("À propos | RCMEC-CI", f"Le RCMEC-CI est une faîtière de microfinance créée en 1995, qui compte dix-huit caisses de base implantées en priorité en zone rurale.", "a-propos.html") + \
        pagehead("À propos de nous", "", "reunion-equipe.jpg") + f'''
<section class="section">
  <div class="container split">
    <div class="split__img"><img src="assets/img/vendeur-banane.jpg" alt="Commerçant sur un marché" loading="lazy"><div class="badge-circle"><b>30+</b><span>ans d'existence</span></div></div>
    <div>
      {sec_head("Qui sommes-nous", "Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire", center=False)}
      <p class="muted">Le RCMEC-CI est une faîtière de microfinance qui compte à ce jour dix-huit caisses. Nous sommes implantés en priorité en zone rurale. Nous représentons une solution durable d'offre de services financiers aux populations qui n'ont pas accès aux produits des banques classiques.</p>
      <p class="muted">Depuis 1995, nous accompagnons ces populations vulnérables dans la réalisation de leurs projets et le développement de leur environnement.</p>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container duo">
    <article class="panel"><span class="eyebrow">Notre mission</span><p>Collecter et gérer l'épargne de nos adhérents, accorder des crédits adaptés à moindre coût à ceux qui en expriment le besoin, et protéger les populations contre l'endettement usurier.</p></article>
    <article class="panel"><span class="eyebrow">Notre objectif</span><p>Apporter aux caisses un appui adéquat afin de leur permettre d'offrir des services financiers de qualité, accessibles à tous les opérateurs économiques en général et particulièrement à ceux du monde rural, semi-urbain, urbain et du secteur informel.</p></article>
  </div>
</section>

<section class="section">
  <div class="container">
    {sec_head("Nos valeurs", "Ce qui nous guide")}
    <div class="vals vals--5">{vh}</div>
  </div>
</section>

<section class="section section--tint">
  <div class="container split split--rev">
    <div class="split__img"><img src="assets/img/artisane.jpg" alt="Commerçante dans sa boutique" loading="lazy"></div>
    <div>
      {sec_head("À qui nous nous adressons", "Notre cible", center=False)}
      <ul class="ticks">{ch}</ul>
    </div>
  </div>
</section>
''' + ctaband() + footer()


# -------------------------------------------------------------- SERVICES
def page_services():
    cards = "".join(svc_card(s) for s in SERVICES)
    rows = ""
    for i, s in enumerate(SERVICES):
        media = f'<img src="assets/img/{s["img"]}" alt="{e(s["t"])}" loading="lazy">' if s.get("img") else f'<div class="svc__panel"><i data-lucide="{s["ico"]}"></i></div>'
        quote = f'<p class="quote">« {e(s["q"])} »</p>' if s.get("q") else ""
        rows += f'''<article class="svc{' svc--rev' if i % 2 else ''}" id="{s["id"]}">
  <div class="svc__media">{media}</div>
  <div class="svc__body"><h2>{s["t"]}</h2><p class="muted">{e(s["d"])}</p>{quote}
  <a class="btn" href="contact.html">Nous contacter <i data-lucide="arrow-right"></i></a></div>
</article>
'''
    return head("Nos services | RCMEC-CI", "Épargne, parts sociales rémunérées, dépôts à terme, crédit, crédit agricole, prêt scolaire, RCMEC Sécurité Étude, transfert rapide d'argent et micro-assurance.", "services.html", "assets/img/vendeur-banane.jpg") + \
        pagehead("Nos services", "", "vendeur-banane.jpg") + f'''
<section class="section section--tint">
  <div class="container"><div class="cards cards--3">{cards}</div></div>
</section>
<section class="section"><div class="container svclist">{rows}</div></section>
''' + ctaband() + footer()


# ------------------------------------------------------------- SIMULATEUR
def page_simulateur():
    return head("Simulateur | RCMEC-CI", "Estimez en FCFA la mensualité d'un crédit ou les intérêts d'un dépôt, avec le taux communiqué par votre caisse.", "simulateur.html") + \
        pagehead("Simulateur", "Estimation en FCFA : montant, durée et taux.", "femme-sourire.jpg") + f'''
<section class="section">
  <div class="container sim">
    <div class="sim__intro">
      {sec_head("Outil d'estimation", "Simulez un crédit ou une épargne", center=False)}
      <p class="muted">Renseignez le montant, la durée et <strong>le taux communiqué par votre caisse</strong>. Ce simulateur ne contient aucun taux officiel : il calcule simplement une estimation à partir des valeurs que vous saisissez.</p>
      <p class="note"><i data-lucide="info"></i>Estimation indicative, sans valeur contractuelle.</p>
    </div>
    <div class="sim__box">
      <div class="tabs" role="tablist">
        <button class="tab is-on" role="tab" data-tab="credit" aria-selected="true">Crédit</button>
        <button class="tab" role="tab" data-tab="epargne" aria-selected="false">Dépôt à terme</button>
      </div>
      <form id="sim-credit" class="simform" data-panel="credit" onsubmit="return false">
        <label>Montant <output id="c-amount-o"></output><input id="c-amount" type="range" min="50000" max="10000000" step="50000" value="1000000"></label>
        <label>Durée <output id="c-dur-o"></output><input id="c-dur" type="range" min="3" max="48" step="1" value="12"></label>
        <label>Taux annuel (%)<input id="c-rate" type="number" min="0" max="100" step="0.1" placeholder="Taux communiqué par votre caisse"></label>
        <div class="result"><div><span>Mensualité estimée</span><b id="c-month">-</b></div><div><span>Coût total du crédit</span><b id="c-cost">-</b></div><div><span>Total à rembourser</span><b id="c-total">-</b></div></div>
      </form>
      <form id="sim-epargne" class="simform" data-panel="epargne" onsubmit="return false" hidden>
        <label>Somme placée <output id="e-amount-o"></output><input id="e-amount" type="range" min="50000" max="20000000" step="50000" value="1000000"></label>
        <label>Durée du placement <output id="e-dur-o"></output><input id="e-dur" type="range" min="3" max="60" step="1" value="12"></label>
        <label>Taux annuel (%)<input id="e-rate" type="number" min="0" max="100" step="0.1" placeholder="Taux communiqué par votre caisse"></label>
        <div class="result"><div><span>Intérêts estimés</span><b id="e-int">-</b></div><div><span>Capital au terme</span><b id="e-total">-</b></div></div>
      </form>
      <a class="btn block" href="contact.html">Nous contacter <i data-lucide="arrow-right"></i></a>
    </div>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CAISSES
def page_caisses():
    chips = '<button type="button" class="chip on" data-region="Toutes">Toutes</button>' + "".join(f'<button type="button" class="chip" data-region="{e(r)}">{e(r)}</button>' for r in CAISSES)
    return head("Nos caisses | RCMEC-CI", "Les caisses du RCMEC-CI en Côte d'Ivoire : Vallée du Bandama, Lagunes, Agnéby, Zanzan et Sud-Comoé. Siège à Cocody II Plateaux, Abidjan.", "caisses.html", "assets/img/artisane.jpg") + \
        pagehead("Nos caisses", "Dix-huit caisses de base, dans plus de 10 régions de la Côte d'Ivoire.", "artisane.jpg") + f'''
<section class="section section--tint">
  <div class="container">
    <div class="dir">
      <div class="dir__tools">
        <input id="q" type="search" placeholder="Rechercher une localité" aria-label="Rechercher une localité">
        <div class="chips" id="chips">{chips}</div>
      </div>
      <div class="dir__grid" id="dir">
{cs_items()}      </div>
      <p class="empty" id="empty" hidden>Aucune caisse trouvée.</p>
      <aside class="hq">
        <div>
          <h3><i data-lucide="building-2"></i>Siège (Direction Générale)</h3>
          <p>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</p>
          <p><i data-lucide="phone"></i> {TEL}</p>
        </div>
        <a class="btn btn--ghost" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte <i data-lucide="arrow-right"></i></a>
      </aside>
    </div>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CONTACT
def page_contact():
    return head("Contact | RCMEC-CI", f"Contactez le RCMEC-CI : Cocody II Plateaux, Carrefour Duncan, Abidjan. Téléphone {TEL}, e-mail {MAIL}.", "contact.html", "assets/img/artisane.jpg") + \
        pagehead("Contact", "", "artisane.jpg") + f'''
<section class="section section--tint">
  <div class="container contact">
    <div class="contact__photo">
      <img src="assets/img/artisane.jpg" alt="Commerçante souriante dans sa boutique" loading="lazy">
      <div class="contact__info">
        <ul>
          <li><i data-lucide="map-pin"></i><span>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</span></li>
          <li><i data-lucide="phone"></i><a href="tel:{TEL_HREF}">{TEL}</a></li>
          <li><i data-lucide="mail"></i><a href="mailto:{MAIL}">{MAIL}</a></li>
        </ul>
      </div>
    </div>
    <form class="cform" id="cform">
      <span class="eyebrow">Contactez-nous</span>
      <h2>Ouvrir un compte</h2>
      <div class="row">
        <input name="nom" placeholder="Nom et prénom" required autocomplete="name" aria-label="Nom et prénom">
        <input name="email" type="email" placeholder="E-mail" required autocomplete="email" aria-label="E-mail">
      </div>
      <div class="row">
        <select name="objet" aria-label="Objet"><option>Ouvrir un compte</option><option>Épargne</option><option>Crédit</option><option>Dépôt à terme</option><option>Transfert d'argent</option><option>Micro-assurance</option><option>Autre demande</option></select>
        <input name="tel" type="tel" placeholder="Téléphone" autocomplete="tel" aria-label="Téléphone">
      </div>
      <textarea name="msg" rows="4" placeholder="Votre message" required aria-label="Message"></textarea>
      <button class="btn" type="submit">Envoyer <i data-lucide="arrow-right"></i></button>
      <p class="fine">Le bouton ouvre votre application e-mail avec le message pré-rempli, adressé à {MAIL}.</p>
    </form>
  </div>
</section>
''' + footer()


if __name__ == "__main__":
    write("index.html", page_index())
    write("a-propos.html", page_apropos())
    write("services.html", page_services())
    write("simulateur.html", page_simulateur())
    write("caisses.html", page_caisses())
    write("contact.html", page_contact())
    urls = ["" if h == "index.html" else h for h, _ in NAV]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                "".join(f"  <url><loc>https://rcmec-ci.com/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
