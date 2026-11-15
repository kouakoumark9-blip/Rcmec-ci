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
GMAPS_Q = "Carrefour+Duncan,+II+Plateaux,+Cocody,+Abidjan,+Côte+d'Ivoire"
GMAPS = "https://www.google.com/maps/search/?api=1&query=" + GMAPS_Q.replace("'", "%27")
GMAPS_EMBED = "https://www.google.com/maps?q=" + GMAPS_Q.replace("'", "%27") + "&output=embed"
SLOGAN = "Avec vous au quotidien pour garantir votre épargne et assurer votre avenir"
FULL = "Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire"

NAV = [("index.html", "Accueil"), ("a-propos.html", "À propos"), ("services.html", "Nos services"),
       ("caisses.html", "Nos caisses"), ("simulateur.html", "Simulateur"), ("contact.html", "Contact")]

# Menu du haut (ordre demandé par RCMEC-CI)
HEAD_NAV = [("index.html", "Accueil"), ("services.html", "Nos services"), ("caisses.html", "Nos caisses"),
            ("a-propos.html", "À propos"), ("contact.html", "Contact")]

# Services : libellés et descriptions issus de la fiche, des affiches et du site officiel.
SERVICES = [
 dict(id="epargne", ico="piggy-bank", t="Épargne",
      d="Comptes d'épargne sécurisés pour les particuliers, les groupements et les professionnels.",
      q="Avec nous, votre épargne est en sécurité."),
 dict(id="parts-sociales", ico="users", t="Parts sociales rémunérées",
      d="Participation au capital mutualiste permettant de devenir membre sociétaire et de percevoir des dividendes."),
 dict(id="depot-a-terme", ico="lock", t="Dépôts à terme (DAT)",
      d="Placement d'une somme bloquée sur une durée définie avec un taux d'intérêt avantageux."),
 dict(id="credit", ico="hand-coins", t="Crédit",
      d="Financement de projets, fonds de roulement, crédits agricoles et soutien aux activités génératrices de revenus. Des crédits adaptés, à moindre coût."),
 dict(id="credit-agricole", ico="sprout", t="Crédit agricole",
      d="Votre projet agricole mérite un coup de pouce !", q="La référence en milieu rural et défavorisé."),
 dict(id="pret-scolaire", ico="graduation-cap", t="Prêt scolaire",
      d="Le prêt scolaire : la clé d'une rentrée réussie."),
 dict(id="securite-etude", ico="shield-check", t="RCMEC Sécurité Étude",
      d="RCMEC Sécurité Étude : l'assurance qui protège chaque parcours scolaire."),
 dict(id="transfert", ico="send", t="Transfert rapide d'argent",
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
    items = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == page else ""}>{l}</a>' for h, l in HEAD_NAV)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0b2545">
<link rel="icon" href="assets/favicon.png" type="image/png">
<link rel="canonical" href="https://rcmec-ci.com/{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{ldjson}
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<div class="util">
  <div class="wrap util__in">
    <div class="util__l"><a href="tel:{TEL_HREF}"><i data-lucide="phone"></i>{TEL}</a><a class="hide-sm" href="mailto:{MAIL}"><i data-lucide="mail"></i>{MAIL}</a></div>
    <div class="util__r"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></div>
  </div>
</div>
<header class="nav" id="nav">
  <div class="wrap nav__in">
    <a class="brand" href="index.html" aria-label="RCMEC-CI, accueil"><img src="assets/logo-mark.png" alt="RCMEC-CI" width="118" height="52"></a>
    <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="menu" id="menu" aria-label="Navigation principale">
      {items}
    </nav>
  </div>
</header>
<main id="main">
'''


def footer():
    links = "".join(f'<li><a href="{h}">{l}</a></li>' for h, l in NAV)
    return f'''</main>
<footer class="footer">
  <div class="wrap footer__grid">
    <div class="footer__brand">
      <div class="logo-card"><img src="assets/logo.png" alt="RCMEC-CI, Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire" width="178" height="72" loading="lazy"></div>
      <p>{FULL}</p>
      <p class="footer__slogan">{SLOGAN}.</p>
    </div>
    <div><h4>Navigation</h4><ul>{links}</ul></div>
    <div><h4>Siège, Direction Générale</h4>
      <address>Cocody II Plateaux, Carrefour Duncan,<br>en face de l'ex-ADDR, Immeuble SICOGI,<br>Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</address>
      <p><a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
      <div class="soc"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></div>
    </div>
  </div>
  <div class="wrap legal">
    <span>© <span id="y"></span> RCMEC-CI. Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire.</span>
    <span>Photos : <a href="https://www.pexels.com" target="_blank" rel="noopener">Pexels</a>, à remplacer par des photos du réseau.</span>
  </div>
</footer>
<script src="js/lucide.min.js"></script>
<script src="js/main.js"></script>
</body>
</html>
'''


def pagehead(title, sub=""):
    return f'''<section class="pagehead">
  <div class="wrap">
    <nav class="crumbs" aria-label="Fil d'Ariane"><a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>{e(title)}</span></nav>
    <h1>{e(title)}</h1>
    {f"<p>{e(sub)}</p>" if sub else ""}
  </div>
</section>
'''


def cta(text=""):
    p = f"<p>{e(text)}</p>" if text else ""
    return f'''<section class="cta">
  <div class="wrap cta__in">
    <div><h2>Ouvrir un compte chez RCMEC-CI</h2>{p}</div>
    <a class="btn btn--light" href="contact.html">Nous contacter</a>
  </div>
</section>
'''


def head2(kicker, title, link=None):
    l = f'<a class="more" href="{link[0]}">{link[1]}<i data-lucide="arrow-right"></i></a>' if link else ""
    return f'<div class="sh"><div><span class="kicker">{e(kicker)}</span><h2>{title}</h2></div>{l}</div>'


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("écrit", name)


def cs_items():
    items = ""
    for r, lst in CAISSES.items():
        for n, v in lst:
            items += f'<div class="cs" data-region="{e(r)}" data-q="{e((n + " " + v + " " + r).lower())}"><strong>Caisse de {e(n)}</strong><span>({e(v)})</span><em>{e(r)}</em></div>\n'
    return items


# ---------------------------------------------------------------- ACCUEIL
TILES = [("parts-sociales", "reunion-equipe.jpg"), ("depot-a-terme", "equipe-bureau.jpg"), ("credit-agricole", "cabosse-cacao.jpg")]

# Illustrations et phrases de l'affiche fournie par RCMEC-CI
PICS = [("epargne", "epargne.png", "Épargne", "Construisez votre avenir en toute sécurité"),
        ("credit", "credit.png", "Crédit", "Financez vos projets agricoles, commerciaux & personnels"),
        ("micro-assurance", "assurance.png", "Assurance", "Protégez votre famille et vos biens"),
        ("transfert", "transfert.png", "Transfert d'argent", "Recevez et envoyez de l'argent facilement")]
PIC_BY_ID = {sid: f for sid, f, _, _ in PICS}


def page_index():
    tiles = ""
    for sid, img in TILES:
        s = next(x for x in SERVICES if x["id"] == sid)
        tiles += f'''<a class="tile" href="services.html#{s["id"]}">
  <img src="assets/img/{img}" alt="" loading="lazy">
  <span class="tile__body"><h3>{s["t"]}</h3><p>{e(s["d"])}</p><span class="tile__more">En savoir plus<i data-lucide="arrow-right"></i></span></span>
</a>
'''
    regions = "".join(f"<li>{e(r)}</li>" for r in CAISSES)
    pics = "".join(f'''<a class="pic-card" href="services.html#{sid}"><img src="assets/ico/{f}" alt="" loading="lazy"><h3>{t}</h3><p>{e(p)}</p><span class="more">En savoir plus<i data-lucide="arrow-right"></i></span></a>
''' for sid, f, t, p in PICS)
    return head("RCMEC-CI | " + FULL, f"RCMEC-CI, faîtière de microfinance (SFD agréé) créée en 1995. 18 caisses dans plus de 10 régions de Côte d'Ivoire. {SLOGAN}.",
                "index.html", ld=True) + f'''
<section class="hero2" style="--img:url(../assets/img/agricultrice.jpg)">
  <div class="wrap hero2__in"><div class="hero2__card">
    <span class="kicker">{FULL}</span>
    <h1>{SLOGAN}</h1>
    <p class="lead">Faîtière de microfinance, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire, depuis 1995.</p>
    <div class="btns"><a class="btn" href="contact.html">Ouvrir un compte</a><a class="btn btn--outline" href="services.html">Découvrir nos services</a></div>
  </div></div>
</section>

<section class="picsec">
  <div class="wrap"><div class="pics">{pics}</div></div>
</section>

<section class="statsband" aria-label="Chiffres clés">
  <div class="wrap statsband__in">
    <div><b data-count="1995" data-plain="1">1995</b><span>Année de création</span></div>
    <div><b data-count="18">18</b><span>Caisses de base</span></div>
    <div><b data-count="10" data-prefix="+">+10</b><span>Régions</span></div>
    <div><b data-count="30" data-prefix="+">+30</b><span>Ans d'existence</span></div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap duo">
    <div class="statement"><span class="kicker">Notre mission</span><p>Collecter et gérer l'épargne de nos adhérents, accorder des crédits adaptés à moindre coût à ceux qui en expriment le besoin, et protéger les populations contre l'endettement usurier.</p></div>
    <div class="statement"><span class="kicker">Notre objectif</span><p>Apporter aux caisses un appui adéquat afin de leur permettre d'offrir des services financiers de qualité, accessibles à tous les opérateurs économiques en général et particulièrement à ceux du monde rural, semi-urbain, urbain et du secteur informel.</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head2("Nos services", "Autres produits et services", ("services.html", "Tous nos services"))}
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="banner2">
  <div class="banner2__txt">
    <div class="banner2__in">
      <span class="kicker kicker--l">Prêt scolaire · RCMEC Sécurité Étude</span>
      <h2>La clé d'une rentrée réussie</h2>
      <p>RCMEC Sécurité Étude : l'assurance qui protège chaque parcours scolaire.</p>
      <a class="btn btn--light" href="services.html#pret-scolaire">Découvrir</a>
    </div>
  </div>
  <div class="banner2__img" role="img" aria-label="Élève souriante" style="--img:url(../assets/img/ecoliere.jpg)"></div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split__img split__img--wide"><img src="assets/img/conseiller-rcmec.jpg" width="1536" height="1024" alt="Conseiller RCMEC-CI au bureau, avec en arrière-plan un marché et un village de Côte d'Ivoire" loading="lazy"></div>
    <div class="split__txt">
      <span class="kicker">À propos de nous</span>
      <h2>Une faîtière de microfinance</h2>
      <p>Nous représentons une solution durable d'offre de services financiers aux populations qui n'ont pas accès aux produits des banques classiques. Depuis 1995, nous accompagnons ces populations vulnérables dans la réalisation de leurs projets et le développement de leur environnement.</p>
      <p>Nous nous adressons aux populations vulnérables ou exclues des banques classiques, aux opérateurs économiques du secteur informel, aux agriculteurs, commerçants, artisans, entrepreneurs et PME.</p>
      <ul class="force">
        <li><i data-lucide="landmark"></i><span><b>18 caisses actives</b>implantées dans plus de 10 régions de la Côte d'Ivoire</span></li>
        <li><i data-lucide="users"></i><span><b>Un personnel qualifié</b>adapté pour répondre à vos besoins, dans chacune de nos agences</span></li>
        <li><i data-lucide="sprout"></i><span><b>Implantés en priorité en zone rurale</b>au service des populations n'ayant pas accès aux banques classiques</span></li>
      </ul>
      <a class="more" href="a-propos.html">En savoir plus<i data-lucide="arrow-right"></i></a>
    </div>
  </div>
</section>

<section class="section section--tint mapsec">
  <div class="wrap">
    {head2("Nous trouver", "Notre siège à Abidjan")}
    <div class="mapgrid">
      <div class="mapgrid__info">
        <h3>Siège, Direction Générale</h3>
        <address>Cocody II Plateaux, Carrefour Duncan,<br>en face de l'ex-ADDR, Immeuble SICOGI,<br>Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</address>
        <p><a href="tel:{TEL_HREF}">{TEL}</a><br><a href="mailto:{MAIL}">{MAIL}</a></p>
        <a class="more" target="_blank" rel="noopener" href="{GMAPS}">Ouvrir dans Google Maps<i data-lucide="arrow-right"></i></a>
      </div>
      <div class="mapgrid__map"><iframe title="Carte : siège du RCMEC-CI, Cocody II Plateaux, Abidjan" src="{GMAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
    </div>
  </div>
</section>

<section class="regions">
  <div class="wrap regions__in">
    <div>
      <span class="kicker kicker--l">Nos caisses</span>
      <h2>Dans plus de 10 régions de la Côte d'Ivoire</h2>
      <ul class="regions__list">{regions}</ul>
    </div>
    <a class="btn btn--light" href="caisses.html">Trouver ma caisse</a>
  </div>
</section>
''' + cta("Ne soyez plus inquiets, vos projets et votre entreprise sont en de bonnes mains.") + footer()


# --------------------------------------------------------------- A PROPOS
def page_apropos():
    vals = [("handshake", "Solidarité"), ("home", "Proximité"), ("landmark", "Inclusion financière"), ("trending-up", "Autonomisation économique"), ("shield-check", "Confiance")]
    vh = "".join(f'<li><i data-lucide="{i}"></i><span>{t}</span></li>' for i, t in vals)
    cible = ["Populations vulnérables ou exclues des banques classiques", "Opérateurs économiques du secteur informel", "Agriculteurs", "Commerçants", "Artisans", "Entrepreneurs et PME"]
    ch = "".join(f"<li>{e(c)}</li>" for c in cible)
    return head("À propos | RCMEC-CI", "Le RCMEC-CI est une faîtière de microfinance créée en 1995, qui compte dix-huit caisses de base implantées en priorité en zone rurale.", "a-propos.html") + \
        pagehead("À propos de nous") + f'''
<section class="section">
  <div class="wrap split">
    <div class="split__txt">
      <span class="kicker">Qui sommes-nous</span>
      <h2>Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire</h2>
      <p>Le RCMEC-CI est une faîtière de microfinance qui compte à ce jour dix-huit caisses. Nous sommes implantés en priorité en zone rurale. Nous représentons une solution durable d'offre de services financiers aux populations qui n'ont pas accès aux produits des banques classiques.</p>
      <p>Depuis 1995, nous accompagnons ces populations vulnérables dans la réalisation de leurs projets et le développement de leur environnement.</p>
    </div>
    <div class="split__img"><img src="assets/img/vendeur-banane.jpg" alt="Commerçant sur un marché" loading="lazy"></div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap duo">
    <div class="statement"><span class="kicker">Notre mission</span><p>Collecter et gérer l'épargne de nos adhérents, accorder des crédits adaptés à moindre coût à ceux qui en expriment le besoin, et protéger les populations contre l'endettement usurier.</p></div>
    <div class="statement"><span class="kicker">Notre objectif</span><p>Apporter aux caisses un appui adéquat afin de leur permettre d'offrir des services financiers de qualité, accessibles à tous les opérateurs économiques en général et particulièrement à ceux du monde rural, semi-urbain, urbain et du secteur informel.</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head2("Nos valeurs", "Ce qui nous guide")}
    <ul class="values">{vh}</ul>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {head2("À qui nous nous adressons", "Notre cible")}
    <ul class="checks">{ch}</ul>
  </div>
</section>
''' + cta() + footer()


# -------------------------------------------------------------- SERVICES
def page_services():
    rows = ""
    for n, s in enumerate(SERVICES, 1):
        quote = f'<p class="quote">« {e(s["q"])} »</p>' if s.get("q") else ""
        rows += f'''<article class="row" id="{s["id"]}">
  <div class="row__n">{n:02d}</div>
  <div class="row__t">{f'<img class="pic" src="assets/ico/{PIC_BY_ID[s["id"]]}" alt="" loading="lazy">' if s["id"] in PIC_BY_ID else f'<i data-lucide="{s["ico"]}"></i>'}<h2>{s["t"]}</h2></div>
  <div class="row__b"><p>{e(s["d"])}</p>{quote}<a class="more" href="contact.html">Nous contacter<i data-lucide="arrow-right"></i></a></div>
</article>
'''
    return head("Nos services | RCMEC-CI", "Épargne, parts sociales rémunérées, dépôts à terme, crédit, crédit agricole, prêt scolaire, RCMEC Sécurité Étude, transfert rapide d'argent et micro-assurance.", "services.html", "assets/img/vendeur-banane.jpg") + \
        pagehead("Nos services") + f'''
<section class="section"><div class="wrap rows">{rows}</div></section>
''' + cta() + footer()


# ------------------------------------------------------------- SIMULATEUR
def page_simulateur():
    return head("Simulateur | RCMEC-CI", "Estimez en FCFA la mensualité d'un crédit ou les intérêts d'un dépôt, avec le taux communiqué par votre caisse.", "simulateur.html") + \
        pagehead("Simulateur", "Estimation en FCFA : montant, durée et taux.") + f'''
<section class="section">
  <div class="wrap sim">
    <div class="sim__intro">
      <span class="kicker">Outil d'estimation</span>
      <h2>Simulez un crédit ou une épargne</h2>
      <p>Renseignez le montant, la durée et <strong>le taux communiqué par votre caisse</strong>. Ce simulateur ne contient aucun taux officiel : il calcule simplement une estimation à partir des valeurs que vous saisissez.</p>
      <p class="note">Estimation indicative, sans valeur contractuelle.</p>
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
      <a class="btn block" href="contact.html">Nous contacter</a>
    </div>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CAISSES
def page_caisses():
    chips = '<button type="button" class="chip on" data-region="Toutes">Toutes</button>' + "".join(f'<button type="button" class="chip" data-region="{e(r)}">{e(r)}</button>' for r in CAISSES)
    return head("Nos caisses | RCMEC-CI", "Les caisses du RCMEC-CI en Côte d'Ivoire : Vallée du Bandama, Lagunes, Agnéby, Zanzan et Sud-Comoé. Siège à Cocody II Plateaux, Abidjan.", "caisses.html", "assets/img/artisane.jpg") + \
        pagehead("Nos caisses", "Dix-huit caisses de base, dans plus de 10 régions de la Côte d'Ivoire.") + f'''
<section class="section">
  <div class="wrap">
    <div class="dir__tools">
      <input id="q" type="search" placeholder="Rechercher une localité" aria-label="Rechercher une localité">
      <div class="chips" id="chips">{chips}</div>
    </div>
    <div class="dir__grid" id="dir">
{cs_items()}    </div>
    <p class="empty" id="empty" hidden>Aucune caisse trouvée.</p>
    <aside class="hq">
      <div>
        <span class="kicker kicker--l">Siège, Direction Générale</span>
        <p>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05 · {TEL}</p>
      </div>
      <a class="btn btn--light" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte</a>
    </aside>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CONTACT
def page_contact():
    return head("Contact | RCMEC-CI", f"Contactez le RCMEC-CI : Cocody II Plateaux, Carrefour Duncan, Abidjan. Téléphone {TEL}, e-mail {MAIL}.", "contact.html", "assets/img/artisane.jpg") + \
        pagehead("Contact") + f'''
<section class="section">
  <div class="wrap contact">
    <div class="contact__info">
      <span class="kicker">Nos coordonnées</span>
      <h2>Siège, Direction Générale</h2>
      <dl>
        <dt>Adresse</dt><dd>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</dd>
        <dt>Téléphone</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a></dd>
        <dt>E-mail</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd>
        <dt>Réseaux sociaux</dt><dd class="soc2"><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a></dd>
      </dl>
      <a class="more" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte<i data-lucide="arrow-right"></i></a>
    </div>
    <form class="cform" id="cform">
      <span class="kicker">Écrivez-nous</span>
      <h2>Ouvrir un compte</h2>
      <div class="row2">
        <input name="nom" placeholder="Nom et prénom" required autocomplete="name" aria-label="Nom et prénom">
        <input name="email" type="email" placeholder="E-mail" required autocomplete="email" aria-label="E-mail">
      </div>
      <div class="row2">
        <select name="objet" aria-label="Objet"><option>Ouvrir un compte</option><option>Épargne</option><option>Crédit</option><option>Dépôt à terme</option><option>Transfert d'argent</option><option>Micro-assurance</option><option>Autre demande</option></select>
        <input name="tel" type="tel" placeholder="Téléphone" autocomplete="tel" aria-label="Téléphone">
      </div>
      <textarea name="msg" rows="5" placeholder="Votre message" required aria-label="Message"></textarea>
      <button class="btn" type="submit">Envoyer</button>
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
