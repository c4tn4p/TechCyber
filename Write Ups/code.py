#!/usr/bin/env python3
#coding: utf-8
 
# Original idea from the CTF Western Tokyos 2020
# Adapted by erk3 for a talk/demo/challenge in my current company, and proposed to RootMe
# 2020/09/29, on a cold evening with a sleepy dog and a pregnant wife by my side
# (Or were they staying close for the fireplace? I wonder...)
 
# Import des modules
import re, html, ipaddress, socket, requests, random, string, flask, sys
from urllib.parse import urlparse

# Définition des variables
FLAG = ""+open(".passwd").readlines()[0]+""
AUTHORIZED_IPS = ['127.0.0.1', '::1', '::ffff:127.0.0.1']
AUTH_TOKEN = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(42))

# Génération de nombre aléatoire avec comme seed 'FLASK'
random.seed(FLAG)
app = flask.Flask(__name__, static_url_path='/static')
 
## Super secure checks
# Est-ce que l'IP est globale (publique) ?
# Si oui : retourner true, sinon retourner false.
def valid_ip(ip):
    try:
        result = ipaddress.ip_address(ip)
        return result.is_global # Not a LAN address
    except Exception as e:
        return False

# Prend le FQDN renseigné dans le grabber, essaie de le résoudre en IP puis utilise valid_ip pour vérifier si l'IP est valide et globale.
def valid_fqdn(fqdn):
    return valid_ip(socket.gethostbyname(fqdn))

# récupération du contenu de l'URL spécifiée dans le grabber
# Si erreur, renvoie de l'image no_idea
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
# Si la réponse contient une redirection (en-tête location), signifie qu'une redirection est demandée
# Si plus d'une redirection envoi de l'image too_far.jpg
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

# Check la validité de l'url à l'aide de valid_fqdn
# S'il se passe une exception, envoi de l'image wait_what
# Si la validation échoue, envoi de l'image wow-so-clever 
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
 
 
# Internal route, only for local administration!
# La fonction admin est appelée lorsque l'on se connecte à /admin
# Pour accéder à /admin il faut :
# Que l'IP soit dans la liste des IP autorisées, soit 127.0.0.1
# que la requête contienne rm-token en entête
# Que la valeur de cet entête soit AUTH_TOKEN
# Si ce n'est pas le cas, on voit l'image magicword_jurassic.jpg
# Si les conditions sont remplies, on peut accéder à la page admin
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
 
# Main application
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
                   <h3 class="d-flex justify-content-center">\o/</h3>
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
 
@app.errorhandler(404)
def page_not_found(e):
   return "Nope. You are lost. Nothing here but me. The forever alone 404 page that no one ever want to see."