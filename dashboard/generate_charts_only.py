from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
from snowflake_utils import load_from_snowflake
import traceback

ROOT = Path(__file__).parent
PUBLIC = ROOT / "public"
PUBLIC.mkdir(exist_ok=True)

CHART_COUNTRY = PUBLIC / "chart_country.png"
CHART_ALT = PUBLIC / "chart_altitude.png"
CHART_VEL = PUBLIC / "chart_velocity.png"

def safe_get(df, col):
    return col in df.columns

def generate_charts(df):
    try:
        print("generate_charts: start")
        try:
            import seaborn  # noqa: F401
            plt.style.use("seaborn-darkgrid")
            print("Using seaborn-darkgrid")
        except Exception:
            try:
                plt.style.use("ggplot")
                print("Using ggplot fallback")
            except Exception:
                plt.rcdefaults()
                print("Using default matplotlib style")

        if safe_get(df, "ORIGIN_COUNTRY"):
            counts = df["ORIGIN_COUNTRY"].fillna("Unknown").value_counts().nlargest(10)
            fig, ax = plt.subplots(figsize=(6,3.5))
            counts.plot.bar(ax=ax, color="#2b8cbe")
            ax.set_title("Antal flyg per land (topp 10)")
            ax.set_ylabel("Antal")
            plt.tight_layout()
            fig.savefig(CHART_COUNTRY, dpi=120)
            plt.close(fig)
            print("Saved", CHART_COUNTRY)

        if safe_get(df, "ALTITUDE_BARO"):
            alt = df["ALTITUDE_BARO"].fillna(0)
            fig, ax = plt.subplots(figsize=(6,3.5))
            ax.hist(alt, bins=30, color="#7fc97f")
            ax.set_title("Höjdfördelning")
            ax.set_xlabel("Altitude (m)")
            ax.set_ylabel("Antal")
            plt.tight_layout()
            fig.savefig(CHART_ALT, dpi=120)
            plt.close(fig)
            print("Saved", CHART_ALT)

        if safe_get(df, "VELOCITY"):
            vel = df[["ICAO24","VELOCITY"]].dropna().sort_values("VELOCITY", ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(6,3.5))
            ax.barh(vel["ICAO24"].astype(str), vel["VELOCITY"], color="#f768a1")
            ax.invert_yaxis()
            ax.set_title("Topp 10 hastigheter (m/s)")
            ax.set_xlabel("Velocity")
            plt.tight_layout()
            fig.savefig(CHART_VEL, dpi=120)
            plt.close(fig)
            print("Saved", CHART_VEL)

        print("generate_charts: done")
        return True
    except Exception:
        traceback.print_exc()
        return False

if __name__ == "__main__":
    df = load_from_snowflake()
    ok = generate_charts(df)
    if not ok:
        print("Charts generation failed; se traceback ovan.")

