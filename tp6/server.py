"""
SVL 2016-2017 M. Nebut
TP Selenium
Application de suivi de devis, codée avec les pieds.
A refactorer.
created : 2017-02-16 10:06:32 CET
"""

import os

import bottle


########################################################################
# Application services
########################################################################

@bottle.route('/')
def index():
    return bottle.template(INDEX)


@bottle.route('/quotes')
def quotes():
    quotes = list_quotes()
    return bottle.template(QUOTES, quotes=quotes)


@bottle.route('/quote/<reference>')
def quote(reference):
    (customer, amount) = read_quote(reference)
    return bottle.template(QUOTE, customer=customer, amount=amount, reference=reference)


@bottle.route('/valid/<reference>', method='POST')
def valid(reference):
    date = bottle.request.forms.get('date')
    valid_quote(reference, date)
    bottle.redirect('/quotes')


@bottle.route('/orders')
def orders():
    orders = list_orders()
    return bottle.template(ORDERS, orders=orders)


@bottle.route('/order/<reference>')
def order(reference):
    (customer, amount, date) = read_order(reference)
    return bottle.template(ORDER, reference=reference, amount=amount, customer=customer, date=date)


########################################################################
# Application functions
########################################################################

def list_quotes():
    quotes = os.listdir('data/quotes')
    return sorted(quotes)


def read_quote(reference):
    filename = os.path.join('data/quotes', reference)
    with open(filename) as the_file:
        the_file.readline()
        id_customer = the_file.readline().rstrip()
        customer = read_customer(id_customer)
        amount = 'Montant: ' + the_file.readline()
        return (customer, amount)


def write_quote(reference, content):
    filename = os.path.join('data/quotes', reference)
    with open(filename, 'w') as the_file:
        the_file.write(content)


def valid_quote(reference, date):
    filename = os.path.join('data/quotes', reference)
    with open(filename) as the_file:
        quote = the_file.read()
        quote += 'Validé le ' + date
        write_quote(reference, quote)
    os.rename(
        os.path.join('data/quotes', reference),
        os.path.join('data/orders', reference))


def list_orders():
    orders = os.listdir('data/orders')
    return sorted(orders)


def read_order(reference):
    filename = os.path.join('data/orders', reference)
    with open(filename) as the_file:
        the_file.readline()
        id_customer = the_file.readline().rstrip()
        customer = read_customer(id_customer)
        amount = 'Montant: ' + the_file.readline()
        date = the_file.readline()
        return (customer, amount, date)

def read_customer(id_customer):
    filename = os.path.join('data/customers', id_customer)
    with open(filename) as the_file:
        return the_file.readline()
    
    
########################################################################
# Templates
########################################################################

INDEX = '''
<p>Suivi des devis</p>

<ul>
<li><a href="/quotes">Devis en attente de commandes</a></li>
<li><a href="/orders">Commandes validées</a></li>
</ul>
'''


QUOTES = '''
<p>Devis</p>
<table>
  % for quote in quotes:
  <tr>
    <td><a href="/quote/{{ quote }}">{{ quote }}</a></td>
  </tr>
  % end
</table>

<a href="/">Accueil</a>
'''

QUOTE = '''
<p>Devis {{  reference }}</p>

<p> {{ customer }}</p>

<p> {{ amount }}</p>

<form action="/valid/{{ reference }}" method="post">
  Date validation : <input name="date" type="text" />
  <input value="Valider" type="submit" />
</form>

<p>
<a href="/quotes">Liste devis</a>
</p>
'''


ORDERS = '''
<p>Commandes</p>
<table>
  % for order in orders:
  <tr>
    <td><a href="/order/{{ order }}">{{ order }}</a></td>
  </tr>
  % end
</table>

<a href="/">Accueil</a>
'''

ORDER = '''
<p>Commande {{ reference }}</p>

<p> {{ customer }} </p>

<p> {{ amount }} </p>

<p> {{ date }} </p>

<p>
<a href="/orders">Liste commandes</a>
</p>
'''

########################################################################
# Start service
########################################################################

if __name__ == '__main__':
    bottle.run(host='localhost', port=8080, debug=True)

# eof
