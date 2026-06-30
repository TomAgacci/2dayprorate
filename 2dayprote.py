import math
from dataclasses import dataclass
from typing import Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------
# Core unit & building models
# -----------------------------

@dataclass
class UnitType:
    name: str
    count: int
    base_monthly_rent: float
    cost_weight: float = 1.0  # heavier units get more cost allocation


@dataclass
class SeasonalCurve:
    """
    month_index: 1..12 -> multiplier on variable costs
    e.g. higher utilities in winter, more repairs in storm season.
    """
    multipliers: Dict[int, float]  # {month: multiplier}

    def get_multiplier(self, month: int) -> float:
        return self.multipliers.get(month, 1.0)


@dataclass
class Building:
    name: str

    # Operating costs
    fixed_costs: Dict[str, float]          # insurance, taxes, etc. (monthly)
    variable_costs: Dict[str, float]       # utilities, repairs, etc. (base monthly)
    staff_salaries: Dict[str, float]       # staff cost per month

    # Capital & depreciation
    annual_depreciation: float             # straight-line depreciation per year
    annual_capex: float                    # planned capex per year (amortized monthly)

    # Vacancy & seasonality
    base_vacancy_rate: float               # long-run vacancy (0..1)
    seasonal_curve: SeasonalCurve

    # Units
    unit_types: Dict[str, UnitType]

    def monthly_depreciation(self) -> float:
        return self.annual_depreciation / 12.0

    def monthly_capex_amortization(self) -> float:
        return self.annual_capex / 12.0

    def total_monthly_cost(self, month: int) -> float:
        season_mult = self.seasonal_curve.get_multiplier(month)

        fixed = sum(self.fixed_costs.values())
        variable = sum(self.variable_costs.values()) * season_mult
        staff = sum(self.staff_salaries.values())
        dep = self.monthly_depreciation()
        capex = self.monthly_capex_amortization()

        return fixed + variable + staff + dep + capex

    def total_weight(self) -> float:
        return sum(ut.count * ut.cost_weight for ut in self.unit_types.values())

    def cost_per_unit_type(self, month: int) -> Dict[str, float]:
        total_cost = self.total_monthly_cost(month)
        total_weight = self.total_weight()

        alloc = {}
        for name, ut in self.unit_types.items():
            weight_share = (ut.count * ut.cost_weight) / total_weight
            alloc[name] = total_cost * weight_share
        return alloc

    def cost_per_unit(self, month: int) -> Dict[str, float]:
        alloc = self.cost_per_unit_type(month)
        return {name: alloc[name] / ut.count for name, ut in self.unit_types.items()}

    def effective_monthly_rent_per_unit(self, unit_name: str) -> float:
        """
        Rent after vacancy: base_rent * (1 - vacancy_rate).
        """
        ut = self.unit_types[unit_name]
        return ut.base_monthly_rent * (1.0 - self.base_vacancy_rate)


@dataclass
class Portfolio:
    buildings: Dict[str, Building]

    def unit_rent_cost_table(self, month: int) -> pd.DataFrame:
        """
        Per-unit table:
        - monthly rent
        - 2/30 base (2-day rent)
        - 30-day total
        - cost per unit
        - margin
        """
        rows = []
        for bname, b in self.buildings.items():
            unit_costs = b.cost_per_unit(month)
            for uname, cost in unit_costs.items():
                ut = b.unit_types[uname]
                monthly_rent = b.effective_monthly_rent_per_unit(uname)
                daily_rent = monthly_rent / 30.0
                two_day_rent = daily_rent * 2.0

                rows.append({
                    "building": bname,
                    "unit_type": uname,
                    "units": ut.count,
                    "monthly_rent": round(monthly_rent, 2),
                    "two_day_rent (2/30)": round(two_day_rent, 2),
                    "30_day_rent_total": round(monthly_rent, 2),
                    "cost_per_unit": round(cost, 2),
                    "margin_per_unit": round(monthly_rent - cost, 2)
                })
        return pd.DataFrame(rows)


# -----------------------------
# Income + Tama-style risk
# -----------------------------

@dataclass
class IncomeProfile:
    monthly_income: float
    social_security: float
    essentials: float

    @property
    def total_resources(self) -> float:
        return self.monthly_income + self.social_security

    @property
    def residual_after_essentials(self) -> float:
        return self.total_resources - self.essentials


@dataclass
class TamaRiskModel:
    base_default_prob: float = 0.03
    low_burden_threshold: float = 0.15
    high_burden_threshold: float = 0.35
    medium_scale: float = 2.0
    high_scale: float = 5.0

    def default_prob(self, monthly_rent: float, income: IncomeProfile) -> float:
        residual = max(income.residual_after_essentials, 1e-6)
        burden = monthly_rent / residual

        if burden <= self.low_burden_threshold:
            p = self.base_default_prob
        elif burden >= self.high_burden_threshold:
            excess = burden - self.high_burden_threshold
            p = self.base_default_prob * (self.high_scale + 10 * excess)
        else:
            scale = self.medium_scale + 5 * (burden - self.low_burden_threshold)
            p = self.base_default_prob * scale

        return max(0.0, min(1.0, p))


def eviction_and_support_view(
    portfolio: Portfolio,
    month: int,
    income: IncomeProfile,
    risk_model: TamaRiskModel
) -> pd.DataFrame:
    df = portfolio.unit_rent_cost_table(month)
    probs = []
    sufficiency = []

    for _, row in df.iterrows():
        rent = row["monthly_rent"]
        p = risk_model.default_prob(rent, income)
        probs.append(round(p, 4))

        residual = income.residual_after_essentials
        sufficiency.append(residual >= rent)

    df["eviction_prob"] = probs
    df["support_sufficient"] = sufficiency
    return df


# -----------------------------
# Heatmap plotting
# -----------------------------

def plot_eviction_heatmap(df_view, value_col="eviction_prob"):
    pivot = df_view.pivot(index="unit_type", columns="building", values=value_col)

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="Reds",
        vmin=0,
        vmax=1,
        linewidths=0.5,
        linecolor="black"
    )
    plt.title("Eviction Probability Heatmap")
    plt.xlabel("Building")
    plt.ylabel("Unit Type")
    plt.tight_layout()
    plt.show()


def plot_support_heatmap(df_view):
    pivot = df_view.pivot(index="unit_type", columns="building", values="support_sufficient")

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot,
        annot=True,
        cmap="Greens",
        linewidths=0.5,
        linecolor="black"
    )
    plt.title("Support Sufficiency Heatmap (Income + Social Security)")
    plt.xlabel("Building")
    plt.ylabel("Unit Type")
    plt.tight_layout()
    plt.show()


# -----------------------------
# Example usage
# -----------------------------

if __name__ == "__main__":
    # Seasonal curve: simple example
    seasonal = SeasonalCurve({
        1: 1.2,  # higher utilities in Jan
        7: 1.1   # slightly higher in July
    })

    # Portfolio with two buildings
    portfolio = Portfolio(buildings={
        "A": Building(
            name="A",
            fixed_costs={"insurance": 3000, "taxes": 5000},
            variable_costs={"utilities": 2000, "repairs": 1500},
            staff_salaries={"manager": 4000, "maintenance": 2500},
            annual_depreciation=60000,
            annual_capex=24000,
            base_vacancy_rate=0.08,
            seasonal_curve=seasonal,
            unit_types={
                "Studio": UnitType("Studio", 20, base_monthly_rent=900, cost_weight=1.0),
                "1BR": UnitType("1BR", 15, base_monthly_rent=1200, cost_weight=1.3),
            }
        ),
        "B": Building(
            name="B",
            fixed_costs={"insurance": 2500, "taxes": 4000},
            variable_costs={"utilities": 1800, "repairs": 1200},
            staff_salaries={"manager": 3500},
            annual_depreciation=48000,
            annual_capex=18000,
            base_vacancy_rate=0.12,
            seasonal_curve=seasonal,
            unit_types={
                "Micro": UnitType("Micro", 30, base_monthly_rent=700, cost_weight=0.8),
                "1BR": UnitType("1BR", 10, base_monthly_rent=1100, cost_weight=1.2),
            }
        )
    })

    # Income + Social Security profile
    income = IncomeProfile(
        monthly_income=900,
        social_security=600,
        essentials=800
    )

    risk_model = TamaRiskModel()

    # Choose month (1 = January)
    month = 1

    # Build per-unit view
    df_view = eviction_and_support_view(portfolio, month, income, risk_model)
    print(df_view)

    # Plot heatmaps
    plot_eviction_heatmap(df_view)
    plot_support_heatmap(df_view)
