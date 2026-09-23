"""Auditable token-cost scenarios; estimates, never spending authorization."""
from dataclasses import dataclass
from decimal import Decimal
from math import ceil

MILLION = Decimal(1_000_000)


@dataclass(frozen=True)
class Price:
    input: Decimal
    output: Decimal
    batch_factor: Decimal = Decimal("0.5")


PRICES = {
    "gpt-5.6-luna": Price(Decimal("0.20"), Decimal("1.20")),
    "gpt-5.6-terra": Price(Decimal("2"), Decimal("12")),
    "gpt-5.6-sol": Price(Decimal("4"), Decimal("20")),
    "gpt-6-astra": Price(Decimal("10"), Decimal("50")),
    "claude-sonnet-5": Price(Decimal("2"), Decimal("10")),
    "gemini-3.8-flash": Price(Decimal("0.75"), Decimal("3.75")),
    "text-embedding-3-small": Price(Decimal("0.02"), Decimal("0"), Decimal("1")),
}
PRICE_DATE = "2026-09-22"


def token_cost(model, input_tokens, output_tokens, batch=False):
    if input_tokens < 0 or output_tokens < 0:
        raise ValueError("Token counts cannot be negative")
    price = PRICES[model]
    factor = price.batch_factor if batch else Decimal("1")
    return ((Decimal(input_tokens) * price.input + Decimal(output_tokens) * price.output)
            / MILLION * factor)


def estimate(sources=350, raw_tokens_per_source=30000, batch=False,
             extraction_model="claude-sonnet-5", reserve=0.30,
             output_scale=1.0, verification_scale=1.0):
    """Billable output includes any reasoning tokens. Fixed output is an assumption.

    Input volumes are aggregate across the bounded calls for each source, NOT
    one full-document request. Reserve is contingency, not a guaranteed ceiling.
    Increase output_scale and verification_scale for dense, high-card-yield works.
    """
    if sources < 1 or raw_tokens_per_source < 1 or reserve < 0:
        raise ValueError("Positive source/token counts and nonnegative reserve required")
    if output_scale <= 0 or verification_scale <= 0:
        raise ValueError("Scales must be positive")
    rows = []

    def add(stage, model, units, inputs, outputs):
        total_input, total_output = units * inputs, units * outputs
        cost = token_cost(model, total_input, total_output, batch)
        rows.append(dict(stage=stage, model=model, units=units,
                         input_tokens=total_input, output_tokens=total_output,
                         usd=float(cost)))

    add("routing", "gpt-5.6-luna", sources, 6000, 500)
    add("extraction", extraction_model, sources,
        ceil(raw_tokens_per_source * 1.25), ceil(8000 * output_scale))
    add("evidence_verification", "gpt-5.6-terra", sources,
        ceil(raw_tokens_per_source * 0.8 * verification_scale),
        ceil(4000 * output_scale * verification_scale))
    add("difficult_cases", "gpt-5.6-sol", ceil(sources * 0.2), 12000, 2000)
    add("duplicate_candidates", "gpt-5.6-luna", sources, 8000, 500)
    add("playbook_composition", "gpt-5.6-sol", 100, 8000, 2000)
    add("evaluation", "gpt-5.6-terra", 200, 6000, 1000)
    add("embeddings", "text-embedding-3-small", sources,
        raw_tokens_per_source + ceil(8000 * output_scale), 0)
    subtotal = sum(Decimal(str(r["usd"])) for r in rows)
    return {"price_date": PRICE_DATE, "currency": "USD", "batch": batch,
            "assumptions": {"sources": sources, "raw_tokens_per_source": raw_tokens_per_source,
                            "output_scale": output_scale, "verification_scale": verification_scale,
                            "reserve_fraction": reserve},
            "stages": rows, "subtotal_usd": float(subtotal),
            "with_reserve_usd": float(subtotal * (1 + Decimal(str(reserve)))),
            "excludes": ["hosting", "human review", "taxes", "OCR/audio/video",
                         "external fact checking/search", "engineering labor"],
            "warning": "Planning scenario, not a quote. Recheck prices and actual provider tokenization."}

