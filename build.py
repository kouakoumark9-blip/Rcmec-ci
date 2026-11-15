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
      d="Participation au capital mutualiste permettant de devenir membre et de recevoir une part des bénéfices."),
 dict(id="depot-a-terme", ico="lock", t="Dépôts à terme (DAT)",
      d="Placement d'une somme bloquée sur une durée définie avec un taux d'intérêt avantageux."),
 dict(id="credit", ico="hand-coins", t="Crédit",
      d="Financement de projets, fonds de roulement, crédits agricoles et soutien aux activités génératrices de revenus. Des crédits adaptés, à faible coût."),
 dict(id="credit-agricole", ico="sprout", t="Crédit agricole",
      d="Votre projet agricole mérite un coup de pouce !", q="La référence en milieu rural et défavorisé."),
 dict(id="pret-scolaire", ico="graduation-cap", t="Prêt scolaire",
      d="Le prêt scolaire : la clé d'une rentrée réussie."),
 dict(id="epargne-ecole", ico="piggy-bank", t="Épargne pour l'école des enfants",
      d="Une épargne pour préparer l'école des enfants."),
 dict(id="transfert", ico="send", t="Transfert d'argent rapide",
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


def _asset_version():
    import hashlib
    h = hashlib.md5()
    for rel in ("css/style.css", "js/main.js"):
        with open(os.path.join(OUT, rel), "rb") as fh:
            h.update(fh.read())
    return h.hexdigest()[:8]


ASSET_V = _asset_version()


def e(s):
    return html.escape(s, quote=True)


def head(title, desc, page, og_img="assets/img/femme-sourire.jpg", ld=False, active=None):
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
    items = "".join(f'<a href="{h}"{" class=on aria-current=page" if h == (active or page) else ""}>{l}</a>' for h, l in HEAD_NAV)
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0b2545">
<link rel="icon" href="assets/favicon-v2.png" type="image/png">
<link rel="canonical" href="https://rcmec-ci.com/{'' if page == 'index.html' else page}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@400;500;600;700&family=Source+Serif+4:opsz,wght@8..60,500;8..60,600;8..60,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css?v={ASSET_V}">
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
      <div class="logo-foot"><img src="assets/logo-blanc.png" alt="RCMEC-CI, Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire" width="260" height="102"></div>
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
  </div>
</footer>
<script src="js/lucide.min.js"></script>
<script src="js/main.js?v={ASSET_V}"></script>
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
            items += f'<div class="cs" data-region="{e(r)}" data-q="{e((n + " " + v + " " + r).lower())}"><strong>Caisse {"d'" if n[0] in "AEIOUÉÈÂÊÎÔ" else "de "}{e(n)}</strong><span>({e(v)})</span><em>{e(r)}</em></div>\n'
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
        tiles += f'''<a class="tile" href="{surl(s["id"])}">
  <img src="assets/img/{img}" alt="" loading="lazy">
  <span class="tile__body"><h3>{s["t"]}</h3><p>{e(s["d"])}</p><span class="tile__more">En savoir plus<i data-lucide="arrow-right"></i></span></span>
</a>
'''
    regions = "".join(f"<li>{e(r)}</li>" for r in CAISSES)
    pics = "".join(f'''<a class="pic-card" href="{surl(sid)}"><img src="assets/ico/{f}" alt="" loading="lazy"><h3>{t}</h3><p>{e(p)}</p><span class="more">En savoir plus<i data-lucide="arrow-right"></i></span></a>
''' for sid, f, t, p in PICS)
    return head("RCMEC-CI | " + FULL, f"RCMEC-CI, réseau de microfinance (SFD agréé) créée en 1995. 18 caisses dans plus de 10 régions de Côte d'Ivoire. {SLOGAN}.",
                "index.html", ld=True) + f'''
<section class="hero2" style="--img:url(../assets/img/agricultrice.jpg)">
  <div class="wrap hero2__in"><div class="hero2__card">
    <span class="kicker">{FULL}</span>
    <h1>{SLOGAN}</h1>
    <p class="lead">Réseau de microfinance, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire. Au service des populations depuis 1995.</p>
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
    <div class="statement"><span class="kicker">Notre mission</span><p>Recevoir et gérer l'épargne de nos membres, accorder des crédits adaptés et peu coûteux à ceux qui en ont besoin, et protéger les populations contre les prêts à taux abusifs.</p></div>
    <div class="statement"><span class="kicker">Notre objectif</span><p>Aider les caisses du réseau à offrir des services financiers de qualité, accessibles à tous, en particulier aux habitants des campagnes, des petites villes et des villes, et à ceux qui travaillent à leur compte.</p></div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="tiles">{tiles}</div>
  </div>
</section>

<section class="banner3" role="img" aria-label="Enfants en uniforme à l'école" style="--img:url(../assets/img/h-ecole-banner.jpg)">
  <div class="wrap banner3__in">
    <div class="banner3__txt">
      <span class="kicker kicker--l">Prêt scolaire · Épargne pour l'école des enfants</span>
      <h2>La clé d'une rentrée réussie</h2>
      <p>Le prêt scolaire et l'épargne pour l'école des enfants vous aident à préparer la rentrée.</p>
      <div class="btns"><a class="btn btn--light" href="service-pret-scolaire.html">Le prêt scolaire</a><a class="btn btn--ghost" href="service-epargne-ecole.html">L'épargne pour l'école</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <div class="split__img split__img--sq split__img--face"><img src="assets/img/vendeur-banane.jpg" width="933" height="1400" alt="Commerçante souriante sur un marché" loading="lazy"></div>
    <div class="split__txt">
      <p>Nous offrons des services financiers durables aux populations qui n'ont pas accès aux produits des banques classiques. Depuis 1995, nous accompagnons ces personnes en situation fragile dans la réalisation de leurs projets et le développement de leur environnement.</p>
      <p>Nous nous adressons aux personnes en situation fragile ou exclues des banques classiques, aux opérateurs du petits métiers et commerces non déclarés, aux agriculteurs, aux commerçants, aux artisans, aux entrepreneurs et aux PME.</p>
      <ul class="force">
        <li><i data-lucide="landmark"></i><span><b>18 caisses actives</b>présentes dans plus de 10 régions de la Côte d'Ivoire</span></li>
        <li><i data-lucide="users"></i><span><b>Un personnel qualifié</b>à votre service dans chacune de nos agences, pour répondre à vos besoins</span></li>
        <li><i data-lucide="sprout"></i><span><b>Une implantation en priorité rurale</b>au service des populations qui n'ont pas accès aux banques classiques</span></li>
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

<section class="plc">
  <img class="plc__img" src="assets/img/placement.jpg" width="2000" height="668" loading="lazy" alt="Horloge et piles de pièces d'or devant un graphique en hausse">
  <div class="wrap plc__wrap"><div class="plc__txt">
    <span class="kicker kicker--l">Dépôts à terme</span>
    <h2>Parce que vos projets méritent un partenaire solide !</h2>
    <p>Placement d'une somme bloquée sur une durée définie avec un taux d'intérêt avantageux.</p>
    <a class="btn" href="service-depot-a-terme.html">Découvrir les dépôts à terme</a>
  </div></div>
</section>
''' + partners_section() + footer()


# --------------------------------------------------------------- A PROPOS
SOURCE_TRESOR = "Source : Direction Générale du Trésor et de la Comptabilité Publique, liste des Systèmes Financiers Décentralisés agréés au 19 août 2024 ; site officiel du RCMEC-CI."


def page_apropos():
    vals = [("handshake", "Solidarité"), ("home", "Proximité"), ("landmark", "Inclusion financière"), ("trending-up", "Autonomisation économique"), ("shield-check", "Confiance")]
    vh = "".join(f'<li><i data-lucide="{i}"></i><span>{t}</span></li>' for i, t in vals)
    cible = ["Personnes en situation fragile ou exclues des banques classiques", "Commerçants et artisans du petits métiers et commerces non déclarés", "Agriculteurs", "Commerçants", "Artisans", "Entrepreneurs et PME"]
    ch = "".join(f"<li>{e(c)}</li>" for c in cible)
    regions = "".join(f"<li>{e(r)}</li>" for r in CAISSES)
    facts = [("Dénomination", "Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire (RCMEC-CI)"),
             ("Statut", "Réseau de microfinance, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire"),
             ("Catégorie", "Institution mutualiste d'épargne et de crédit, réseau qui regroupe les unions mutualistes"),
             ("Au service des populations", "Depuis 1995"),
             ("Autorisation d'exercer", "Arrêté n° 151 du 8 juin 1999 (immatriculation A-U-1.4.1/98-13)"),
             ("Réseau", "18 caisses de base, dans plus de 10 régions de la Côte d'Ivoire"),
             ("Implantation", "Surtout dans les campagnes, mais aussi dans les petites villes et les villes"),
             ("Siège, Direction Générale", "Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3e étage, Abidjan")]
    fh = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in facts)
    return head("À propos | RCMEC-CI", "Le RCMEC-CI est une réseau de microfinance, SFD agréé en Côte d'Ivoire, au service des populations depuis 1995. Mission, valeurs, cible et cadre officiel.", "a-propos.html") + \
        pagehead("À propos de nous") + f'''
<section class="section">
  <div class="wrap split">
    <div class="split__txt">
      <span class="kicker">Qui sommes-nous</span>
      <h2>Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire</h2>
      <p>Le RCMEC-CI est un réseau de microfinance qui compte à ce jour dix-huit caisses, situées en priorité dans les campagnes. Nous offrons des services financiers durables aux populations qui n'ont pas accès aux produits des banques classiques.</p>
      <p>Depuis 1995, nous accompagnons ces personnes en situation fragile dans la réalisation de leurs projets et le développement de leur environnement.</p>
    </div>
    <div class="split__img split__img--wide"><img src="assets/img/conseiller-rcmec.jpg" width="1536" height="1024" alt="Conseiller RCMEC-CI au bureau, avec en arrière-plan un marché et un village de Côte d'Ivoire" loading="lazy"></div>
  </div>
</section>

<section class="triband" aria-label="Nos engagements">
  <div class="wrap triband__in">
    <div><b>Épargne</b></div><div><b>Sécurité</b></div><div><b>Fiabilité</b></div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {head2("Fiche d'identité", "Le RCMEC-CI en bref")}
    <dl class="idcard">{fh}</dl>
    <p class="srcnote">{SOURCE_TRESOR}</p>
  </div>
</section>

<section class="section">
  <div class="wrap duo">
    <div class="statement"><span class="kicker">Notre mission</span><p>Recevoir et gérer l'épargne de nos membres, accorder des crédits adaptés et peu coûteux à ceux qui en ont besoin, et protéger les populations contre les prêts à taux abusifs.</p></div>
    <div class="statement"><span class="kicker">Notre objectif</span><p>Aider les caisses du réseau à offrir des services financiers de qualité, accessibles à tous, en particulier aux habitants des campagnes, des petites villes et des villes, et à ceux qui travaillent à leur compte.</p></div>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {head2("Nos valeurs", "Ce qui nous guide")}
    <ul class="values">{vh}</ul>
  </div>
</section>

<section class="section">
  <div class="wrap split split--rev">
    <div class="split__img split__img--sq"><img src="assets/img/artisane.jpg" width="1350" height="1400" alt="Commerçante souriante derrière son étal" loading="lazy"></div>
    <div class="split__txt">
      <span class="kicker">À qui nous nous adressons</span>
      <h2>Notre cible</h2>
      <ul class="checks checks--one">{ch}</ul>
    </div>
  </div>
</section>

<section class="regions">
  <div class="wrap regions__in">
    <div>
      <span class="kicker kicker--l">Notre réseau</span>
      <h2>18 caisses de base, présentes dans plus de 10 régions de la Côte d'Ivoire</h2>
      <p class="regions__lead">Les caisses présentes sur ce site se trouvent dans les régions suivantes :</p>
      <ul class="regions__list">{regions}</ul>
    </div>
    <a class="btn btn--light" href="caisses.html">Voir nos caisses</a>
  </div>
</section>
''' + cta() + footer()


# -------------------------------------------------------------- SERVICES
# Règle : ce qui est propre à RCMEC-CI vient uniquement de leurs sources (fiche, affiches, site officiel).
# Les rubriques « En général » ne sont que des définitions courantes du produit, sans aucune condition, taux ou durée.
NOTE_CONDITIONS = "Les conditions précises (montants, durées, taux, pièces à fournir) sont communiquées par votre caisse. Contactez-nous pour les connaître."

SVC = {
 "epargne": dict(img="comptabilite.jpg", pos="50% 40%", alt="Femme comptant des billets à son bureau",
   lead="Un compte d'épargne sécurisé pour mettre votre argent à l'abri et construire votre avenir.",
   rcmec=["Des comptes d'épargne sécurisés, pour les particuliers, les groupements et les professionnels.",
          "Une mission du réseau : recevoir et gérer l'épargne de ses membres.",
          "Un réseau de 18 caisses de base, dans plus de 10 régions de la Côte d'Ivoire."],
   general=["L'épargne consiste à mettre de côté une partie de ses revenus plutôt que de la dépenser. Déposée dans une institution financière agréée, elle est plus en sécurité que de l'argent conservé chez soi.",
            "Épargner régulièrement permet de faire face aux imprévus, de préparer un projet ou de se constituer un capital."],
   pour=["Les particuliers", "Les groupements", "Les professionnels"],
   quote="Construisez votre avenir en toute sécurité."),
 "parts-sociales": dict(img="reunion-equipe.jpg", pos="50% 45%", alt="Réunion de travail autour d'une table",
   lead="Devenez membre de votre caisse en achetant une part de son capital.",
   rcmec=["Une participation au capital mutualiste, qui permet de devenir membre.", "Des parts sociales rémunérées : vous pouvez recevoir une part des bénéfices."],
   general=["Dans une mutuelle d'épargne et de crédit, les membres sont aussi ceux qui la possèdent. En souscrivant des parts sociales, chaque membre apporte une part du capital de la caisse.",
            "Le capital ainsi constitué sert de base solide à l'activité de la caisse, notamment pour accorder des crédits à ses membres."],
   pour=["Toute personne qui souhaite devenir membre de sa caisse"],
   quote=None),
 "depot-a-terme": dict(img="placement.jpg", pos="70% 50%", alt="Horloge et piles de pièces d'or devant un graphique en hausse",
   lead="Placez une somme sur une durée définie, avec un taux d'intérêt avantageux.",
   rcmec=["Le placement d'une somme, bloquée pendant une durée définie.", "Un taux d'intérêt avantageux."],
   general=["Un dépôt à terme est un placement : vous confiez une somme à l'institution pour une durée convenue à l'avance, pendant laquelle elle reste bloquée.",
            "En contrepartie, l'institution vous verse un intérêt. Ce type de placement convient à une somme dont vous n'avez pas besoin avant l'échéance."],
   pour=["Toute personne ou structure qui dispose d'une somme à placer"],
   quote=None),
 "credit": dict(img="vendeur-banane.jpg", pos="50% 40%", alt="Commerçante souriante sur son étal",
   lead="Des crédits adaptés à vos activités, à faible coût, pour financer vos projets.",
   rcmec=["Financement de projets.", "Fonds de roulement.", "Crédits agricoles.", "Soutien aux activités génératrices de revenus.",
          "Des crédits adaptés, à faible coût.", "Une protection contre les prêts à taux abusifs."],
   general=["Un crédit est une somme mise à votre disposition, que vous remboursez progressivement avec des intérêts. Un fonds de roulement finance les dépenses courantes d'une activité (achat de marchandises, par exemple).",
            "Un crédit bien adapté à votre activité vous évite de recourir à des prêts informels à des conditions défavorables."],
   pour=["Les commerçants", "Les artisans", "Les agriculteurs", "Les entrepreneurs et PME", "Les opérateurs du petits métiers et commerces non déclarés"],
   quote="Financez vos projets agricoles, commerciaux & personnels."),
 "credit-agricole": dict(img="cabosse-cacao.jpg", pos="50% 50%", alt="Cabosse de cacao posée sur des fèves de cacao",
   lead="Votre projet agricole mérite un coup de pouce.",
   rcmec=["Un financement pour les projets agricoles.", "Des caisses situées en priorité dans les campagnes."],
   general=["Un crédit agricole finance l'activité d'une exploitation : préparation des terres, achat de semences et de matériel, par exemple.",
            "L'activité agricole suit le rythme des saisons : le crédit se définit donc avec la caisse, en fonction de votre projet."],
   pour=["Les agriculteurs", "Les populations du monde rural"],
   quote="La référence en milieu rural et défavorisé."),
 "pret-scolaire": dict(img="ecole-uniformes.jpg", pos="50% 40%", alt="Enfants en uniforme assis à leurs bancs d'école",
   lead="Un prêt pour préparer la rentrée scolaire de vos enfants.",
   rcmec=["Un prêt pensé pour la scolarité des enfants."],
   general=["Un prêt scolaire est un crédit destiné aux dépenses liées à la scolarité des enfants. Il permet d'étaler ces dépenses plutôt que de les payer en une fois."],
   pour=["Les parents d'élèves"],
   quote="La clé d'une rentrée réussie."),
 "epargne-ecole": dict(img="classe.jpg", pos="50% 35%", alt="Enfants souriants dans une salle de classe",
   lead="Mettez de côté dès aujourd'hui pour l'école de vos enfants.",
   rcmec=["Un produit consacré à l'épargne pour l'école des enfants."],
   general=["Une épargne scolaire consiste à mettre régulièrement de l'argent de côté pour les dépenses d'école des enfants.",
            "Elle permet d'aborder la rentrée avec une réserve, plutôt que de tout payer en une seule fois."],
   pour=["Les parents qui souhaitent préparer la scolarité de leurs enfants"],
   quote=None),
 "transfert": dict(img="telephone-homme.jpg", pos="60% 40%", alt="Homme souriant consultant son téléphone",
   lead="Envoyez et recevez de l'argent facilement, en toute sécurité.",
   rcmec=["Envoi et réception de fonds sécurisés.", "Un service disponible sur l'ensemble du territoire.", "Des caisses réparties dans plus de 10 régions."],
   general=["Un transfert d'argent permet de faire parvenir une somme à un proche, ou d'en recevoir une, sans avoir à se déplacer avec de l'argent liquide.",
            "Pour votre sécurité, vérifiez toujours l'identité du bénéficiaire et ne communiquez jamais vos informations personnelles à des inconnus."],
   pour=["Toute personne qui souhaite envoyer ou recevoir des fonds"],
   quote="Recevez et envoyez de l'argent facilement."),
 "micro-assurance": dict(img="famille-perron.jpg", pos="50% 45%", alt="Famille souriante assise sur le perron de sa maison",
   lead="Protégez votre famille et vos biens.",
   rcmec=["Des solutions de micro-assurance pour protéger votre famille et vos biens."],
   general=["La micro-assurance est une assurance conçue pour les personnes à revenus modestes, avec des protections simples et accessibles.",
            "Elle aide un ménage ou une petite activité à faire face à un événement imprévu sans compromettre son équilibre financier."],
   pour=["Les familles", "Les petites activités"],
   quote=None),
}


# « Pourquoi c'est important » : explications générales du rôle de chaque produit, sans condition propre à RCMEC-CI.
IMPORTANCE = {
 "epargne": ["L'épargne est votre première protection contre les imprévus : maladie, panne, mauvaise saison. Elle permet d'y faire face sans s'endetter.",
             "Placée dans une institution agréée, elle est à l'abri des risques liés à l'argent conservé chez soi (perte, vol, dépenses impulsives) et prépare vos projets à long terme."],
 "parts-sociales": ["Dans une mutuelle, ce sont les membres qui constituent le capital de la caisse. Souscrire des parts sociales, c'est donc contribuer à la solidité de l'institution qui vous sert.",
                    "C'est aussi ce qui fait la différence avec une banque classique : le membre n'est pas seulement un client, il est propriétaire d'une part de la caisse."],
 "depot-a-terme": ["Bloquer une somme pour une durée définie aide à la protéger des dépenses du quotidien et à la faire fructifier grâce aux intérêts.",
                   "C'est une façon simple de préparer une échéance : un investissement, une dépense importante, un projet familial."],
 "credit": ["Pour un commerçant, un artisan ou un entrepreneur, le crédit permet d'acheter du stock, d'équiper son atelier ou de saisir une opportunité sans attendre d'avoir économisé la somme.",
            "Un crédit encadré, auprès d'une institution agréée, protège de l'endettement informel, souvent beaucoup plus coûteux."],
 "credit-agricole": ["En agriculture, il faut dépenser avant de récolter : semences, entretien, main-d'œuvre. Un financement adapté permet de franchir ce cap.",
                     "Soutenir les projets agricoles, c'est aussi soutenir les familles et l'économie des zones rurales, où le réseau est implanté en priorité."],
 "pret-scolaire": ["L'éducation est l'un des investissements les plus importants pour une famille, et la rentrée concentre de nombreuses dépenses.",
                   "Un prêt scolaire permet d'étaler ces dépenses pour que les enfants commencent l'année dans de bonnes conditions."],
 "epargne-ecole": ["La scolarité d'un enfant représente des dépenses régulières, qui se concentrent au moment de la rentrée.",
                    "Épargner à l'avance permet de les préparer sans s'endetter."],
 "transfert": ["Pouvoir envoyer de l'argent à un proche, ou en recevoir, rapidement, est souvent essentiel : soutien à la famille, règlement d'une urgence, échanges entre régions.",
               "Passer par une institution agréée évite de transporter de l'argent liquide et sécurise l'opération."],
 "micro-assurance": ["Un accident, une maladie ou un sinistre peuvent suffire à faire basculer un ménage ou une petite activité.",
                     "La micro-assurance, par ses protections simples et accessibles, aide à absorber ces chocs sans perdre ce que l'on a construit."],
}

# « Pourquoi choisir RCMEC-CI » : uniquement des faits issus de la liste officielle des SFD agréés, du site officiel et de la fiche.
WHY = [("shield-check", "Un réseau agréé", "Système Financier Décentralisé agréé en Côte d'Ivoire par arrêté n° 151 du 8 juin 1999 (source : liste officielle des SFD agréés du Trésor)."),
       ("calendar-check", "Depuis 1995", "Nous accompagnons les personnes en situation fragile dans la réalisation de leurs projets depuis 1995."),
       ("map-pinned", "Un réseau de proximité", "18 caisses de base dans plus de 10 régions de la Côte d'Ivoire, situées en priorité dans les campagnes."),
       ("hand-coins", "Des services à faible coût", "Des services de proximité à faible coût, destinés aux populations qui n'ont pas accès aux banques classiques."),
       ("users", "Un personnel qualifié", "Dans chacune de nos agences, un personnel qualifié pour répondre à vos besoins."),
       ("lock", "Une protection contre les prêts à taux abusifs", "Notre mission : accorder des crédits à ceux qui en ont besoin et protéger les populations contre les prêts à taux abusifs.")]


HDR = {"epargne": "h-epargne.jpg", "parts-sociales": "h-parts-sociales.jpg", "depot-a-terme": "placement.jpg", "credit": "h-credit.jpg",
       "credit-agricole": "h-credit-agricole.jpg", "pret-scolaire": "h-pret-scolaire.jpg", "epargne-ecole": "h-epargne-ecole.jpg",
       "transfert": "h-transfert.jpg", "micro-assurance": "h-micro-assurance.jpg"}
HDR_ALT = {"epargne": "Femme comptant des billets à son bureau", "parts-sociales": "Réunion de travail autour d'une table", "depot-a-terme": "Horloge et piles de pièces d'or devant un graphique en hausse",
           "credit": "Commerçante souriante sur un marché", "credit-agricole": "Cabosse de cacao posée sur des fèves de cacao", "pret-scolaire": "Enfants en uniforme assis à leurs bancs d'école",
           "epargne-ecole": "Enfants souriants dans une salle de classe", "transfert": "Homme souriant consultant son téléphone", "micro-assurance": "Famille souriante assise sur le perron de sa maison"}


def herosvc(h1, lead, img, alt, crumbs, btns, pos="center"):
    return f'''<section class="shero2">
  <img class="shero2__bg" src="assets/img/{img}" alt="{e(alt)}" fetchpriority="high" style="object-position:{pos}">
  <div class="wrap shero2__in">
    <nav class="crumbs" aria-label="Fil d'Ariane">{crumbs}</nav>
    <h1>{h1}</h1>
    <p class="shero2__lead">{e(lead)}</p>
    <div class="btns">{btns}</div>
  </div>
</section>
'''


def partners_section():
    """Bandeau défilant « Nos Partenaires » : données dans data/partners.json, logos dans assets/img/partners/."""
    with open(os.path.join(OUT, "data", "partners.json"), encoding="utf-8") as fh:
        items = json.load(fh)
    def card(pt):
        logo = pt.get("logo", "")
        if logo and os.path.exists(os.path.join(OUT, "assets", "img", "partners", logo)):
            vis = f'<img src="assets/img/partners/{e(logo)}" alt="" height="44">'
        elif pt.get("icon"):
            vis = f'<span class="pt__ini pt__ini--ico" aria-hidden="true"><i data-lucide="{e(pt["icon"])}"></i></span>'
        else:
            ini = e(pt.get("initials") or pt["name"][:2].upper())
            vis = f'<span class="pt__ini{" pt__ini--long" if len(ini) > 3 else ""}" aria-hidden="true">{ini}</span>'
        return f'<li class="pt"><span class="pt__logo">{vis}</span><span class="pt__txt"><b>{e(pt["name"])}</b><small>{e(pt["role"])}</small></span></li>'
    lis = "".join(card(pt) for pt in items)
    dur = max(24, 4 * len(items))
    return f'''<section class="partners" aria-label="Nos partenaires">
  <div class="wrap partners__head"><h2>Nos Partenaires</h2></div>
  <div class="marquee" style="--dur:{dur}s">
    <div class="marquee__track">
      <ul class="marquee__list">{lis}</ul>
      <ul class="marquee__list" aria-hidden="true">{lis}</ul>
    </div>
  </div>
</section>
'''


def surl(sid):
    return f"service-{sid}.html"


def page_services():
    cards = ""
    for n, s in enumerate(SERVICES, 1):
        d = SVC[s["id"]]
        cards += f'''<a class="scard" href="{surl(s["id"])}">
  <span class="scard__img"><img src="assets/img/{d["img"]}" alt="{e(d["alt"])}" loading="lazy" style="object-position:{d["pos"]}"></span>
  <span class="scard__body"><span class="scard__n">{n:02d}</span><h2>{s["t"]}</h2><p>{e(d["lead"])}</p><span class="more">Lire le détail<i data-lucide="arrow-right"></i></span></span>
</a>
'''
    return head("Nos services | RCMEC-CI", "Épargne, parts sociales rémunérées, dépôts à terme, crédit, crédit agricole, prêt scolaire, épargne pour l'école des enfants, transfert d'argent rapide et micro-assurance.", "services.html", "assets/img/vendeur-banane.jpg") + \
        herosvc("Nos services", "Épargne, crédit, assurance et transfert d'argent : des services financiers de proximité.", "h-services.jpg", "Femmes d'une équipe réunies autour d'une tablette", '<a href="index.html">Accueil</a><span aria-hidden="true">/</span><span>Nos services</span>', '<a class="btn" href="contact.html">Nous contacter</a>') + f'''
<section class="section svcintro">
  <div class="wrap">
    <p class="lead2">Nous offrons des services financiers durables aux populations qui n'ont pas accès aux produits des banques classiques. Notre mission : recevoir et gérer l'épargne de nos membres et accorder des crédits à ceux qui en ont besoin, avec des services de proximité à faible coût.</p>
  </div>
</section>
<section class="section section--tint svclist2"><div class="wrap"><div class="scards">{cards}</div></div></section>
<section class="triband" aria-label="Nos engagements">
  <div class="wrap triband__in"><div><b>Épargne</b></div><div><b>Sécurité</b></div><div><b>Fiabilité</b></div></div>
</section>
''' + cta() + footer()


def page_service(i):
    s = SERVICES[i]; d = SVC[s["id"]]
    prev_s = SERVICES[(i - 1) % len(SERVICES)]; next_s = SERVICES[(i + 1) % len(SERVICES)]
    rc = "".join(f"<li>{e(x)}</li>" for x in d["rcmec"])
    gen = "".join(f"<p>{e(x)}</p>" for x in d["general"])
    pour = "".join(f"<li>{e(x)}</li>" for x in d["pour"])
    imp = "".join(f"<p>{e(x)}</p>" for x in IMPORTANCE[s["id"]])
    why = "".join(f'<article><span class="ico"><i data-lucide="{ic}"></i></span><h3>{e(t)}</h3><p>{e(x)}</p></article>' for ic, t, x in WHY)
    quote = f'<p class="svc2__q">« {e(d["quote"])} »</p>' if d.get("quote") else ""
    crumbs_svc = f'<a href="index.html">Accueil</a><span aria-hidden="true">/</span><a href="services.html">Nos services</a><span aria-hidden="true">/</span><span>{s["t"]}</span>'
    btns_svc = '<a class="btn" href="contact.html">Nous contacter</a><a class="btn btn--ghost" href="services.html">Tous les services</a>'
    others = "".join(
        f'<a class="scard scard--s" href="{surl(o["id"])}"><span class="scard__img"><img src="assets/img/{SVC[o["id"]]["img"]}" alt="" loading="lazy" style="object-position:{SVC[o["id"]]["pos"]}"></span><span class="scard__body"><h3>{o["t"]}</h3><span class="more">Lire le détail<i data-lucide="arrow-right"></i></span></span></a>'
        for o in SERVICES if o["id"] != s["id"])
    return head(f'{s["t"]} | RCMEC-CI', d["lead"], surl(s["id"]), f'assets/img/{d["img"]}', active="services.html") + f'''
{herosvc(s["t"], d["lead"], HDR[s["id"]], HDR_ALT[s["id"]], crumbs_svc, btns_svc)}

<section class="section">
  <div class="wrap sdetail">
    <div class="sdetail__main">
      <h2>Ce que propose RCMEC-CI</h2>
      <ul class="checks checks--one">{rc}</ul>
      {quote}
      <h2 class="sdetail__h">En général</h2>
      <div class="prose">{gen}</div>
      <h2 class="sdetail__h">Pourquoi c'est important</h2>
      <div class="prose">{imp}</div>
    </div>
    <aside class="sdetail__side">
      <div class="sbox"><h3>Pour qui ?</h3><ul class="checks checks--one">{pour}</ul></div>
      <div class="sbox sbox--navy"><h3>Conditions</h3><p>{e(NOTE_CONDITIONS)}</p><a class="btn btn--light" href="contact.html">Nous contacter</a><p class="sbox__tel"><a href="tel:{TEL_HREF}">{TEL}</a></p></div>
    </aside>
  </div>
</section>

<section class="section section--tint">
  <div class="wrap">
    {head2("Pourquoi choisir RCMEC-CI", "Ce qui caractérise le réseau")}
    <div class="why">{why}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    {head2("Nos services", "Découvrez aussi")}
    <div class="scards scards--s">{others}</div>
    <div class="pager"><a href="{surl(prev_s["id"])}"><i data-lucide="arrow-left"></i><span><small>Précédent</small>{prev_s["t"]}</span></a><a href="{surl(next_s["id"])}"><span><small>Suivant</small>{next_s["t"]}</span><i data-lucide="arrow-right"></i></a></div>
  </div>
</section>
''' + cta() + footer()


# ------------------------------------------------------------- SIMULATEUR
def page_simulateur():
    return head("Simulateur | RCMEC-CI", "Estimez en FCFA la mensualité d'un crédit ou les intérêts d'un dépôt, avec le taux communiqué par votre caisse.", "simulateur.html") + \
        pagehead("Simulateur", "Estimation en FCFA : montant, durée et taux.") + f'''
<section class="section">
  <div class="wrap sim">
    <div class="sim__intro">
      <span class="kicker">Outil d'estimation</span>
      <h2>Simulez un crédit ou un dépôt à terme</h2>
      <p>Renseignez le montant, la durée et <strong>le taux communiqué par votre caisse</strong>. Ce simulateur ne contient aucun taux officiel : il calcule simplement une estimation à partir des valeurs que vous saisissez.</p>
      <p class="note">Estimation indicative, donnée à titre d'exemple, sans engagement de la caisse.</p>
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
    groups = ""
    for r, lst in CAISSES.items():
        rows = "".join(f'<li class="cs" data-region="{e(r)}" data-q="{e((n + " " + v + " " + r).lower())}"><span class="cs__n"><i data-lucide="landmark"></i>Caisse {"d'" if n[0] in "AEIOUÉÈÂÊÎÔ" else "de "}{e(n)}</span><span class="cs__v">{e(v)}</span></li>\n' for n, v in lst)
        groups += f'''<section class="rgroup" data-region="{e(r)}">
  <header class="rgroup__h"><h2>{e(r)}</h2><span>Région</span></header>
  <div class="rgroup__cols"><span>Caisse</span><span>Localité de rattachement</span></div>
  <ul class="rgroup__list">
{rows}  </ul>
</section>
'''
    return head("Nos caisses | RCMEC-CI", "Les caisses du RCMEC-CI en Côte d'Ivoire : Vallée du Bandama, Lagunes, Agnéby, Zanzan et Sud-Comoé. Siège à Cocody II Plateaux, Abidjan.", "caisses.html", "assets/img/artisane.jpg") + \
        pagehead("Nos caisses", "Les caisses du réseau, classées par région.") + f'''
<section class="section section--caisses">
  <div class="wrap">
    <div id="dir" class="rgroups">
{groups}    </div>
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
    <div class="ccol">
      <header class="ccol__h"><span>Nos coordonnées</span><h2>Siège, Direction Générale</h2></header>
      <ul class="clist">
        <li><i data-lucide="map-pin"></i><div><b>Adresse</b><span>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</span></div></li>
        <li><i data-lucide="phone"></i><div><b>Téléphone</b><a href="tel:{TEL_HREF}">{TEL}</a></div></li>
        <li><i data-lucide="mail"></i><div><b>E-mail</b><a href="mailto:{MAIL}">{MAIL}</a></div></li>
        <li><i data-lucide="share-2"></i><div><b>Réseaux sociaux</b><span class="soc2"><a href="{FB}" target="_blank" rel="noopener">Facebook</a><a href="{LI}" target="_blank" rel="noopener">LinkedIn</a><a href="{IG}" target="_blank" rel="noopener">Instagram</a></span></div></li>
      </ul>
      <div class="ccol__f"><a class="more" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte<i data-lucide="arrow-right"></i></a></div>
    </div>
    <form class="cform ccol" id="cform">
      <header class="ccol__h"><span>Écrivez-nous</span><h2>Envoyez-nous un message</h2></header>
      <div class="cform__body">
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
            </div>
    </form>
  </div>
</section>
''' + footer()


if __name__ == "__main__":
    write("index.html", page_index())
    write("a-propos.html", page_apropos())
    write("services.html", page_services())
    for _i, _s in enumerate(SERVICES):
        write(surl(_s["id"]), page_service(_i))
    write("simulateur.html", page_simulateur())
    write("caisses.html", page_caisses())
    write("contact.html", page_contact())
    urls = ["" if h == "index.html" else h for h, _ in NAV] + [surl(_s["id"]) for _s in SERVICES]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                "".join(f"  <url><loc>https://rcmec-ci.com/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
