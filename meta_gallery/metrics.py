"""Metric helpers. None always means "unavailable", never zero."""


def num(value):
    """Parse a Meta metric (string, number or {"value": ...}) into float or None."""
    if value is None:
        return None
    if isinstance(value, dict):
        value = value.get('value')
        if value is None:
            return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ratio(numerator, denominator, scale=1.0):
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator * scale


def derive(spend, purchases, value, impressions, link_clicks):
    """Return additive totals plus derived ratios for one ad and one period.

    Purchase ROAS is total attributed purchase value divided by total spend.
    If Meta reported no purchase value, ROAS is unavailable, not zero.
    """
    return {
        'spend': spend,
        'purchases': purchases,
        'purchase_value': value,
        'impressions': impressions,
        'link_clicks': link_clicks,
        'roas': ratio(value, spend),
        'cpa': ratio(spend, purchases),
        'link_ctr': ratio(link_clicks, impressions, 100.0),
        'link_cpc': ratio(spend, link_clicks),
    }


def row_metrics(row):
    return derive(num(row.get('amount_spent')), num(row.get('omni_purchase')),
                  num(row.get('omni_purchase_values')), num(row.get('impressions')),
                  num(row.get('link_click')))


def collection_roas(ads):
    """Period ROAS for a set of ads: sum(value) / sum(spend), over ads with spend.

    Ads with unavailable purchase value contribute spend but no value, so the
    result is labelled as a lower bound when any value is unavailable.
    """
    spend = sum(a['metrics']['spend'] or 0 for a in ads)
    values = [a['metrics']['purchase_value'] for a in ads]
    value = sum(v for v in values if v is not None)
    return {'spend': spend, 'purchase_value': value, 'roas': ratio(value, spend),
            'ads_without_reported_value': sum(1 for v in values if v is None)}
