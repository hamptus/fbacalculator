from decimal import Decimal, ROUND_UP
from numpy import median

""" Calculate FBA fees """

TWO_PLACES = Decimal("0.01")

PICK_PACK = {
    "Standard": Decimal("1.06"),
    "SML_OVER": Decimal("4.09"),
    "MED_OVER": Decimal("5.20"),
    "LRG_OVER": Decimal("8.40"),
    "SPL_OVER": Decimal("10.53"),
}


def get_30_day(standard_oversize, cubic_foot):
    if standard_oversize == "Standard":
        return Decimal('0.5525') * normalize(cubic_foot)
    return Decimal('0.4325') * normalize(cubic_foot)


def get_standard_or_oversize(length, width, height, weight):
    """ Determine if object is standard size or oversized """
    if any([(weight > 20),
            (max(length, width, height) > 18),
            (min(length, width, height) > 8),
            (median([length, width, height]) > 14)]):
        return "Oversize"
    return "Standard"


def normalize(data):
    if type(data) != Decimal:
        return Decimal(str(data))
    return data


def get_dimensional_weight(length, width, height):
    dw = (height * length * width) / Decimal('166.0')
    return Decimal(dw).quantize(TWO_PLACES)


def get_girth_and_length(length, width, height):
    gl = max(length, width, height) + \
        (median([length, width, height]) * 2) + \
        (min(length, width, height) * 2)

    return Decimal(gl).quantize(Decimal("0.1"))


def get_cubic_foot(length, width, height):
    return (length * width * height) / Decimal('1728.0')


def get_weight_handling(size_tier, outbound, price=Decimal('0'), is_media=False):
    if price >= 300:
        return Decimal('0')
    outbound = normalize(outbound).quantize(Decimal("0"), rounding=ROUND_UP)

    if size_tier == "SML_STND":
        return Decimal('0.5')

    if size_tier == "LRG_STND":

        if is_media:
            if outbound <= 1:
                return Decimal('0.85')
            if outbound <= 2:
                return Decimal('1.24')
            return Decimal('1.24') + (outbound - 2) * Decimal('0.41')

        if outbound <= 1:
            return Decimal('0.96')
        if outbound <= 2:
            return Decimal('1.95')
        return Decimal('1.95') + (outbound - 2) * Decimal('0.39')

    if size_tier == "SPL_OVER":
        if outbound <= 90:
            return Decimal("124.58")
        return Decimal('124.58') + (outbound - 90) * Decimal('0.92')

    if size_tier == "LRG_OVER":
        if outbound <= 90:
            return Decimal("63.98")
        return Decimal('63.98') + (outbound - 90) * Decimal('0.8')

    if size_tier == "MED_OVER":
        if outbound <= 2:
            return Decimal("2.73")
        return Decimal('2.73') + (outbound - 2) * Decimal('0.39')

    if outbound <= 2:
        return Decimal('2.06')
    return Decimal('2.06') + (outbound - 2) * Decimal('0.39')


def calculate_fees(length, width, height, weight, sales_price=Decimal("0"),
                   is_apparel=False, is_media=False, is_pro=True):
    """ Calculate the FBA fees for the given variables """
    # Make sure the values are decimals
    length, width = normalize(length), normalize(width)
    height, weight = normalize(height), normalize(weight)

    dimensional_weight = get_dimensional_weight(length, width, height)
    girth_length = get_girth_and_length(length, width, height)

    standard_oversize = get_standard_or_oversize(length, width, height, weight)

    cubic_foot = get_cubic_foot(length, width, height)

    if standard_oversize == "Standard":
        if is_media:
            fee_weight = 14/16
        else:
            fee_weight = 12/16

        if all(
            [
                (fee_weight >= weight),
                (max(length, width, height) <= Decimal('15')),
                (min(length, width, height) <= Decimal('0.75')),
                (median([length, width, height]) <= Decimal('12'))
            ]
        ):
            size_tier = "SML_STND"
        else:
            size_tier = "LRG_STND"
    else:
        if any(
            [
                (girth_length > 165),
                (weight > 150),
                (max(length, width, height) > 108),
             ]
        ):
            size_tier = "SPL_OVER"
        elif girth_length > 130:
            size_tier = "LRG_OVER"
        elif any(
            [
                (weight > 70),
                (max(length, width, height) > 60),
                (median([length, width, height]) > 30),
            ]
        ):
            size_tier = "MED_OVER"
        else:
            size_tier = "SML_OVER"

    if is_media:
        outbound = weight + Decimal("0.125")
    else:
        if standard_oversize == "Standard":
            if weight <= 1:
                outbound = weight + Decimal('0.25')
            else:
                outbound = max(weight, dimensional_weight) + Decimal('0.25')
        else:
            if size_tier == "SPL_OVER":
                outbound = weight + 1
            else:
                outbound = max(weight, dimensional_weight) + 1

    if is_media or standard_oversize == "Oversize":
        order_handling = 0
    else:
        order_handling = 1

    if sales_price >= 300:
        pick_pack = 0
    else:
        pick_pack = PICK_PACK.get(standard_oversize, PICK_PACK.get(size_tier))

    weight_handling = get_weight_handling(
        size_tier, outbound, sales_price, is_media).quantize(TWO_PLACES)

    thirty_day = get_30_day(standard_oversize, cubic_foot)

    costs = normalize(pick_pack) + \
        normalize(weight_handling) + \
        normalize(thirty_day) + \
        normalize(order_handling)

    # Add the referral fees if we know how much we plan to sell the product for
    if sales_price:
        referral_fee = sales_price * Decimal('0.15')
        costs += referral_fee.quantize(TWO_PLACES)

    if is_media:
        closing_fee = Decimal('1.35')
        costs += closing_fee

    if is_apparel:
        costs += Decimal('0.40')

    if not is_pro:
        costs += Decimal('1.0')
    return costs.quantize(TWO_PLACES)
