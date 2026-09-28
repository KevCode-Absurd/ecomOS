# Connector census: Shopify Admin API (GraphQL)

Filled by a field-census session from Shopify's official developer documentation (shopify.dev, fetched 28 Sep 2026). Every line carries the doc url it came from. Nothing from memory.

## Access
- auth: OAuth access scopes, granted per app install. Read-only scopes used for this connector:
  - `read_orders` — Order, OrderTransaction, Fulfillment, AbandonedCheckout objects (default 60-day order window) — https://shopify.dev/docs/api/usage/access-scopes
  - `read_all_orders` — orders older than 60 days — https://shopify.dev/docs/api/usage/access-scopes
  - `read_customers` — Customer, Company, Segment objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_products` — Product, ProductVariant, Collection objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_inventory` — InventoryItem, InventoryLevel objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_assigned_fulfillment_orders` / `read_merchant_managed_fulfillment_orders` — FulfillmentOrder objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_fulfillments` — FulfillmentService objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_returns` — Return and reverse-logistics objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_shopify_payments_disputes` — ShopifyPaymentsDispute objects — https://shopify.dev/docs/api/usage/access-scopes
  - `read_shopify_payments_payouts` — ShopifyPaymentsPayout, ShopifyPaymentsBalanceTransaction — https://shopify.dev/docs/api/usage/access-scopes
  - `read_marketing_events` — MarketingEvent, MarketingActivity (feeds CustomerVisit.marketingEvent) — https://shopify.dev/docs/api/usage/access-scopes
  - Abandoned checkouts also need `read_orders`, plus the merchant user must hold the `manage_abandoned_checkouts` permission (a store-user permission, not a second OAuth scope); a POS-originated call needs the `view_abandoned_checkouts` retail permission instead — https://shopify.dev/docs/api/admin-graphql/latest/queries/abandonedCheckouts
  - `InventoryItem.unitCost` additionally needs the "View product costs" permission granted to the user once granular product permissions are enabled — https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem
- rate limits: leaky-bucket calculated query cost. Restore rate by plan: Standard 100 points/second, Advanced Shopify 200 points/second, Shopify Plus 1000 points/second, Shopify for enterprise (Commerce Components) 2000 points/second. Quota refills continuously (not a fixed window), so short bursts are fine as long as average cost stays under the restore rate. A single query cannot exceed 1,000 points regardless of plan. — https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits (overview at https://shopify.dev/docs/api/usage/limits)
- history available: orders default to a 60-day lookback window unless the app has `read_all_orders`, which lifts that limit — https://shopify.dev/docs/api/usage/access-scopes
- doc index: https://shopify.dev/docs/api/admin-graphql

## Objects and grain
| Object | Grain | Doc |
|---|---|---|
| Order | one order, with nested line items, discounts, shipping and tax lines, refunds | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| LineItem | one line item within an order | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| CustomerJourneySummary / CustomerVisit | one order's pre-purchase session history (first visit, last visit, moments) | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary, https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| Customer | one customer, lifetime order count and spend | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| ProductVariant | one SKU-level variant of a product | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| InventoryItem / InventoryLevel | one variant's stock, by location | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem, https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel |
| Fulfillment | one shipment (or partial shipment) of an order, with tracking | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| Return | one buyer return intent against an order, with return line items | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| ShopifyPaymentsDispute | one card-network dispute (inquiry or chargeback) tied to an order | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| ShopifyPaymentsPayout | one bank deposit or withdrawal from the Shopify Payments balance | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| AbandonedCheckout | one checkout started and not completed | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |

## Fields
| Field | Type | Meaning | Object | Doc |
|---|---|---|---|---|
| lineItems | LineItemConnection! | the order's line items | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| discountApplications | DiscountApplicationConnection! | discounts applied to the order, excluding order edits and refunds | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| discountCodes | [String!]! | discount codes applied to the order | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| shippingLine | ShippingLine | consolidated shipping cost, carrier and service level | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| shippingLines | ShippingLineConnection! | shipping methods applied to the order | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| taxLines | [TaxLine!]! | tax lines before returns | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| currentTaxLines | [TaxLine!]! | tax lines after returns and refunds processed | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| refunds | [Refund!]! | refunds applied to the order | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| sourceName | String | platform the order originated from (web, mobile_app, pos) | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| customerJourneySummary | CustomerJourneySummary | customer's visits and interactions before placing the order | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| totalPriceSet | MoneyBag! | original order total before returns, shop and presentment currencies | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| currentTotalPriceSet | MoneyBag! | order total after adjustments, shop and presentment currencies | Order | https://shopify.dev/docs/api/admin-graphql/latest/objects/Order |
| quantity | Int! | units ordered, including refunded and removed units | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| currentQuantity | Int! | units ordered excluding refunded and removed | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| sku | String | variant SKU number | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| variant | ProductVariant | the associated variant | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| originalUnitPriceSet | MoneyBag! | unit price at order creation, no discounts | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| discountedUnitPriceSet | MoneyBag! | approximate unit price including line-level discounts | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| discountedTotalSet | MoneyBag! | total discounted price, including refunded/removed qty | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| discountAllocations | [DiscountAllocation!]! | discounts allocated to the line item | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| totalDiscountSet | MoneyBag! | total discount amount on the line | LineItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/LineItem |
| priceSet | MoneyBag! | tax amount, shop and presentment currencies, after discounts and before returns | TaxLine | https://shopify.dev/docs/api/admin-graphql/latest/objects/TaxLine |
| rate | Float | tax rate as a decimal of the line item price | TaxLine | https://shopify.dev/docs/api/admin-graphql/latest/objects/TaxLine |
| ratePercentage | Float | tax rate as a percentage of the line item price | TaxLine | https://shopify.dev/docs/api/admin-graphql/latest/objects/TaxLine |
| title | String! | name of the tax | TaxLine | https://shopify.dev/docs/api/admin-graphql/latest/objects/TaxLine |
| channelLiable | Boolean | whether the submitting channel is liable for remitting; null is unknown | TaxLine | https://shopify.dev/docs/api/admin-graphql/latest/objects/TaxLine |
| customerOrderIndex | Int | position of this order in the customer's order history | CustomerJourneySummary | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary |
| daysToConversion | Int | days from first session to order creation | CustomerJourneySummary | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary |
| firstVisit | CustomerVisit | the customer's first session going into the shop | CustomerJourneySummary | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary |
| lastVisit | CustomerVisit | the last session before the order was made | CustomerJourneySummary | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary |
| ready | Boolean! | whether attributed sessions for the order have been created yet | CustomerJourneySummary | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary |
| occurredAt | DateTime! | date and time the session occurred | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| referralCode | String | marketing referral code from ref, source, or r URL attributes | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| referrerUrl | URL | webpage where the customer clicked the link to the store | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| source | String! | source of the visit: platform, email, direct, domain, QR, or unknown | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| sourceType | MarketingTactic | type of marketing tactic for the visit | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| landingPage | URL | first page landed on for the session | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| utmParameters | UTMParameters | UTM parameters gathered from the referrer URL | CustomerVisit | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit |
| campaign | String | name of the marketing campaign | UTMParameters | https://shopify.dev/docs/api/admin-graphql/latest/objects/UTMParameters |
| source | String | traffic source, such as Google or an email newsletter | UTMParameters | https://shopify.dev/docs/api/admin-graphql/latest/objects/UTMParameters |
| medium | String | marketing medium, such as a banner or email newsletter | UTMParameters | https://shopify.dev/docs/api/admin-graphql/latest/objects/UTMParameters |
| content | String | differentiates similar content or links in one campaign | UTMParameters | https://shopify.dev/docs/api/admin-graphql/latest/objects/UTMParameters |
| term | String | paid search terms used by the campaign | UTMParameters | https://shopify.dev/docs/api/admin-graphql/latest/objects/UTMParameters |
| numberOfOrders | UnsignedInt64! | number of orders the customer has made in their lifetime | Customer | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| amountSpent | MoneyV2! | total amount the customer has spent on orders in their lifetime | Customer | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| orders | OrderConnection! | paginated list of the customer's orders | Customer | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| emailMarketingConsent | CustomerEmailMarketingConsentState | email marketing consent state | Customer | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| smsMarketingConsent | CustomerSmsMarketingConsentState | SMS marketing consent state | Customer | https://shopify.dev/docs/api/admin-graphql/latest/objects/Customer |
| marketingState | CustomerEmailMarketingState! | current opt-in/opt-out state for email marketing | CustomerEmailMarketingConsentState | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerEmailMarketingConsentState |
| marketingOptInLevel | CustomerMarketingOptInLevel | single or double opt-in level | CustomerEmailMarketingConsentState | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerEmailMarketingConsentState |
| consentUpdatedAt | DateTime | when consent state last changed | CustomerEmailMarketingConsentState | https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerEmailMarketingConsentState |
| sku | String | case-sensitive SKU identifier | ProductVariant | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| price | Money! | price in the shop's default currency | ProductVariant | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| compareAtPrice | Money | compare-at price | ProductVariant | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| inventoryItem | InventoryItem! | the inventory item used to query inventory information, including unit cost | ProductVariant | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| inventoryQuantity | Int | total sellable quantity of the variant | ProductVariant | https://shopify.dev/docs/api/admin-graphql/latest/objects/ProductVariant |
| unitCost | MoneyV2 | unit cost of the inventory item; needs "View product costs" permission | InventoryItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem |
| tracked | Boolean! | whether inventory levels are tracked for this item | InventoryItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem |
| inventoryLevels | InventoryLevelConnection! | quantities across all stocking locations | InventoryItem | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem |
| quantities | [InventoryQuantity!]! | stock amounts by state (available, on_hand, incoming, committed) | InventoryLevel | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel |
| location | Location! | the stocking location for this level | InventoryLevel | https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel |
| status | FulfillmentStatus! | current operational state of the fulfillment | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| displayStatus | FulfillmentDisplayStatus | human-readable display status | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| trackingInfo | [FulfillmentTrackingInfo!]! | tracking company, number and URL | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| deliveredAt / inTransitAt / estimatedDeliveryAt | DateTime | shipment timeline milestones | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| events | FulfillmentEventConnection! | history of events for this fulfillment | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| fulfillmentLineItems | FulfillmentLineItemConnection! | line items included in this fulfillment | Fulfillment | https://shopify.dev/docs/api/admin-graphql/latest/objects/Fulfillment |
| status | ReturnStatus! | current state of the return | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| returnLineItems | ReturnLineItemTypeConnection! | items being returned | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| totalQuantity | Int! | total units in the return | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| refunds | RefundConnection! | refunds issued against this return | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| returnShippingFees | [ReturnShippingFee!]! | fees charged for return shipping | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| decline | ReturnDecline | detail on a declined return | Return | https://shopify.dev/docs/api/admin-graphql/latest/objects/Return |
| amount | MoneyV2! | total amount disputed by the cardholder | ShopifyPaymentsDispute | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| status | DisputeStatus! | current state of the dispute | ShopifyPaymentsDispute | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| type | DisputeType! | inquiry vs. chargeback phase | ShopifyPaymentsDispute | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| evidenceDueBy / evidenceSentOn / finalizedOn | DateTime | dispute evidence timeline | ShopifyPaymentsDispute | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| order | Order | the order containing the disputed charge | ShopifyPaymentsDispute | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsDispute |
| net | MoneyV2! | total amount and currency of the payout | ShopifyPaymentsPayout | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| status | ShopifyPaymentsPayoutStatus! | payout status | ShopifyPaymentsPayout | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| issuedAt | DateTime! | exact time the payout was issued | ShopifyPaymentsPayout | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| summary | ShopifyPaymentsPayoutSummary! | fees and gross by transaction type | ShopifyPaymentsPayout | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| transactionType | ShopifyPaymentsPayoutTransactionType! | deposit vs. withdrawal | ShopifyPaymentsPayout | https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout |
| abandonedCheckoutUrl | URL! | URL for the buyer to recover their checkout | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |
| lineItems | AbandonedCheckoutLineItemConnection! | original product selections and pricing | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |
| discountCodes | [String]! | discount codes entered by the buyer at checkout | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |
| taxLines | [TaxLine]! | tax lines on the abandoned checkout | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |
| totalPriceSet | MoneyBag! | sum of items including discounts, shipping, taxes, tips | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |
| customer | Customer | the customer, may be null for draft-order/app-created checkouts | AbandonedCheckout | https://shopify.dev/docs/api/admin-graphql/latest/objects/AbandonedCheckout |

Note: this session did not independently re-confirm the field list of `Refund`/`RefundLineItem`, `DiscountApplication`, or `ShippingLine` sub-objects against a direct fetch; their parent-level fields above (`refunds`, `discountApplications`, `shippingLine(s)`) are confirmed from the Order object page. A follow-up census can expand those sub-objects from https://shopify.dev/docs/api/admin-graphql/latest/objects/Refund, .../DiscountApplication and .../ShippingLine if line-level detail on those becomes load-bearing.

## Breakdowns and dimensions
Shopify's Admin API is not a metrics/insights endpoint with breakdown dimensions like Meta or Google Ads; it returns row-level records (orders, customers, line items) that ecomOS aggregates itself. The closest thing to a breakdown is filtering and grouping by fields already listed above: `sourceName` (channel), `location` (fulfillment/inventory location), `status` (order, return, fulfillment, dispute), and `customerJourneySummary`/`CustomerVisit.source` (acquisition channel). No allowed/not-allowed combination rules are documented, because these are not a pre-aggregated insights API. — https://shopify.dev/docs/api/admin-graphql/latest/objects/Order

## Attribution and windows
Shopify does not compute marketing attribution itself. `CustomerJourneySummary` and `CustomerVisit` record raw session history (source, referrer, UTM parameters, landing page, timestamp) for the sessions Shopify's own storefront tracked before an order; there is no configurable attribution window or model — it is a first-touch/last-touch pair (`firstVisit`, `lastVisit`) plus a full `moments` list, with `ready` indicating whether the attributed sessions have finished being attached to the order (session data can lag order creation). Any multi-touch or windowed attribution model is computed downstream (e.g. in GA4 or Meta), not by Shopify. — https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary, https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerVisit

## Limits and gotchas
- Query cost: every GraphQL query is scored a calculated point cost against the leaky-bucket rate limit above; a single query cannot exceed 1,000 points. — https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits
- Pagination: cursor-based (`edges { cursor, node }` or `nodes`, plus `pageInfo { hasNextPage, hasPreviousPage, startCursor, endCursor }`); forward with `first`/`after`, backward with `last`/`before`. — https://shopify.dev/docs/api/usage/pagination-graphql
- Bulk operations: for full historical pulls (all orders, all customers), submit a query via the `bulkOperationRunQuery` mutation instead of paginating manually. Track completion via the `bulk_operations/finish` webhook or by polling `bulkOperation(id:)`; `objectCount` gives a running total processed. On completion the response includes a `url` to download the results as JSON Lines (JSONL) — one node object per line, with nested connections flattened and linked back to their parent via an auto-generated `__parentId`. Download URLs are signed and expire after one week. — https://shopify.dev/docs/api/usage/bulk-operations/queries
- Orders default to a 60-day lookback; `read_all_orders` is required to read older orders. — https://shopify.dev/docs/api/usage/access-scopes
- `InventoryItem.unitCost` is hidden unless the querying user has the "View product costs" permission, even with `read_inventory` granted — https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryItem
- Shopify Payments objects (`ShopifyPaymentsDispute`, `ShopifyPaymentsPayout`) only return data for stores on Shopify Payments; other gateways have no data here even with the scope granted — https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout
- Abandoned checkouts need `read_orders` plus the separate `manage_abandoned_checkouts` merchant-user permission (or `view_abandoned_checkouts` for POS) — this is a permission check on top of the OAuth scope, not covered by scope grant alone. — https://shopify.dev/docs/api/admin-graphql/latest/queries/abandonedCheckouts
- API versions are released quarterly (January, April, July, October), named by release date (e.g. `2026-01`); each stable version is supported for a minimum window before retirement, and the endpoint path includes the version, e.g. `/admin/api/2026-01/graphql.json`. — https://shopify.dev/docs/api/usage/versioning
- `ShopifyPaymentsPayout.bankAccount` and `.gross` are deprecated fields still present in the schema — https://shopify.dev/docs/api/admin-graphql/latest/objects/ShopifyPaymentsPayout
- `InventoryLevel.scheduledChanges` is deprecated — https://shopify.dev/docs/api/admin-graphql/latest/objects/InventoryLevel

## Sample row
Field shape only, constructed from the documented schema fields above (section: Fields). No fabricated business values.
```json
{
  "order": {
    "id": "gid://shopify/Order/000000000",
    "sourceName": "web",
    "totalPriceSet": { "shopMoney": { "amount": "0.00", "currencyCode": "USD" } },
    "currentTotalPriceSet": { "shopMoney": { "amount": "0.00", "currencyCode": "USD" } },
    "discountCodes": [],
    "taxLines": [
      { "title": "", "rate": 0.0, "ratePercentage": 0.0, "priceSet": { "shopMoney": { "amount": "0.00", "currencyCode": "USD" } }, "channelLiable": null }
    ],
    "shippingLines": { "edges": [ { "node": { "title": "" } } ] },
    "refunds": [],
    "lineItems": {
      "edges": [
        {
          "node": {
            "quantity": 0,
            "sku": "",
            "variant": { "sku": "", "price": "0.00", "inventoryItem": { "unitCost": { "amount": "0.00", "currencyCode": "USD" } } },
            "originalUnitPriceSet": { "shopMoney": { "amount": "0.00", "currencyCode": "USD" } },
            "discountedUnitPriceSet": { "shopMoney": { "amount": "0.00", "currencyCode": "USD" } },
            "discountAllocations": []
          }
        }
      ]
    },
    "customerJourneySummary": {
      "customerOrderIndex": 0,
      "daysToConversion": 0,
      "ready": true,
      "firstVisit": { "occurredAt": "", "source": "", "referrerUrl": "", "landingPage": "", "utmParameters": { "source": "", "medium": "", "campaign": "", "content": "", "term": "" } },
      "lastVisit": { "occurredAt": "", "source": "", "referrerUrl": "", "landingPage": "", "utmParameters": { "source": "", "medium": "", "campaign": "", "content": "", "term": "" } }
    }
  }
}
```

## Maps to ecomOS tables
| Table in contracts/data-sources.md | Fields used |
|---|---|
| `orders` | Order.id, createdAt, customer, lineItems (sku, quantity), Order.totalPriceSet/currentTotalPriceSet (subtotal, total), discountApplications/discountCodes (discount), TaxLine.priceSet (tax by jurisdiction via taxLines), shippingLine (shipping), sourceName (channel), customerJourneySummary/CustomerVisit/UTMParameters (utm), status, refunds |
| `customers` | Customer.id, orders (first_order_at derived), numberOfOrders (orders_count), amountSpent (total_spent), emailMarketingConsent/smsMarketingConsent (email_consent, sms_consent) |
| `products` | ProductVariant.sku, price; InventoryItem.unitCost (cost) |
| `inventory` | InventoryLevel.quantities, location (stock by sku by day) |
| `reversed_orders` | Return.status/returnLineItems (return), ShopifyPaymentsDispute.status/amount/type (chargeback); return to origin stays null for US per app/CLAUDE.md |
| `payouts` | ShopifyPaymentsPayout.net, issuedAt, summary, transactionType |

## Follow-ups for a later pass
Flagged by the research session as not independently verified this pass; worth a direct fetch before this census is treated as exhaustive:
- `Refund`, `RefundLineItem`, `DiscountApplication`, `ShippingLine` sub-object field lists (only their parent-level fields on Order are confirmed here) — https://shopify.dev/docs/api/admin-graphql/latest/objects/Refund, https://shopify.dev/docs/api/admin-graphql/latest/objects/DiscountApplication, https://shopify.dev/docs/api/admin-graphql/latest/objects/ShippingLine
- The newer `Abandonment` object and `abandonmentByAbandonedCheckoutId` query, which may carry abandonment-cause and recovery-attempt fields not on `AbandonedCheckout` itself — https://shopify.dev/docs/api/admin-graphql/latest/objects/Abandonment
- Exact numeric pagination ceilings (per-request and total item caps) — https://shopify.dev/docs/api/usage/pagination-graphql
