
class ACTIONS_LABELS:
    buy = 'Buy'
    buyToClose = 'Buy to close'
    sell = 'Sell'
    shortSell = 'Short sell'
    split = 'split'
    nameChange = 'Name change'

class LABELS:
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


class OPTION_LABELS:
    strike = 'Strike Price'
    exp = 'Expiry Date'
    type = 'Option Type'
    codes = 'Other symbols'

class DESCRIPTION_LABELS:
    nameChange = ' is now '
    expiration = 'EXPIRATION '

def makeFrench():
    ACTIONS_LABELS.buy = 'Achat'
    ACTIONS_LABELS.buyToClose = 'Achat pour fermer sa position'
    ACTIONS_LABELS.sell = 'Vente'
    ACTIONS_LABELS.shortSell = 'Vente a découvert'
    ACTIONS_LABELS.split = 'split'
    ACTIONS_LABELS.nameChange = 'Changement de nom'


    LABELS.date = 'Date'
    LABELS.action = 'Action'
    LABELS.price = 'Prix'
    LABELS.ticker = 'Symbole'
    LABELS.quantity = 'Quantité'
    LABELS.currency = 'Devise'
    LABELS.rate = 'Taux de change'
    LABELS.id = 'ID'
    LABELS.description = 'Description'
    LABELS.index = 'Index'
    LABELS.avg = 'Prix moyen de la position'
    LABELS.tot = 'Nombre total de titre après la transaction'
    LABELS.transactionValue = 'Valeur de la transaction'
    LABELS.averageValue = 'Valeur de la position'
    LABELS.profit = 'Profit'
    LABELS.aquisitionCost = "Coût d'acquisition"
    LABELS.aquisitionRate = "Taux de change moyen de l'acquisition"
    LABELS.dispotitionValue = 'Valeur de la disposition'
    LABELS.dispositionRate = 'Taux de change moyen de la disposition'

    OPTION_LABELS.strike = 'Strike Price'
    OPTION_LABELS.exp = "Date d'axpiration"
    OPTION_LABELS.type = "Type d'option"
    OPTION_LABELS.codes = "Autre symboles"

    DESCRIPTION_LABELS.nameChange = ' est maintenant '