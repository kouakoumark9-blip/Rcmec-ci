#!/usr/bin/env python3
"""Génère les pages HTML statiques du site RCMEC-CI. Usage : python3 build.py"""
import html, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
FB = "https://web.facebook.com/p/R%C3%A9seau-des-Caisses-Mutuelles-dEpargne-et-de-Cr%C3%A9dit-de-C%C3%B4te-dIvoire-61587044378852/"
LI = "https://www.linkedin.com/company/rcmec-ci/"
IG = "https://www.instagram.com/rcmecci/"
TEL, TEL_HREF, MAIL = "+225 27 22 50 12 85", "+2252722501285", "contact@rcmec.ci"
OSM = "https://www.openstreetmap.org/search?query=Carrefour%20Duncan%20Cocody%20Abidjan"

NAV = [("index.html", "Accueil"), ("a-propos.html", "À propos"), ("services.html", "Services"),
       ("caisses.html", "Nos caisses"), ("simulateur.html", "Simulateur"), ("conseils.html", "Conseils"),
       ("contact.html", "Contact")]

SERVICES = [
 dict(id="epargne", ico="piggy-bank", t="Épargne", img="femme-sourire.jpg",
      d="Un compte d'épargne sécurisé pour les particuliers, les groupements et les professionnels.",
      p="Votre épargne est collectée et gérée par votre caisse mutualiste, au plus près de chez vous. C'est le socle de notre mission : sécuriser l'argent de nos adhérents et le faire travailler pour la communauté.",
      l=["Dépôts et retraits en caisse", "Ouverture simple pour particuliers, groupements et professionnels", "Épargne collectée et gérée par le réseau mutualiste"]),
 dict(id="parts-sociales", ico="users", t="Parts sociales rémunérées", img="reunion-equipe.jpg",
      d="Devenez membre sociétaire en participant au capital de votre caisse.",
      p="En souscrivant des parts sociales, vous devenez co-propriétaire de la mutuelle. Vous participez à ses décisions et à son développement, et vos parts sont rémunérées.",
      l=["Participation au capital de la caisse", "Statut de membre sociétaire", "Rémunération des parts selon les décisions de la caisse"]),
 dict(id="depot-a-terme", ico="lock", t="Dépôts à terme (DAT)", img="equipe-bureau.jpg",
      d="Placez une somme bloquée sur une durée définie pour la faire fructifier.",
      p="Le dépôt à terme convient lorsque vous savez que vous n'aurez pas besoin d'une somme pendant une période donnée. Vous la placez, elle est bloquée pour la durée convenue, et elle vous rapporte un intérêt fixé à l'avance.",
      l=["Somme bloquée sur une durée choisie", "Taux d'intérêt convenu à l'avance", "Idéal pour un projet à échéance connue"]),
 dict(id="credit", ico="hand-coins", t="Crédit", img="vendeur-banane.jpg",
      d="Financement de projets, fonds de roulement et activités génératrices de revenus, à moindre coût.",
      p="Commerçants, artisans, entrepreneurs : nos crédits financent votre activité sans vous exposer à l'endettement usurier. Chaque dossier est étudié en caisse, au plus près de votre réalité.",
      l=["Fonds de roulement pour commerçants et artisans", "Équipement et projets d'entreprise", "Étude du dossier en caisse, remboursement adapté à votre activité"]),
 dict(id="credit-agricole", ico="sprout", t="Crédit agricole", img="cabosse-cacao.jpg", new=True,
      d="Votre projet agricole mérite un coup de pouce : cacao, anacarde, cultures vivrières.",
      p="Nos caisses sont implantées en priorité en zone rurale. Elles connaissent les cycles de vos cultures et vous accompagnent pour financer vos campagnes agricoles.",
      l=["Intrants, semences et petit matériel", "Échéances pensées pour vos cycles de récolte", "Accompagnement par des caisses implantées en zone rurale"]),
 dict(id="pret-scolaire", ico="graduation-cap", t="Prêt scolaire & Sécurité Étude", new=True,
      d="Préparez la rentrée sereinement et protégez chaque parcours scolaire.",
      p="Deux solutions pour les familles : le prêt scolaire, « la clé d'une rentrée réussie », et RCMEC Sécurité Étude, « l'assurance qui protège chaque parcours scolaire ».",
      l=["Prêt scolaire pour financer la rentrée", "RCMEC Sécurité Étude : assurance du parcours scolaire", "Conditions détaillées communiquées en caisse"]),
 dict(id="transfert", ico="send", t="Transfert rapide d'argent", img="artisane.jpg",
      d="Envoyez et recevez des fonds en toute sécurité sur l'ensemble du territoire.",
      p="Avec des caisses réparties dans plus de 10 régions, vous pouvez envoyer de l'argent à vos proches ou en recevoir, de manière sécurisée, sans quitter votre région.",
      l=["Envoi et réception de fonds", "Réseau de caisses dans plus de 10 régions", "Opération sécurisée en caisse"]),
 dict(id="micro-assurance", ico="umbrella", t="Micro-assurance",
      d="Des solutions d'assurance accessibles pour protéger votre famille et votre activité.",
      p="La micro-assurance protège les ménages et les petites activités contre les aléas de la vie. Elle est pensée pour les populations rurales, semi-urbaines et urbaines.",
      l=["Protection adaptée à votre situation", "Garanties liées à vos produits d'épargne et de crédit", "Détail des garanties communiqué en caisse"]),
]

CAISSES = {
 "Vallée du Bandama": [("Katiola", "Katiola"), ("Boniérédougou", "Dabakala")],
 "Lagunes": [("Macory", "Abidjan"), ("Koumassi", "Abidjan"), ("Yopougon Millionnaire", "Abidjan"), ("Bingerville", "Abidjan"), ("Ahouanou", "Grand-Lahou")],
 "Agnéby": [("Tiassalé", "Agboville"), ("N'Zianouan", "Agboville"), ("Bacon", "Bacon")],
 "Zanzan": [("Bondoukou", "Bondoukou"), ("Tabagne", "Bondoukou"), ("Gouméré", "Bondoukou"), ("Assuéfry", "Tanda"), ("Transua", "Tanda")],
 "Sud-Comoé": [("Aboisso", "Aboisso"), ("Affiénou", "Aboisso"), ("Koffikro", "Aboisso"), ("N'Zikro", "Aboisso")],
}

TIPS = [
 ("Épargne", "Pourquoi épargner régulièrement, même de petites sommes ?",
  "Mettre de côté un montant fixe à chaque rentrée d'argent crée un matelas de sécurité pour les imprévus et finance vos projets sans dette. L'important n'est pas la somme, c'est la régularité."),
 ("Crédit", "Bien préparer sa demande de crédit",
  "Définissez le montant réellement utile, la durée et votre capacité de remboursement mensuelle. Une mensualité raisonnable évite les difficultés. Utilisez notre simulateur pour vous faire une idée avant de rencontrer votre caisse."),
 ("Prévention", "Pourquoi éviter l'endettement usurier ?",
  "Les prêts informels à taux excessifs fragilisent les ménages et les activités. Un crédit mutualiste, encadré et transparent, protège votre entreprise et votre famille."),
 ("Placement", "Comprendre le dépôt à terme",
  "Un dépôt à terme bloque une somme pendant une durée convenue, en échange d'un intérêt fixé à l'avance. Il convient pour une somme dont vous n'avez pas besoin à court terme."),
 ("Mutualité", "Devenir sociétaire : le rôle des parts sociales",
  "En souscrivant des parts sociales, vous devenez membre de la mutuelle. Vous participez à sa vie et à ses décisions, et vos parts sont rémunérées."),
 ("Sécurité", "Sécuriser vos transferts d'argent",
  "Effectuez vos envois et retraits en caisse, vérifiez toujours le nom du bénéficiaire et ne communiquez jamais vos informations personnelles à des inconnus, par téléphone ou par message."),
]


def e(s):
    return html.escape(s, quote=True)


def head(title, desc, page, og_img="assets/img/femme-sourire.jpg", ld=False):
    ldjson = ""
    if ld:
        ldjson = '<script type="application/ld+json">' + json.dumps({
            "@context": "https://schema.org", "@type": "FinancialService",
            "name": "RCMEC-CI - Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire",
            "url": "https://rcmec-ci.com/", "logo": "assets/logo.png", "foundingDate": "1995",
            "slogan": "Avec vous au quotidien pour garantir votre épargne et assurer votre avenir",
            "telephone": TEL, "email": MAIL, "areaServed": "CI", "sameAs": [LI, IG],
            "address": {"@type": "PostalAddress",
                        "streetAddress": "Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bât. A, 3e étage",
                        "postOfficeBoxNumber": "05 BP 822", "addressLocality": "Abidjan", "addressCountry": "CI"}},
            ensure_ascii=False) + "</script>"
    return f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#1b3a6b">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
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
<div class="progress" id="progress" aria-hidden="true"></div>
<div class="topbar">
  <div class="container topbar__in">
    <ul class="topbar__info">
      <li><i data-lucide="phone"></i><a href="tel:{TEL_HREF}">{TEL}</a></li>
      <li><i data-lucide="mail"></i><a href="mailto:{MAIL}">{MAIL}</a></li>
      <li class="hide-sm"><i data-lucide="map-pin"></i>Cocody II Plateaux, Abidjan</li>
    </ul>
    <ul class="topbar__social">
      <li><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a></li>
      <li><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a></li>
      <li><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></li>
    </ul>
  </div>
</div>
<header class="nav" id="nav">
  <div class="container nav__in">
    <a class="brand" href="index.html" aria-label="RCMEC-CI, accueil"><img src="assets/logo.png" alt="RCMEC-CI" width="150" height="58"></a>
    <button class="burger" id="burger" aria-label="Ouvrir le menu" aria-expanded="false"><span></span><span></span><span></span></button>
    <nav class="menu" id="menu" aria-label="Navigation principale">
      {"".join(f'<a href="{h}"{" class=on aria-current=page" if h == page else ""}>{l}</a>' for h, l in NAV)}
      <a class="btn btn--pill menu__cta" href="contact.html">Ouvrir un compte <i data-lucide="chevron-right"></i></a>
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
    <div>
      <div class="logo-card"><img src="assets/logo.png" alt="RCMEC-CI" width="150" height="58" loading="lazy"></div>
      <p>Avec vous au quotidien pour garantir votre épargne et assurer votre avenir.</p>
      <ul class="topbar__social foot-social">
        <li><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook"><i data-lucide="facebook"></i></a></li>
        <li><a href="{LI}" target="_blank" rel="noopener" aria-label="LinkedIn"><i data-lucide="linkedin"></i></a></li>
        <li><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram"><i data-lucide="instagram"></i></a></li>
      </ul>
    </div>
    <div><h4>Liens rapides</h4><ul>{links}</ul></div>
    <div><h4>Coordonnées</h4><ul><li>Cocody II Plateaux, Carrefour Duncan<br>Immeuble SICOGI, Bât. A, 3<sup>e</sup> étage</li><li>05 BP 822 Abidjan 05</li><li>{TEL}</li><li>{MAIL}</li></ul></div>
    <div><h4>Newsletter</h4><p>Conseils financiers et actualités du réseau.</p><form class="nl" id="nl"><input type="email" placeholder="Votre e-mail" required aria-label="E-mail"><button class="btn btn--pill" type="submit">S'abonner</button></form></div>
  </div>
  <div class="container legal">
    <p>RCMEC-CI est un Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire. Les conditions de crédit, d'épargne et d'assurance sont communiquées en caisse. Les simulations présentées sur ce site sont indicatives.</p>
    <p>Photos : <a href="https://www.pexels.com" target="_blank" rel="noopener">Pexels</a> (licence libre), à remplacer par des photos du réseau. © <span id="y"></span> RCMEC-CI. Tous droits réservés.</p>
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
    <p>{e(sub)}</p>
  </div>
</section>
'''


def ctaband(title="Prêt à ouvrir un compte ?", txt="Rendez-vous dans la caisse la plus proche ou écrivez-nous : un conseiller vous accompagne."):
    return f'''<section class="ctaband">
  <div class="container ctaband__in">
    <div><h2>{e(title)}</h2><p>{e(txt)}</p></div>
    <a class="btn btn--pill btn--light" href="contact.html">Nous contacter <i data-lucide="chevron-right"></i></a>
  </div>
</section>
'''


def svc_card(s, link=True):
    badge = '<span class="badge">À la une</span>' if s.get("new") else ""
    return f'''<a class="card" href="services.html#{s["id"]}">{badge}
  <span class="card__head"><i data-lucide="{s["ico"]}"></i><h3>{s["t"]}</h3></span>
  <p>{e(s["d"])}</p><span class="plus"><i data-lucide="arrow-right"></i></span></a>'''


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("écrit", name)


# ---------------------------------------------------------------- ACCUEIL
def page_index():
    slides = [
        ("femme-sourire.jpg", "50% 25%", "Microfinance de proximité depuis 1995", "Votre épargne en sécurité, vos projets en marche", "Avec vous au quotidien pour garantir votre épargne et assurer votre avenir.", "contact.html", "Ouvrir un compte", True),
        ("cabosse-cacao.jpg", "60% 50%", "Agriculture & ruralité", "Votre projet agricole mérite un coup de pouce", "Cacao, anacarde, cultures vivrières : des crédits adaptés aux cycles de vos exploitations.", "simulateur.html", "Simuler mon crédit", False),
        ("artisane.jpg", "50% 30%", "Commerçants, artisans, PME", "Un financement accessible, sans endettement usurier", "Fonds de roulement, équipement, activités génératrices de revenus : nous vous accompagnons.", "services.html#credit", "Voir nos crédits", False),
    ]
    sl = ""
    for i, (img, pos, chip, h, lead, href, cta, first) in enumerate(slides):
        tag = "h1" if first else "h2 class=h1"
        close = "h1" if first else "h2"
        sl += f'''    <article class="slide{' is-active' if first else ''}" style="--img:url(../assets/img/{img});--pos:{pos}">
      <div class="container slide__in"><p class="chip-label">{e(chip)}</p><{tag}>{e(h)}</{close}><p class="lead">{e(lead)}</p>
      <a class="btn btn--pill" href="{href}">{cta} <i data-lucide="chevron-right"></i></a></div>
    </article>
'''
    prev = [s for s in SERVICES if s["id"] in ("epargne", "credit", "credit-agricole", "transfert")]
    tips = "".join(f'<article><span class="tag">{t}</span><h3>{e(h)}</h3><p>{e(p[:130].rsplit(" ",1)[0])}…</p><a class="more more--text" href="conseils.html">Lire la suite<i data-lucide="chevron-right"></i></a></article>' for t, h, p in TIPS[:3])
    return head("RCMEC-CI | Microfinance de proximité en Côte d'Ivoire",
                "RCMEC-CI, faîtière de microfinance (SFD) créée en 1995 : épargne, crédit, dépôts à terme, transfert d'argent et micro-assurance partout en Côte d'Ivoire.",
                "index.html", ld=True) + f'''
<section class="hero">
  <div class="slides" id="slides">
{sl}    <button class="arrow arrow--l" id="prev" aria-label="Précédent"><i data-lucide="chevron-left"></i></button>
    <button class="arrow arrow--r" id="next" aria-label="Suivant"><i data-lucide="chevron-right"></i></button>
    <div class="dots" id="dots" role="tablist" aria-label="Diapositives"></div>
  </div>
</section>

<section class="pillars">
  <div class="container pillars__grid">
    <article class="pcard"><i data-lucide="shield-check" class="pcard__ico"></i><span class="sub">Épargne sécurisée</span><h3>Sécurité de l'épargne</h3><p>Des dépôts collectés et gérés par un réseau mutualiste, au plus près de vous.</p><a class="more" href="services.html#epargne">Lire la suite<i data-lucide="chevron-right"></i></a></article>
    <article class="pcard"><i data-lucide="hand-coins" class="pcard__ico"></i><span class="sub">Moindre coût</span><h3>Crédits accessibles</h3><p>Des financements adaptés à vos activités, sans intermédiaire usurier.</p><a class="more" href="simulateur.html">Simuler<i data-lucide="chevron-right"></i></a></article>
    <article class="pcard"><i data-lucide="map-pinned" class="pcard__ico"></i><span class="sub">Partout en Côte d'Ivoire</span><h3>Réseau de proximité</h3><p>18 caisses de base dans plus de 10 régions, en zone rurale, semi-urbaine et urbaine.</p><a class="more" href="caisses.html">Nos caisses<i data-lucide="chevron-right"></i></a></article>
  </div>
</section>

<section class="section">
  <div class="container about">
    <div class="collage">
      <img class="c1" src="assets/img/reunion-equipe.jpg" alt="Réunion d'équipe dans un bureau" loading="lazy">
      <img class="c2" src="assets/img/vendeur-banane.jpg" alt="Commerçant sur un marché" loading="lazy">
      <img class="c3" src="assets/img/equipe-bureau.jpg" alt="Équipe au travail" loading="lazy">
    </div>
    <div class="about__text">
      <span class="pill-label">À propos de nous</span>
      <h2>Libérez le potentiel de <span class="acc">votre activité</span></h2>
      <p>Le RCMEC-CI est une faîtière de microfinance, Système Financier Décentralisé (SFD) agréé. Depuis 1995, nous offrons des services financiers durables aux populations qui n'ont pas accès aux produits des banques classiques.</p>
      <p>Notre mission : collecter et gérer l'épargne de nos adhérents, accorder des crédits à ceux qui en expriment le besoin et protéger les populations contre l'endettement usurier.</p>
      <a class="btn btn--pill" href="a-propos.html">En savoir plus <i data-lucide="chevron-right"></i></a>
    </div>
  </div>
</section>

<section class="band" aria-label="Chiffres clés" style="--img:url(../assets/img/equipe-bureau.jpg)">
  <div class="container band__grid">
    <div class="bstat"><i data-lucide="calendar-check"></i><b data-count="1995" data-plain="1">0</b><span>Année de création</span></div>
    <div class="bstat"><i data-lucide="landmark"></i><b data-count="18">0</b><span>Caisses de base</span></div>
    <div class="bstat"><i data-lucide="award"></i><b data-count="years" data-prefix="+">0</b><span>Ans d'expertise</span></div>
    <div class="bstat"><i data-lucide="map-pin"></i><b data-count="10" data-prefix="+">0</b><span>Régions couvertes</span></div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <header class="sec-head"><h2><span class="acc">Nos</span> services financiers</h2><p>Épargne, crédit, assurance, transfert : des produits simples, pensés pour votre activité.</p></header>
    <div class="cards cards--4">{"".join(svc_card(s) for s in prev)}</div>
    <p class="center"><a class="btn btn--pill" href="services.html">Tous nos services <i data-lucide="chevron-right"></i></a></p>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="split__img"><img src="assets/img/femme-sourire.jpg" alt="Cliente souriante" loading="lazy"></div>
    <div>
      <span class="pill-label">Outil interactif</span>
      <h2>Simulez votre <span class="acc">crédit</span> ou votre épargne</h2>
      <p class="muted">Obtenez en quelques secondes une estimation en FCFA : mensualité, coût total, intérêts. Un bon moyen de préparer votre rendez-vous en caisse.</p>
      <a class="btn btn--pill" href="simulateur.html">Ouvrir le simulateur <i data-lucide="chevron-right"></i></a>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <header class="sec-head"><h2>Conseils <span class="acc">financiers</span></h2><p>Bien gérer son argent, pas à pas.</p></header>
    <div class="tips">{tips}</div>
    <p class="center"><a class="btn btn--pill" href="conseils.html">Tous les conseils <i data-lucide="chevron-right"></i></a></p>
  </div>
</section>
''' + ctaband() + footer()


# --------------------------------------------------------------- A PROPOS
def page_apropos():
    profiles = [("sprout", "Agriculteurs", "Financez semences, intrants et matériel, avec des échéances alignées sur vos récoltes."),
                ("store", "Commerçants", "Renforcez votre fonds de roulement et sécurisez vos recettes au quotidien."),
                ("hammer", "Artisans", "Équipez votre atelier et développez votre clientèle sans prêteurs informels."),
                ("briefcase", "Entrepreneurs & PME", "Un partenaire local pour épargner, investir et faire grandir votre entreprise.")]
    pr = "".join(f'<article><i data-lucide="{i}"></i><h3>{e(t)}</h3><p>{e(d)}</p></article>' for i, t, d in profiles)
    return head("À propos | RCMEC-CI", "Depuis 1995, le RCMEC-CI accompagne les populations exclues des banques classiques : mission, valeurs et réseau de 18 caisses de base.", "a-propos.html") + \
        pagehead("À propos de nous", "Une faîtière de microfinance ancrée dans le quotidien des Ivoiriens.", "reunion-equipe.jpg") + f'''
<section class="section">
  <div class="container about">
    <div class="collage">
      <img class="c1" src="assets/img/reunion-equipe.jpg" alt="Réunion d'équipe" loading="lazy">
      <img class="c2" src="assets/img/vendeur-banane.jpg" alt="Commerçant sur un marché" loading="lazy">
      <img class="c3" src="assets/img/equipe-bureau.jpg" alt="Équipe au travail" loading="lazy">
    </div>
    <div class="about__text">
      <span class="pill-label">Notre histoire</span>
      <h2>Plus de <span class="acc">30 ans</span> aux côtés des populations</h2>
      <p>Le Réseau des Caisses Mutuelles d'Épargne et de Crédit de Côte d'Ivoire (RCMEC-CI) est une faîtière de microfinance, Système Financier Décentralisé (SFD) agréé en Côte d'Ivoire. Il compte dix-huit caisses de base, implantées en priorité en zone rurale, mais aussi en zone semi-urbaine et urbaine.</p>
      <p>Depuis 1995, nous sommes installés auprès des populations les plus vulnérables, ce qui leur permet de profiter de services de proximité à moindre coût.</p>
    </div>
  </div>
</section>

<section class="band" aria-label="Chiffres clés" style="--img:url(../assets/img/equipe-bureau.jpg)">
  <div class="container band__grid">
    <div class="bstat"><i data-lucide="calendar-check"></i><b data-count="1995" data-plain="1">0</b><span>Année de création</span></div>
    <div class="bstat"><i data-lucide="landmark"></i><b data-count="18">0</b><span>Caisses de base</span></div>
    <div class="bstat"><i data-lucide="award"></i><b data-count="years" data-prefix="+">0</b><span>Ans d'expertise</span></div>
    <div class="bstat"><i data-lucide="map-pin"></i><b data-count="10" data-prefix="+">0</b><span>Régions couvertes</span></div>
  </div>
</section>

<section class="section">
  <div class="container">
    <header class="sec-head"><h2>Notre mission <span class="acc">&amp; nos valeurs</span></h2><p>Collecter et gérer l'épargne de nos adhérents, accorder des crédits à ceux qui en expriment le besoin, et protéger les populations contre l'endettement usurier.</p></header>
    <div class="vals">
      <article><i data-lucide="handshake"></i><h3>Solidarité</h3><p>Une mutuelle, c'est d'abord des membres qui avancent ensemble.</p></article>
      <article><i data-lucide="home"></i><h3>Proximité</h3><p>Des caisses implantées là où vivent et travaillent nos adhérents.</p></article>
      <article><i data-lucide="trending-up"></i><h3>Performance</h3><p>Un service de qualité, assuré par un personnel formé.</p></article>
    </div>
  </div>
</section>

<section class="section section--tint">
  <div class="container">
    <header class="sec-head"><h2>Notre objectif <span class="acc">principal</span></h2><p>Offrir des services financiers de qualité, accessibles à tous les opérateurs économiques, et particulièrement à ceux du monde rural, semi-urbain, urbain et du secteur informel. Le réseau apporte aux caisses l'appui nécessaire pour y parvenir.</p></header>
    <div class="profiles">{pr}</div>
  </div>
</section>
''' + ctaband("Rejoignez le réseau", "Devenez membre d'une caisse RCMEC-CI près de chez vous.") + footer()


# -------------------------------------------------------------- SERVICES
def page_services():
    cards = "".join(svc_card(s) for s in SERVICES)
    rows = ""
    for i, s in enumerate(SERVICES):
        lis = "".join(f"<li>{e(x)}</li>" for x in s["l"])
        media = f'<img src="assets/img/{s["img"]}" alt="{e(s["t"])}" loading="lazy">' if s.get("img") else f'<div class="svc__panel"><i data-lucide="{s["ico"]}"></i></div>'
        rows += f'''<article class="svc{' svc--rev' if i % 2 else ''}" id="{s["id"]}">
  <div class="svc__media">{media}</div>
  <div class="svc__body"><span class="pill-label">{e("À la une" if s.get("new") else "Service")}</span><h2>{s["t"]}</h2><p class="muted">{e(s["p"])}</p><ul class="ticks">{lis}</ul>
  <a class="btn btn--pill" href="contact.html">Contacter une caisse <i data-lucide="chevron-right"></i></a></div>
</article>
'''
    return head("Nos services | RCMEC-CI", "Épargne, parts sociales, dépôts à terme, crédit, crédit agricole, prêt scolaire, transfert d'argent et micro-assurance : découvrez les services du RCMEC-CI.", "services.html", "assets/img/vendeur-banane.jpg") + \
        pagehead("Nos services", "Des produits simples, pensés pour votre activité.", "vendeur-banane.jpg") + f'''
<section class="section section--tint">
  <div class="container"><div class="cards cards--4">{cards}</div></div>
</section>
<section class="section"><div class="container svclist">{rows}</div></section>
''' + ctaband("Un projet à financer ?", "Simulez votre crédit, puis rencontrez votre caisse.") + footer()


# ------------------------------------------------------------- SIMULATEUR
def page_simulateur():
    return head("Simulateur de crédit et d'épargne | RCMEC-CI", "Estimez en FCFA la mensualité d'un crédit ou les intérêts d'un dépôt à terme avec le simulateur du RCMEC-CI.", "simulateur.html") + \
        pagehead("Simulateur", "Estimez votre crédit ou votre épargne en FCFA.", "femme-sourire.jpg") + f'''
<section class="section">
  <div class="container sim">
    <div class="sim__intro">
      <span class="pill-label">Outil interactif</span>
      <h2>Simulez votre <span class="acc">crédit</span> ou votre épargne</h2>
      <p class="muted">Obtenez en quelques secondes une estimation en FCFA. Les taux ci-contre sont des <strong>exemples modifiables</strong> : les conditions réelles sont fixées par votre caisse lors de l'étude de votre dossier.</p>
      <p class="note"><i data-lucide="info"></i>Estimation indicative, sans valeur contractuelle.</p>
      <ol class="steps">
        <li><b>1</b><span>Choisissez le montant et la durée.</span></li>
        <li><b>2</b><span>Ajustez le taux d'exemple si besoin.</span></li>
        <li><b>3</b><span>Rendez-vous en caisse pour une offre personnalisée.</span></li>
      </ol>
    </div>
    <div class="sim__box">
      <div class="tabs" role="tablist">
        <button class="tab is-on" role="tab" data-tab="credit" aria-selected="true">Crédit</button>
        <button class="tab" role="tab" data-tab="epargne" aria-selected="false">Épargne (DAT)</button>
      </div>
      <form id="sim-credit" class="simform" data-panel="credit" onsubmit="return false">
        <label>Montant souhaité <output id="c-amount-o"></output><input id="c-amount" type="range" min="50000" max="10000000" step="50000" value="1000000"></label>
        <label>Durée <output id="c-dur-o"></output><input id="c-dur" type="range" min="3" max="48" step="1" value="12"></label>
        <label>Taux annuel d'exemple (%)<input id="c-rate" type="number" min="0" max="60" step="0.5" value="12"></label>
        <div class="result"><div><span>Mensualité estimée</span><b id="c-month">-</b></div><div><span>Coût total du crédit</span><b id="c-cost">-</b></div><div><span>Total à rembourser</span><b id="c-total">-</b></div></div>
      </form>
      <form id="sim-epargne" class="simform" data-panel="epargne" onsubmit="return false" hidden>
        <label>Somme placée <output id="e-amount-o"></output><input id="e-amount" type="range" min="50000" max="20000000" step="50000" value="1000000"></label>
        <label>Durée du placement <output id="e-dur-o"></output><input id="e-dur" type="range" min="3" max="60" step="1" value="12"></label>
        <label>Taux annuel d'exemple (%)<input id="e-rate" type="number" min="0" max="30" step="0.25" value="4"></label>
        <div class="result"><div><span>Intérêts estimés</span><b id="e-int">-</b></div><div><span>Capital au terme</span><b id="e-total">-</b></div></div>
      </form>
      <a class="btn btn--pill block" href="contact.html">Faire ma demande en caisse <i data-lucide="chevron-right"></i></a>
    </div>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CAISSES
def page_caisses():
    chips = '<button type="button" class="chip on" data-region="Toutes">Toutes</button>' + "".join(f'<button type="button" class="chip" data-region="{e(r)}">{e(r)}</button>' for r in CAISSES)
    items = ""
    for r, lst in CAISSES.items():
        for n, v in lst:
            items += f'<div class="cs" data-region="{e(r)}" data-q="{e((n + " " + v + " " + r).lower())}"><em>Région {e(r)}</em><strong>Caisse de {e(n)}</strong><small>Rattachée à {e(v)}</small></div>\n'
    total = sum(len(v) for v in CAISSES.values())
    return head("Nos caisses | RCMEC-CI", "Trouvez la caisse RCMEC-CI la plus proche : Lagunes, Zanzan, Sud-Comoé, Agnéby, Vallée du Bandama. Siège à Cocody II Plateaux, Abidjan.", "caisses.html", "assets/img/artisane.jpg") + \
        pagehead("Nos caisses", "Une caisse près de chez vous, dans plus de 10 régions.", "artisane.jpg") + f'''
<section class="section section--tint">
  <div class="container">
    <header class="sec-head"><h2>Une caisse <span class="acc">près de chez vous</span></h2><p>{total} localités listées par région. Filtrez ou recherchez la vôtre.</p></header>
    <div class="dir">
      <div class="dir__tools">
        <input id="q" type="search" placeholder="Rechercher une localité (ex. Aboisso)" aria-label="Rechercher une localité">
        <div class="chips" id="chips">{chips}</div>
      </div>
      <div class="dir__grid" id="dir">
{items}      </div>
      <p class="empty" id="empty" hidden>Aucune caisse trouvée. Contactez-nous pour être orienté.</p>
      <aside class="hq">
        <div>
          <h3><i data-lucide="building-2"></i>Direction Générale</h3>
          <p>Cocody II Plateaux, Carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bâtiment A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</p>
          <p><i data-lucide="phone"></i> {TEL}</p>
        </div>
        <a class="btn btn--pill btn--light" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte <i data-lucide="chevron-right"></i></a>
      </aside>
    </div>
  </div>
</section>
''' + footer()


# ----------------------------------------------------------------- CONSEILS
def page_conseils():
    arts = "".join(f'<article id="c{i}"><span class="tag">{t}</span><h2>{e(h)}</h2><p>{e(p)}</p></article>' for i, (t, h, p) in enumerate(TIPS, 1))
    return head("Conseils financiers | RCMEC-CI", "Épargne, crédit, dépôt à terme, parts sociales, prévention de l'endettement usurier : les conseils du RCMEC-CI pour bien gérer votre argent.", "conseils.html", "assets/img/cacao-seche.jpg") + \
        pagehead("Conseils financiers", "Bien gérer son argent, pas à pas.", "cacao-seche.jpg") + f'''
<section class="section">
  <div class="container"><div class="arts">{arts}</div></div>
</section>
''' + ctaband("Une question sur votre budget ?", "Votre conseiller en caisse vous répond.") + footer()


# ----------------------------------------------------------------- CONTACT
def page_contact():
    return head("Contact | RCMEC-CI", "Contactez le RCMEC-CI : Cocody II Plateaux, Carrefour Duncan, Abidjan. Téléphone +225 27 22 50 12 85, e-mail contact@rcmec.ci.", "contact.html", "assets/img/artisane.jpg") + \
        pagehead("Contact", "Ouvrez un compte ou posez-nous vos questions.", "artisane.jpg") + f'''
<section class="section section--tint">
  <div class="container contact">
    <div class="contact__photo">
      <img src="assets/img/artisane.jpg" alt="Commerçante souriante dans sa boutique" loading="lazy">
      <div class="badge-circle"><b>30+</b><span>ans d'expérience</span></div>
      <div class="contact__info">
        <ul>
          <li><i data-lucide="map-pin"></i><span>II Plateaux, carrefour Duncan, en face de l'ex-ADDR, Immeuble SICOGI, Bât. A, 3<sup>e</sup> étage, Abidjan<br>05 BP 822 Abidjan 05</span></li>
          <li><i data-lucide="phone"></i><a href="tel:{TEL_HREF}">{TEL}</a></li>
          <li><i data-lucide="mail"></i><a href="mailto:{MAIL}">{MAIL}</a></li>
        </ul>
      </div>
    </div>
    <form class="cform" id="cform">
      <span class="pill-label">Contactez-nous</span>
      <h2><span class="acc">Ouvrez</span> un compte !</h2>
      <p class="lead2">Écrivez-nous ou passez à la caisse la plus proche : un conseiller vous orientera.</p>
      <div class="row">
        <input name="nom" placeholder="Nom et prénom" required autocomplete="name" aria-label="Nom et prénom">
        <input name="email" type="email" placeholder="E-mail" required autocomplete="email" aria-label="E-mail">
      </div>
      <div class="row">
        <select name="objet" aria-label="Objet"><option>Ouvrir un compte</option><option>Demander un crédit</option><option>Placer mon épargne (DAT)</option><option>Transfert d'argent</option><option>Micro-assurance</option><option>Autre question</option></select>
        <input name="tel" type="tel" placeholder="Téléphone / Mobile" autocomplete="tel" aria-label="Téléphone">
      </div>
      <textarea name="msg" rows="4" placeholder="Votre message" required aria-label="Message"></textarea>
      <button class="btn btn--pill" type="submit">Envoyer le message <i data-lucide="chevron-right"></i></button>
      <p class="fine">Le bouton ouvre votre application e-mail avec le message pré-rempli, adressé à {MAIL}.</p>
    </form>
  </div>
</section>
<section class="section">
  <div class="container">
    <div class="ccards">
      <article><i data-lucide="map-pin"></i><h3>Siège</h3><p>Cocody II Plateaux, Carrefour Duncan, Immeuble SICOGI, Bât. A, 3<sup>e</sup> étage, Abidjan</p><a class="more more--text" target="_blank" rel="noopener" href="{OSM}">Voir sur la carte<i data-lucide="chevron-right"></i></a></article>
      <article><i data-lucide="phone"></i><h3>Téléphone</h3><p>{TEL}</p><a class="more more--text" href="tel:{TEL_HREF}">Appeler<i data-lucide="chevron-right"></i></a></article>
      <article><i data-lucide="landmark"></i><h3>Nos caisses</h3><p>Trouvez la caisse la plus proche de chez vous.</p><a class="more more--text" href="caisses.html">Voir les caisses<i data-lucide="chevron-right"></i></a></article>
    </div>
  </div>
</section>
''' + footer()


if __name__ == "__main__":
    write("index.html", page_index())
    write("a-propos.html", page_apropos())
    write("services.html", page_services())
    write("simulateur.html", page_simulateur())
    write("caisses.html", page_caisses())
    write("conseils.html", page_conseils())
    write("contact.html", page_contact())
    urls = ["" if h == "index.html" else h for h, _ in NAV]
    with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
                "".join(f"  <url><loc>https://rcmec-ci.com/{u}</loc></url>\n" for u in urls) + "</urlset>\n")
