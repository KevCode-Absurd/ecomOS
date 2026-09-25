# PROD rooms: what they show that common tools do not

Three rooms: Products and research, Supply and inventory, Marketplaces and quick commerce.

**Products and research.** Helium 10 and Jungle Scout read Amazon Brand Analytics and keyword demand only. This room joins video-commerce demand, ad library spend and DTC review mining in one screen, then runs a coded margin and compliance gate before sourcing spend happens. It checks a live SKU's actual margin against the gate's model, which Shopify's CM1-only profit-by-SKU report cannot do since it never allocates ad spend or return cost. A visible time box per candidate keeps research from sprawling.

**Supply and inventory.** Katana and Cin7 size reorder points from velocity and lead time alone. This room recomputes landed cost the moment FX, freight or duty moves and flags a margin recheck, and sizes safety stock against India-specific spike risk (festive demand, COD-market RTO). Shiprocket and NimbusPost report courier RTO and NDR data in aggregate; this room ties the courier scorecard to the brand's own COD reversal cost to decide, per order, whether another attempt is worth it. Peak-season readiness rolls stock, staffing and WMS load into one percentage instead of a split spreadsheet.

**Marketplaces and quick commerce.** Blinkit, Zepto and Instamart dashboards commonly report ROAS on MRP, overstating real return 30 to 50 percent; this room recomputes ROAS from transaction value and shows the gap. Amazon Brand Analytics covers Amazon only; this room watches Buy Box, reviews, listing health and account risk together across Amazon, Flipkart, Myntra, Nykaa, Blinkit and Zepto. It reconciles marketplace settlements against order records automatically, normally done by hand per platform, and splits an Amazon sales change into traffic versus conversion before calling a product a failure.

## Hardest data to get

- True transaction-value order exports from quick commerce (platforms default to MRP-based numbers; real value per order may need a data-sharing agreement).
- Marketplace settlement files in a reconcilable, per-order format (Amazon, Flipkart and quick commerce use different schemas and cadences).
- Courier-level NDR and COD remittance data fine enough to tie a reschedule decision to unit economics (most aggregators expose this at account level, not per shipment).
- BIS, hallmarking and FSSAI compliance status per SKU (lives in physical certificates and supplier paperwork, not an API).
- Ad library and video-commerce demand signals (public but needs scraping or a paid tool; no clean feed exists).
