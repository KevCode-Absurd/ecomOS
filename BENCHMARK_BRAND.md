# TrailFold - fictional benchmark brand

This is invented test data, not a connected business or observed customer performance.

```json
{
  "fictional": true,
  "name": "TrailFold",
  "market": "US",
  "currency": "USD",
  "platforms": [
    "Shopify",
    "Meta Ads",
    "Klaviyo"
  ],
  "positioning": "Practical lightweight bags for commuters who take short weekend trips; restrained, useful, plain-spoken voice.",
  "products": [
    {
      "sku": "DAY18",
      "name": "Daypack 18L",
      "price": 80,
      "landed_cogs": 28,
      "pick_pack": 2,
      "merchant_shipping_cost": 8,
      "payment_fee_percent": 3,
      "features": [
        "18L capacity",
        "padded 13-inch laptop sleeve",
        "water-resistant fabric, not waterproof",
        "external bottle pocket"
      ],
      "stock": 210,
      "daily_units_sold": 8,
      "confirmed_replenishment_units": 500,
      "replenishment_arrival_days": 35
    },
    {
      "sku": "POUCH",
      "name": "Cable pouch",
      "price": 20,
      "landed_cogs": 5,
      "stock": 800
    },
    {
      "sku": "BOTTLE",
      "name": "Steel bottle",
      "price": 32,
      "landed_cogs": 9,
      "stock": 600
    }
  ],
  "policies": {
    "shipping": "Free US shipping; delivery estimate 4-7 business days",
    "returns": "30-day returns for unused products; return shipping paid by customer",
    "discounts": "No current discount. Any new discount needs owner approval."
  },
  "claim_constraints": [
    "No evidence for waterproof, medical, sustainability or lifetime-durability claims.",
    "No verified competitor performance data.",
    "No clinical or controlled product test results."
  ],
  "customer_themes": {
    "simulated_review_count": 120,
    "themes": [
      "fits daily commute",
      "customers ask whether a 15-inch laptop fits",
      "customers ask whether rain protection means waterproof"
    ],
    "support_tickets_last_30_days": {
      "delivery_date_questions": 42,
      "15_inch_laptop_fit": 28,
      "waterproof_questions": 18
    },
    "note": "Themes, not verbatim licensed testimonials; no fabricated quotes or endorsements."
  },
  "website_snapshot": {
    "pdp_headline": "Adventure starts here",
    "first_image": "product on plain background",
    "pdp_details": "Laptop sizing and delivery window are below reviews; CTA says Buy now. No field speed or session-recording data."
  },
  "shopify": {
    "previous_30_days": {
      "sessions": 20000,
      "orders": 600,
      "net_product_revenue": 54000,
      "mobile_sessions": 15000,
      "mobile_orders": 400,
      "desktop_sessions": 5000,
      "desktop_orders": 200,
      "add_to_cart_sessions": 2000,
      "checkout_started_sessions": 1200
    },
    "current_30_days": {
      "sessions": 25000,
      "orders": 500,
      "net_product_revenue": 45000,
      "mobile_sessions": 20000,
      "mobile_orders": 300,
      "desktop_sessions": 5000,
      "desktop_orders": 200,
      "add_to_cart_sessions": 2000,
      "checkout_started_sessions": 1000
    },
    "definitions": "Revenue excludes tax/shipping; periods equal length. Funnel counts are session-based and internally consistent, but no controlled attribution experiment.",
    "new_customer_share_current": 0.72,
    "cohort_90_day_repeat_rate": 0.14
  },
  "meta": {
    "previous_30_days": {
      "spend": 18000,
      "reported_purchase_value": 54000,
      "cpm": 12,
      "link_ctr_percent": 1.5
    },
    "current_30_days": {
      "spend": 22000,
      "reported_purchase_value": 70400,
      "cpm": 15,
      "link_ctr_percent": 1.2
    },
    "settings": "7-day click plus 1-day view; no incremental lift study. Meta reported value not reconciled to Shopify orders.",
    "creative_history": [
      {
        "name": "Desk-to-trail demonstration",
        "spend_share": 0.55,
        "observed_result": "Largest spend recipient; mature creative. No asset-level contribution data."
      },
      {
        "name": "Laptop-fit comparison",
        "spend_share": 0.25,
        "observed_result": "Higher CTR in small test; conversion sample not supplied."
      },
      {
        "name": "Minimal product still",
        "spend_share": 0.2,
        "observed_result": "No reliable lift estimate."
      }
    ]
  },
  "klaviyo": {
    "marketable_profiles": 12000,
    "reported_attributed_revenue_current": 14000,
    "attribution_window": "5-day click plus 5-day open",
    "flows": [
      {
        "name": "welcome",
        "messages": 1,
        "offer": "none"
      },
      {
        "name": "checkout abandonment",
        "trigger": "Started Checkout",
        "messages": 1,
        "delay_hours": 24,
        "observed_gap": "No Added to Cart flow; filters not audited."
      }
    ],
    "campaigns_per_week": 3,
    "reported_open_rate_percent": 52,
    "click_rate_percent": 1.1,
    "order_rate_percent": 0.18,
    "note": "Revenue attribution overlaps other systems; no holdout or recent deliverability audit."
  },
  "resources": {
    "weekly_designer_hours": 8,
    "weekly_developer_hours": 4,
    "owner_hours": 4,
    "next_14_day_test_budget": 3000,
    "cash_constraint": "Protect replenishment payments; no additional inventory purchase approved."
  },
  "unavailable": [
    "GA4 breakdowns",
    "Clarity/Hotjar recordings",
    "field Core Web Vitals",
    "SKU-level ad acquisition cost",
    "cohort contribution LTV",
    "creative-level conversion sample sizes",
    "channel incrementality",
    "email holdout data"
  ]
}
```
