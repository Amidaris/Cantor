from flask import Flask, render_template, url_for, request, flash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ThisIsSuperSecretKey'

class Currency:

    def __init__(self, code, name, flag):
        self.code = code
        self. name = name
        self.flag = flag
    
    def __repr__(self):
        return '<Currency {}>'.format(self.code)


class CantorOffer:

    def __init__(self):
        self.currencies = []
        self.denied_codes = []
    
    def load_offer(self):
        self.currencies.append(Currency('GBP', 'Pound', 'flag_england.png' ))
        self.currencies.append(Currency('USD', 'Dollar', 'flag_usa.png' ))
        self.currencies.append(Currency('CAD', 'Canadian Dollar', 'flag_canada.png' ))
        self.currencies.append(Currency('JPY', 'Yen', 'flag_japan.png' ))
        self.currencies.append(Currency('NOK', 'Norwegian Krone', 'flag_norway.png' ))
        self.currencies.append(Currency('UNK', 'Unknown Dollar', 'flag_unknown.png' ))
        self.denied_codes.append('UNK')
    
    def get_by_code(self, code):
        for currency in self.currencies:
            if currency.code == code:
                return currency
        return Currency('unknown', 'unknown', 'flag_unknown.png')

@app.route('/')
def index():
    return 'This is index'

@app.route('/exchange', methods=['GET', 'POST'])
def exchange():

    offer = CantorOffer()
    offer.load_offer()

    if request.method == 'GET':
        return render_template('exchange.html', offer=offer)
    else:
        # flash("Debug: starting exchange in Post mode")
        currency = 'EUR'
        if "currency" in request.form:
            currency = request.form['currency']
        
        if currency in offer.denied_codes:
            flash('The currency {} cannot be accepted'.format(currency))
        elif offer.get_by_code(currency) == 'unknown':
            flash('The selected currency is unknown and cannot be accepted.')
        else:
            flash('Request to exchange {} was accepted.'.format(currency))
        
        amount = 100
        if 'amount'in request.form:
            amount = request.form['amount']

        return render_template('exchange_results.html', currency=currency, amount=amount,
                               currency_info=offer.get_by_code(currency)) 