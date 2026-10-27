"""Example DiD analysis: TWFE, event study, and a heterogeneity-robust estimator (did2s)."""

from pathlib import Path
from typing import Annotated

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import pyfixest as pf
from pytask import Product

from econ.config import CLEAN, FIGURES, TABLES


def task_did_example(
    src: Path = CLEAN / "panel.parquet",
    table: Annotated[Path, Product] = TABLES / "did_main.tex",
    figure: Annotated[Path, Product] = FIGURES / "event_study.pdf",
    numbers: Annotated[Path, Product] = TABLES / "numbers.tex",
) -> None:
    df = pd.read_parquet(src)
    vcov = {"CRV1": "state"}

    twfe = pf.feols("y ~ treat_post | state + year", data=df, vcov=vcov)
    gardner = pf.did2s(
        df,
        yname="y",
        first_stage="~ 0 | state + year",
        second_stage="~ treat_post",
        treatment="treat_post",
        cluster="state",
    )
    table.write_text(pf.etable([twfe, gardner], type="tex", labels={"treat_post": "Treated $\\times$ Post"}))

    # Never-treated units (rel_time == -1000) join the omitted reference period; bin event time to [-6, 6].
    es_df = df.assign(rel_time=df.rel_time.replace(-1000, -1).clip(-6, 6))
    es = pf.feols("y ~ i(rel_time, ref=-1) | state + year", data=es_df, vcov=vcov)
    coefs = es.tidy().reset_index()
    coefs["k"] = coefs["Coefficient"].str.extract(r"\[T?\.?(-?[\d.]+)\]").astype(float)
    coefs = pd.concat([coefs, pd.DataFrame({"k": [-1.0], "Estimate": [0.0], "2.5%": [0.0], "97.5%": [0.0]})]).sort_values("k")
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.errorbar(coefs.k, coefs.Estimate, yerr=[coefs.Estimate - coefs["2.5%"], coefs["97.5%"] - coefs.Estimate], fmt="o", capsize=3)
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(-0.5, color="grey", ls="--", lw=0.8)
    ax.set_xlabel("Years relative to treatment")
    ax.set_ylabel("Effect on y")
    fig.tight_layout()
    fig.savefig(figure)

    b, se = twfe.coef()["treat_post"], twfe.se()["treat_post"]
    numbers.write_text(
        f"\\newcommand{{\\twfeEffect}}{{{b:.3f}}}\n"
        f"\\newcommand{{\\twfeSE}}{{{se:.3f}}}\n"
        f"\\newcommand{{\\nObs}}{{{len(df):,}}}\n"
    )
