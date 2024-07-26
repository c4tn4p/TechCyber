# HTTP - DNS Rebinding

[https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding](https://www.root-me.org/fr/Challenges/Reseau/HTTP-DNS-Rebinding)

- [HTTP - DNS Rebinding](#http---dns-rebinding)
  - [Définitions](#définitions)
    - [DNS - *Domain Name System*](#dns---domain-name-system)
    - [SOP - *Same Origin Policy*](#sop---same-origin-policy)
    - [iframe - *Inline Frame*](#iframe---inline-frame)
    - [Cross-Site Scripting - XSS](#cross-site-scripting---xss)
    - [Phishing](#phishing)
    - [DNS Rebinding](#dns-rebinding)
  - [Résolution du challenge](#résolution-du-challenge)
    - [Analyse du code](#analyse-du-code)
    - [Exploitation 🥷🏻](#exploitation-)
  - [Sources](#sources)


## Définitions

Quelques rappels sur des notions de base et quelques rappels sur d’autres types d’attaques à utiliser pour exploiter le DNS Rebinding.

### DNS - *Domain Name System*

Définition fournie par [Stéphane Bortzmeyer](https://www.bortzmeyer.org/) dans l’un de ces articles :

> D'abord, fixons la terminologie. Parler de « serveur DNS » tout court (ou, encore pire de « DNS » pour désigner un serveur, du genre « pour être sûr que la NSA ait mes données, j'utilise `8.8.8.8` en DNS ») est générateur de confusion. En effet, les deux types de serveurs DNS, résolveurs et serveurs faisant autorité sont très différents, posent des questions bien diverses, et il est rare qu'on ait besoin de parler des deux ensemble. Quand quelqu'un écrit ou dit « serveur DNS », il s'agit en général de l'un ou de l'autre type, et cela vaudrait donc la peine de le préciser. Les termes de résolveur et de serveur faisant autorité sont bien définis dans le RFC 9499 mais il est sans doute utile de rappeler ces définitions et quelques explications ici :

> **Un résolveur** (en anglais *resolver*) est un serveur DNS qui ne connaît presque rien au démarrage, mais qui va interroger, pour le compte du client final, d'autres serveurs jusqu'à avoir une réponse qu'il transmettra au client final. Dans une configuration typique, le résolveur que vous utilisez est géré par votre FAI ou bien par le service informatique de l'organisation où vous travaillez. (Il existe aussi des résolveurs publics, comme ceux de Cloudflare ou de Quad9.)

> **Un serveur** faisant autorité (en anglais authoritative server, parfois bêtement traduit par « serveur autoritaire ») connaît (« fait autorité pour ») une ou plusieurs zones DNS et il sert l'information sur ces zones aux résolveurs qui l'interrogeront. Il est typiquement géré par un hébergeur DNS ou par le bureau d'enregistrement ou directement par le titulaire du nom de domaine.

*Sources* 

- [https://www.bortzmeyer.org/separer-resolveur-autorite.html](https://www.bortzmeyer.org/separer-resolveur-autorite.html)
- [https://www.bortzmeyer.org/resolveur-dns.html](https://www.bortzmeyer.org/resolveur-dns.html)

### SOP - *Same Origin Policy*

Origin = protocole + hostname + port. L’IP adresse résolue ne rendre pas dans la SOP !

La Same Origin Policy (SOP) est un principe de sécurité fondamentale dans les navigateurs web qui restreint la manière dont les documents ou les scripts chargés d'une origine peuvent interagir avec des ressources provenant d'une autre origine. Une origine est définie par la combinaison du protocole (par exemple, HTTP ou HTTPS), du nom de domaine et du port.

La SOP a pour objectif principal de protéger les utilisateurs contre diverses attaques, notamment le Cross-Site Scripting (XSS) et le Cross-Site Request Forgery (CSRF). Elle garantit qu'un script chargé à partir d'une origine donnée ne peut pas accéder aux propriétés et aux méthodes des documents chargés à partir d'une autre origine.

Deux URL ont la même origine si elles partagent les mêmes

- Protocole : Exemple, `http://` ou `https://`
- Nom de Domaine : `Exemple`, `example.com`
- Port : Exemple, `:80` pour `HTTP` ou `:443` pour `HTTPS`

Exemples d'Origines

- `http://example.com/page1.html` et `http://example.com/page2.html` ont la même origine.
- `http://example.com` et `https://example.com` ont des origines différentes (protocole différent).
- `http://example.com` et `http://sub.example.com` ont des origines différentes (sous-domaine différent).
- `http://example.com:80` et `http://example.com:8080` ont des origines différentes (port différent).

### iframe - *Inline Frame*

Une iframe (ou "inline frame") est un élément HTML qui permet d'intégrer un autre document HTML dans la page web courante. Les iframes sont couramment utilisées pour afficher du contenu provenant d'autres sources, comme des vidéos, des publicités, ou des pages web externes, sans que l'utilisateur ait besoin de quitter la page principale.

### Cross-Site Scripting - XSS

Une faille de Cross-Site Scripting (XSS) est une vulnérabilité de sécurité courante dans les applications web. Elle permet à un attaquant d'injecter des scripts malveillants dans des pages web vues par d'autres utilisateurs. Les types de XSS les plus courants sont :

- **XSS Réfléchi** *- Reflected XSS*
    
    Le script malveillant est injecté dans une requête HTTP et est renvoyé dans la réponse sans être stocké. L'attaque se produit chaque fois que l'utilisateur visite une URL spécialement conçue.
    
- **XSS Persistant -** *Stored XSS*
    
    Le script malveillant est stocké sur le serveur et est servi à chaque utilisateur qui visite la page affectée.
    
- **XSS basé sur le DOM -** *DOM-based XSS*
    
    Le script malveillant est injecté et exécuté directement par le navigateur, manipulant le Document Object Model (DOM).
    

### Phishing

Le phishing est une technique de fraude en ligne qui vise à tromper les utilisateurs pour les amener à divulguer des informations personnelles, telles que des identifiants de connexion, des informations financières ou d'autres données sensibles ou les emmener vers du contenu malveillant. Les attaques de phishing exploitent souvent des leurres, comme des courriels, des messages, ou des sites web factices qui ressemblent à des sources fiables et légitimes, pour induire les victimes en erreur.

### DNS Rebinding

![https://cdn.cyberpunk.rs/wp-content/uploads/2018/12/dns_rebind_general_approach.jpg](https://cdn.cyberpunk.rs/wp-content/uploads/2018/12/dns_rebind_general_approach.jpg)

Une attaque *DNS Rebinding* est une méthode utilisée par des attaquants pour contourner les politiques de sécurité des navigateurs web et accéder à des réseaux internes, souvent protégés par des pare-feu.

1. L'attaquant contrôle un DNS malveillant, qui répond aux requêtes pour un certain domaine, par exemple `malicious.com`.
2. L'attaquant incite l'utilisateur à charger `malicious.com` (iframe, XSS, Phishing,..)
3. Le navigateur de la de la victime effectue une requête DNS à la recherche de l'adresse IP de `malicious.com`. Le DNS de l'attaquant répond avec l'adresse réelle de `malicious.com`, et fixe la valeur TTL à une valeur faible (1 seconde) afin que le cache ne dure pas.
4. Le site `malicious.com` contient des fichiers JS malveillants qui s'exécutent sur le navigateur de la victime. Par exemple, la page peut commencer à faire d'étranges demandes POST étranges à `malicious.com/fire_sprinkler_system` avec un JSON : {« fire_sprinkler_system_test » : 1}
5. Les demandes sont initialement envoyées à `malicious.com`, mais la faible valeur du TTL oblige le navigateur à navigateur à résoudre à nouveau le domaine (via une autre recherche DNS).
6. Cette fois-ci, le serveur DNS de l'attaquant répond par une autre IP, une adresse IP du
du réseau local, par exemple : `192.168.1.10` ou `127.0.0.1`, qui se trouve être le serveur du réseau de la victime en charge du *Fire Sprinkler System.*
7. La machine de la victime envoie une requête POST destinée à `malicious.com` et donc vers `192.168.1.10` et le Sprinkler System arrose tout le monde.

*Source* 

[https://www.cyberpunk.rs/dns-rebinding-behind-the-enemy-lines](https://www.cyberpunk.rs/dns-rebinding-behind-the-enemy-lines)

> *Pourquoi l'attaquant doit faire du rebinding avant d'envoyer les requêtes aux interfaces web auquel il souhaite accéder ? Qu'est-ce qui empêche l'attaquant d'accéder directement via un script java aux ressources via l’adresse IP, sans faire de résolution DNS ?*
> 

L'attaquant doit effectuer le rebinding DNS avant d'envoyer les requêtes à l'interface web du routeur pour contourner les restrictions de sécurité du navigateur web et accéder aux ressources internes du réseau de la victime en contournant la SOP.

Le navigateur de la victime est alors utilisé comme un proxy involontaire pour accéder aux ressources internes, car le navigateur peut naturellement accéder à toutes les adresses IP privées du réseau accessibles par la machine de la victime.

En modifiant la résolution DNS, l'attaquant utilise le navigateur de la victime pour envoyer des requêtes HTTP directement aux adresses IP internes. Puisque le navigateur de la victime est sur le réseau interne, il peut atteindre ces adresses internes sans être bloqué par les pare-feu externes.

**Les pare-feu et les dispositifs de sécurité réseau** protègent contre les accès externes ne bloqueront pas ces requêtes, car elles proviennent de l'intérieur du réseau (depuis le navigateur de la victime).

Sans DNS rebinding, l’attaque ne serait pas possible :

- **Tentative de requête directe bloquée par SOP**
    
    Un script sur `malicious-site.com` tente d'accéder directement à `http://192.168.1.1`. Le navigateur bloque cette requête car elle viole la politique de même origine.
    
- **Requête rejetée par pare-feu**
    
    Si un attaquant externe essaie d'accéder directement à `http://192.168.1.1` via un script ou une requête HTTP, le pare-feu du réseau interne bloque cette requête car elle provient d'une source non autorisée.
    

> *Est-ce que l'attaquant dois lui même posséder un serveur DNS pour mener l'attaque ?*
> 

L'attaque DNS rebinding repose sur la capacité de l'attaquant à manipuler les réponses aux requêtes DNS de manière dynamique. Pour ce faire, l'attaquant doit avoir un contrôle total sur le serveur DNS qui répond aux requêtes pour le domaine utilisé dans l'attaque.

- **Modification des enregistrements DNS**
    
    L'attaquant doit initialement configurer le serveur DNS pour répondre avec une adresse IP publique. Ensuite, il doit pouvoir modifier rapidement cette réponse pour une adresse IP interne (locale) après un certain délai.
    
- **Définition de courts TTL - *Time-To-Live***
    
    Le serveur DNS de l'attaquant peut définir des valeurs de TTL très courtes pour les enregistrements DNS. Cela force le navigateur de la victime à refaire des requêtes DNS fréquemment, permettant ainsi au serveur DNS de répondre avec des adresses IP différentes à des moments stratégiques.
    

> *Est-ce que la victime doit faire une action (cliquer) sur l'iframe pour que l'attaque se lance ?*
> 

la victime n'a généralement pas besoin d'effectuer une action spécifique comme cliquer sur l'iframe pour que l'attaque se lance.  Lorsqu’une page contenant une iframe hebergée sur `malicious.com`, le navigateur de la victime effectue une requête DNS pour `malicious.com`.

## Résolution du challenge

Énoncé

> Le devops de cette petite application web a peu de temps et peu de moyens. L’interface d’administration est ainsi, comme souvent, embarquée avec l’IHM utilisateur. Pour autant il s’est assuré qu’on ne puisse pas y accéder de l’extérieur !
> 

- Indice : *TTL=0*

Lien vers l’application web

- [http://challenge01.root-me.org:54022/](http://challenge01.root-me.org:54022/)

### Analyse du code

Le challenge nous fourni le code source de l’application : analysons le !

- Import des modules et définition des variables

```python
#!/usr/bin/env python3
#coding: utf-8

# Original idea from the CTF Western Tokyos 2020
# Adapted by erk3 for a talk/demo/challenge in my current company, and proposed to RootMe
# 2020/09/29, on a cold evening with a sleepy dog and a pregnant wife by my side
# (Or were they staying close for the fireplace? I wonder...)

import re, html, ipaddress, socket, requests, random, string, flask, sys
from urllib.parse import urlparse

FLAG = ""+open(".passwd").readlines()[0]+""
AUTHORIZED_IPS = ['127.0.0.1', '::1', '::ffff:127.0.0.1']
AUTH_TOKEN = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(42))

```

- Génération de nombre aléatoire avec comme seed 'FLASK'

```python
random.seed(FLAG)
app = flask.Flask(__name__, static_url_path='/static')

```

**Checks de sécurité**

- **Analyse de l'IP renseignée dans le grabber**
    - Est-ce qu'il s'agit d'une IP publique (globale)
        - Si oui
            - true
        - Si non
            - false

```python
### Super secure checks
def valid_ip(ip):
    try:
        result = ipaddress.ip_address(ip)
        return result.is_global # Not a LAN address
    except Exception as e:
        return False

```

- **Analyse du FQDN**
    - Prend le FQDN renseigné dans le grabber, essaie de le résoudre en IP puis utilise `valid_ip` pour vérifier si l'IP est valide et globale.

```python
def valid_fqdn(fqdn):
    return valid_ip(socket.gethostbyname(fqdn))
```

- **Récupération du contenu de l'URL spécifiée dans le grabber** *- try / catch*
    - Si erreur, renvoie de l'image `no_idea.jpg`
    - Si la réponse contient une redirection (en-tête location), signifie qu'une redirection est demandée
    - Si plus d'une redirection envoi de l'image `too_far.jpg`

```python
def get_url(url, recursion):
    try:
        r = requests.get(url, allow_redirects=False, timeout=5, headers={'rm-token': AUTH_TOKEN})
    except Exception as e:
       return '''
               <html>
                   <head>
                       <title>Oo</title>
                   </head>
                   <body>
                       <img src="%s"/>
                   </body>
               </html>
           ''' % (flask.url_for('static', filename='no_idea.jpg'),)
    if 'location' in r.headers:
        if recursion > 1:
            return '''
               <html>
                   <head>
                       <title>Too far gone</title>
                   </head>
                   <body>
                       <img src="%s"/>
                   </body>
               </html>
           ''' % (flask.url_for('static', filename='too_far.jpg'),)
        url = r.headers['location']
        check = check_url(url)
        if check is not None:
            return check
        return get_url(url, recursion + 1)
    return r.text

```

- **Check la validité de l’URL à l'aide de `valid_fqdn`**
    - S'il se passe une exception, envoi de l'image `wait_what.jpg`
    - Si la validation échoue, envoi de l'image `wow-so-clever.jpg`

```python
def check_url(url):
    try:
        #check = valid_fqdn(urlparse(url).netloc.split(':')[0])
        check = valid_fqdn(urlparse(url).hostname)
    except Exception as e:
        return '''
           <html>
               <head>
                   <title>Wait, what?</title>
               </head>
               <body>
                   <img src="%s"/>
               </body>
           </html>
       ''' % (flask.url_for('static', filename='what.jpg'),)
    if check == False:
        return '''
           <html>
               <head>
                   <title>Nope</title>
               </head>
               <body>
                   <img src="%s"/>
               </body>
           </html>
       ''' % (flask.url_for('static', filename='wow-so-clever.jpg'),)
    return None

```

**Espace Admin**

- **La fonction admin est appelée lorsque l'on se connecte à `/admin`**
    - si les conditions sont remplies, on peut accéder à la page d’admin
        - Si
            - l'IP source n’est pas dans la liste des autorisées ( `127.0.0.1` ou équivalent en IPv6)
            - la requête ne contient pas `rm-token` dans son en entête
            - ou que le contenu de `rm-token` est différent de `AUTH_TOKEN`
            - Envoyer l’image `magicword_jurassic.jpg`  (accès non autorisé)
        - Sinon
            - Afficher la page admin (et donc le flag)

```python
# Internal route, only for local administration!
@app.route('/admin')
def admin():
    if flask.request.remote_addr not in AUTHORIZED_IPS or 'rm-token' not in flask.request.headers or flask.request.headers['rm-token'] != AUTH_TOKEN:
        return '''
           <html>
               <head>
                   <title>Not the admin page</title>
                   <link rel="stylesheet" href="/static/bootstrap.min.css">
               </head>
               <body style="background:black">
                   <div class="d-flex justify-content-center">
                       <img src="%s"/>
                   </div>
               </body>
           </html>
       ''' % (flask.url_for('static', filename='magicword_jurassic.jpg'),)
    msg = '''
       <html>
           <head>
               <title>Admin page</title>
               <link rel="stylesheet" href="/static/bootstrap.min.css">
           </head>
           <body style="background:pink">
               <br/>
               <h1 class="d-flex justify-content-center">Well done!</h1>
               <h3 class="d-flex justify-content-center">Have a cookie. Admins love cookies.</h1>
               <h6 class="d-flex justify-content-center">Flag: %s</h6>
               <div class="d-flex justify-content-center">
                   <img src="%s"/>
               </div>
           </body>
       </html>
   ''' % (FLAG, flask.url_for('static', filename='cookie.png'),)
    return msg

```

**Application**

- Définition de l’application
    - modification des url pour ajouter https si l’url en entré ne le contient pas

```python
@app.route('/grab')
def grab():
    url = flask.request.args.get('url', '')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    check = check_url(url)
    if check is not None:
        return check
    res = get_url(url, 0)
    return res
```

Page html du grabber

```python
@app.route('/')
def index():
    return '''
       <!DOCTYPE html>
       <html>
           <head>
               <title>URL Grabber v42</title>
               <link rel="stylesheet" href="/static/bootstrap.min.css">
               <script src="/static/vue.min.js"></script>
           </head>
           <body style="height: 100vh;">
               <div id="app" class="container" style="height: 100%">
                   <br/>
                   <h1 class="d-flex justify-content-center">Mega super URL grabber</h1>
                   <h3 class="d-flex justify-content-center">\\o/</h3>
                   <br/>
                   <h6 class="d-flex justify-content-center">Please be aware that I'm a nice tool, I don't grab pages that forbid me to frame them!</h3>
                   <h6 class="d-flex justify-content-center"><span>Also keep out of my <a href="/admin">/admin</a> page (it's only accessible from localhost anyway...)</span></h6>
                    <br/>
                    <br/>
                    <div class="input-group input-group-lg mb-3">
                        <input name="searchie" class="form-control">
                        <div class="input-group-append">
                            <button onclick="grab()" class="btn btn-primary">graby-grabo?</button>
                        </div>
                    </div>
                <iframe name='framie' srcdoc="<html>Try me I'm famous</html>" width="100%" height="50%"></iframe>
                </div>
                <script>
                    var grab = function () {
                        fetch('/grab?url=' + this.document.getElementsByName('searchie')[0].value)
                        .then((r) => r.text())
                        .then((r) => {
                            this.document.getElementsByName('framie')[0].setAttribute('srcdoc',r);
                        })
                    };
                </script>
            </body>
        </html>
    '''
```

404 pour tout le reste

- Phrase à afficher si la requête ne remplie aucune des conditions précédents

```jsx
@app.errorhandler(404)
def page_not_found(e):
   return "Nope. You are lost. Nothing here but me. The forever alone 404 page that no one ever want to see."
```

### Exploitation 🥷🏻

L’application *URL Grabber* possède donc une page d’administration en `127.0.0.1:54022/admin` à laquelle nous devons accéder pour trouver le flag.

Il va donc falloir utiliser une attaque DNS Rebinding pour y accéder. Après l’analyse de code, on réalise rapidement que l’application n’accepte pas d’adresse IP privée et que la seule possibilité d’arriver à l’interface d’administration est d’avoir pour IP source `127.0.0.1`.

> Mais comment fait on une attaque DNS Rebinding ? Dois-je monter un serveur DNS et une application web comprenant du code malveillant ?
> 

Il existe un framework appelé singularity disponible ici :

[https://github.com/nccgroup/singularity](https://github.com/nccgroup/singularity)

Une page de démonstration est même disponible :

http://rebind.it:8080/manager.html

Ce framework agit à la fois comme un serveur DNS et comme une page web contenant différents payload. Une recherche sur l’adresse IP publique de la démo du framework nous montre qu’il agit bien comme DNS (port 53 ouvert).

[https://www.shodan.io/host/35.185.206.165](https://www.shodan.io/host/35.185.206.165)

Pour comprendre le fonctionnement de l’application, j’ai décidé d’installer moi même ce framework sur l’un de mes VPS. Je suis la documentation [**officielle fournie sur le GitHub**](https://github.com/nccgroup/singularity/wiki/Setup-and-Installation), réalise mes entrées DNS en suivant les instructions :

> *Configure appropriate DNS records to delegate the management of a test subdomain ("dynamic.your.domain.") of a domain you own ("your.domain.") to the Singularity's DNS server that we will deploy shortly:*
> 
> - ***A Name**: "rebinder", **IPv4**: "ip.ad.dr.ss".*
> - ***NS Name**: "dynamic", **Hostname**: "rebinder.your.domain.". Note that the ending dot "." in the hostname is required.*
> 
> *This sample setup informs DNS clients, including browsers, that "ip.ad.dr.ss" answers queries for any subdomains under ".dynamic.your.domain.", e.g. "foo.dynamic.your.domain.". This also permits one to access the Singularity management console using the "rebinder.your.domain" DNS name with a web browser.*
> 

Je déroule l’installation du framework.

J’ai maintenant un setup qui contient

- Un serveur DNS configuré pour avoir des TTL très courts
- Une page web contenant des payloads (utilisant le même port que l’application à pirater)
- Cette même page web permet de créer des enregistrements dynamiques ayant des TTL très cours

[http://rebinder.kittypants.rip:54022/singularity.html](http://rebinder.kittypants.rip:54022/singularity.html)

mais patatra… Il n’est pas possible de lancer l’attaque dans le grabber… Il n’est pas possible de cliquer sur les boutons depuis le grabber… fausse piste !

En faisant quelques recherches supplémentaires, je suis arrivé sur un second framework :

[https://github.com/taviso/rbndr?tab=readme-ov-file](https://github.com/taviso/rbndr?tab=readme-ov-file)

> *rbndr is a very simple, non-conforming, name server for testing software against DNS rebinding vulnerabilities. The server responds to queries by randomly selecting one of the addresses specified in the hostname and returning it as the answer with a very low ttl.*
> 

Il y a donc un setup hébergé, fonctionnel, générant des noms de domaine au TTL très court et disponible ! Yes !

Tentons donc alors de bypasser la SOP (garder la même origine) en utilisant une IP publique qui s’échangera avec [localhost](http://localhost) !

## Sources

- [https://www.digitalocean.com/community/tutorials/how-to-install-go-on-debian-10](https://www.digitalocean.com/community/tutorials/how-to-install-go-on-debian-10)
- [https://github.com/sameersbn/docker-bind/issues/65](https://github.com/sameersbn/docker-bind/issues/65)
- [https://blog.compass-security.com/2021/02/the-good-old-dns-rebinding/](https://blog.compass-security.com/2021/02/the-good-old-dns-rebinding/)
- [https://blog.bi0s.in/2021/12/05/Web/Vulpixelize-HITCONCTF2021/](https://blog.bi0s.in/2021/12/05/Web/Vulpixelize-HITCONCTF2021/)
- Contexte
[DNS Rebinding Attacks Explained](https://www.youtube.com/watch?v=n1ZszREP1HM)
