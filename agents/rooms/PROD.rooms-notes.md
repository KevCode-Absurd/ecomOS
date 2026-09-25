# PROD rooms: what they show that common tools do not

Three rooms: Products and research, Supply and inventory, Marketplaces and quick commerce.

**Products and research.** Helium 10 and Jungle Scout read Amazon Brand Analytics and keyword demand only. This room joins video-commerce demand, ad library spend and DTC review mining in one screen, then runs a coded margin and compliance gate before sourcing spend happens. It checks a live SKU's actual margin against the gate's model, which Shopify's CM1-only profit-by-SKU report cannot do since it never allocates ad spend or return cost. A visible time box per candidate keeps research from sprawling.

**Supply and inventory.** Katana and Cin7 size reorder points from velocity and lead time alone. This room recomputes landed cost the moment FX, freight or duty moves and flags a margin recheck, and sizes safety stock against peak-season spike risk (Q4/BFCM demand, carrier return-to-sender risk; India: festive demand and COD-market RTO, markets: IN). ShipStation, EasyPost and 3PLs report carrier exception data in aggregate (India: Shiprocket and NimbusPost report courier RTO and NDR data in aggregate); this room ties the carrier scorecard to the brand's own chargeback and return-to-sender cost (India: COD reversal cost) to decide, per order, whether another attempt is worth it. It shows chargebacks, disputes, return-to-sender and, for an India brand, RTO as one reversed-orders group next to the payment method mix (card, wallet, BNPL, and cod_share for India, markets: IN), instead of merging them into one number. Peak-season readiness rolls stock, staffing and WMS load into one percentage instead of a split spreadsheet.

**Marketplaces and quick commerce.** Instacart, DoorDash and Gopuff dashboards commonly report ROAS on list price (India: Blinkit, Zepto and Instamart on MRP), overstating real return 30 to 50 percent; this room recomputes ROAS from transaction value and shows the gap. Amazon Brand Analytics covers Amazon only; this room watches Buy Box, reviews, listing health and account risk together across Amazon, Walmart, Target Plus, eBay and TikTok Shop (India: Flipkart, Myntra, Nykaa, Blinkit and Zepto). It reconciles marketplace settlements against order records automatically, normally done by hand per platform, and splits an Amazon sales change into traffic versus conversion before calling a product a failure.

## Hardest data to get

- True transaction-value order exports from rapid-delivery/quick-commerce platforms (platforms default to list/MRP-based numbers; real value per order may need a data-sharing agreement).
- Marketplace settlement files in a reconcilable, per-order format (Amazon, Walmart and rapid-delivery platforms use different schemas and cadences; India: Amazon, Flipkart and quick commerce).
- Carrier-level exception and, for an India brand, COD remittance data fine enough to tie a reschedule decision to unit economics (most aggregators expose this at account level, not per shipment; India: NDR and COD remittance data, markets: IN).
- US labelling and quality-marking status per SKU (FTC quality mark, Care Labeling, Prop 65; India: BIS, hallmarking and FSSAI compliance status), which lives in physical certificates and supplier paperwork, not an API.
- Ad library and video-commerce demand signals (public but needs scraping or a paid tool; no clean feed exists).
