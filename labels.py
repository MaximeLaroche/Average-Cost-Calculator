
class ACTIONS:
    buy = 'Buy'
    buyToClose = 'Buy to close'
    sell = 'Sell'
    shortSell = 'Short sell'
    split = 'split'

class NAMES:
    date = 'Date'
    action = 'Action'
    price = 'Price'
    ticker = 'Symbol'
    quantity = 'Quantity'
    currency = 'Currency'
    rate = 'Exchange rate'
    id = 'ID'
    description = 'Description'
    index = 'Index'
    avg = 'Average position price'
    tot = 'Total Amount of shares after transaction'
    transactionValue = 'Value of Transaction'
    averageValue = 'Valeur of position'
    profit = 'Profit'
    aquisitionCost = 'Aquisition Cost'
    aquisitionRate = 'Average aquisition Exchange rate'
    dispotitionValue = 'Value of Disposition'
    dispositionRate = 'Disposition Exchange Rate'


class OPTION_NAMES:
    strike = 'Strike Price'
    exp = 'Expiry Date'
    type = 'Option Type'
    codes = 'Other symbols'

def makeFrench():
    ACTIONS.buy = 'Achat'
    ACTIONS.buyToClose = 'Achat pour fermer sa position'
    ACTIONS.sell = 'Vente'
    ACTIONS.shortSell = 'Vente a découvert'
    ACTIONS.split = 'split'

    NAMES.date = 'Date'
    NAMES.action = 'Action'
    NAMES.price = 'Prix'
    NAMES.ticker = 'Symbole'
    NAMES.quantity = 'Quantité'
    NAMES.currency = 'Devise'
    NAMES.rate = 'Taux de change'
    NAMES.id = 'ID'
    NAMES.description = 'Description'
    NAMES.index = 'Index'
    NAMES.avg = 'Prix moyen de la position'
    NAMES.tot = 'Nombre total de titre après la transaction'
    NAMES.transactionValue = 'Valeur de la transaction'
    NAMES.averageValue = 'Valeur de la position'
    NAMES.profit = 'Profit'
    NAMES.aquisitionCost = "Coût d'acquisition"
    NAMES.aquisitionRate = "Taux de change moyen de l'acquisition"
    NAMES.dispotitionValue = 'Valeur de la disposition'
    NAMES.dispositionRate = 'Taux de change moyen de la disposition'

    OPTION_NAMES.strike = 'Strike Price'
    OPTION_NAMES.exp = "Date d'axpiration"
    OPTION_NAMES.type = "Type d'option"
    OPTION_NAMES.codes = "Autre symboles"