"""Narrative scaffolding utilities."""

from __future__ import annotations

import textwrap

import pandas as pd

TEMPLATE = """# Cultural Futures Brief

## Snapshot
- Horizon: {horizon} periods
- Series analyzed: {series_count}
- Models evaluated: {models}

## Highlights
{highlights}

## Narrative Angles
1. **Safe-Haven Signals** — {safe_haven}
2. **Media Momentum** — {media_momentum}
3. **Macro Crosswinds** — {macro_crosswinds}

*Generated automatically. Expand with qualitative context before publication.*
"""


def build_narrative_brief(df: pd.DataFrame) -> str:
    """Produce a markdown narrative summary from forecast output."""
    horizon = df.groupby("unique_id").size().median()
    series_count = df["unique_id"].nunique()
    models = ", ".join(sorted(df.get("model_family", "unknown").unique()))

    def describe_trend(subset: pd.DataFrame) -> str:
        sample = subset.sort_values("ds").tail(3)["y"].tolist()
        if len(sample) < 2:
            return "insufficient data"
        if sample[-1] > sample[0]:
            return "upward trajectory"
        if sample[-1] < sample[0]:
            return "downward trajectory"
        return "holding steady"

    safe_haven = describe_trend(
        df[df["unique_id"].str.contains("gold", case=False, na=False)]
    )
    media_momentum = describe_trend(
        df[df["unique_id"].str.contains("film|media", case=False, na=False)]
    )
    macro_crosswinds = describe_trend(
        df[df["unique_id"].str.contains("inflation|sentiment", case=False, na=False)]
    )
    highlights = textwrap.fill(
        "Preliminary models indicate divergent futures across commodity and cultural signals; use these projections to stage scenario narratives.",
        width=88,
    )
    return TEMPLATE.format(
        horizon=int(horizon) if not pd.isna(horizon) else "unknown",
        series_count=series_count,
        models=models,
        highlights=highlights,
        safe_haven=safe_haven,
        media_momentum=media_momentum,
        macro_crosswinds=macro_crosswinds,
    )
