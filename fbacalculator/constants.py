from decimal import Decimal


PICK_PACK = {
    "Standard": Decimal("1.06"),
    "SML_OVER": Decimal("4.09"),
    "MED_OVER": Decimal("5.20"),
    "LRG_OVER": Decimal("8.40"),
    "SPL_OVER": Decimal("10.53"),
}

THIRTY_DAY = {
    "Standard": Decimal('0.5525'),
    "Oversize": Decimal('0.4325'),
}

DIMENSIONAL_WEIGHT_DIVISOR = Decimal('166.0')
CUBIC_FOOT_DIVISOR = Decimal('1728.0')

FEE_WEIGHT = 12.0/16.0
FEE_WEIGHT_MEDIA = 14.0/16.0

CLOSING_FEES = {
    'referral': Decimal('0.15'),
    'media': Decimal('1.35'),
    'apparel': Decimal('0.40'),
    'non-pro': Decimal('1.0'),
}
