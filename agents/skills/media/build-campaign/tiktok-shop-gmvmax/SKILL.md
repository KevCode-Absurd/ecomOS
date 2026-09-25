---
    name: tiktok-shop-gmvmax
    owner: media-buyer
    version: 1
    invoke_when: TikTok Shop is launching or the quarterly SKU review is due
    inputs: catalogue, margin by SKU, TikTok Seller Center state
    outputs: Shop setup checklist, GMV Max SKU list, change list
    ---
    Purpose: get TikTok Shop selling with complete listings, and keep GMV Max's
    automated spend limited to SKUs whose margin can absorb it.

    Steps
    1. Complete listings in Seller Center: images, descriptions, pricing, before
       any sale attempt.
    2. Verify the Shopify-TikTok connector is the official app before linking.
    3. Build TikTok Search with 20-50 keywords, phrase match; keep adding negatives.
    4. Rank SKUs by margin; put only the top 20 percent into GMV Max.
    5. Set GMV Max's ROI target above break-even for those SKUs, never a flat
       number copied from another platform.
    6. Test an alternate storefront template against the current one.

    Checks
    - No SKU with thin margin sits in GMV Max.
    - Listings are complete before any spend starts.

    Output: Shop setup checklist, GMV Max SKU list, change list.

    Example: a SKU has 18% margin while the top 20% cutoff is 35% margin -> excluded
    from GMV Max even if it is a bestseller by unit volume.
