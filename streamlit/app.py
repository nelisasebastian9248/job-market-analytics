
from __future__ import annotations

import sys
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from ingestion.utils.snowflake import get_snowflake_connection


SKILL_DEMAND_SQL = """
select skill, skill_mentions, distinct_jobs, distinct_companies
from JOB_MARKET_ANALYTICS.MART.MART_SKILL_DEMAND
order by skill_mentions desc
"""

GITHUB_MOMENTUM_SQL = """
select full_name, stargazers_count, forks_count, subscribers_count, open_issues_count, momentum_score
from JOB_MARKET_ANALYTICS.MART.MART_GITHUB_REPO_MOMENTUM
order by momentum_score desc
"""

SALARY_BENCHMARKS_SQL = """
select job_title, location_display_name, job_postings, avg_salary_min, avg_salary_max
from JOB_MARKET_ANALYTICS.MART.MART_SALARY_BENCHMARKS
order by job_postings desc, avg_salary_max desc
"""


@st.cache_data(ttl=600)
def load_dataframe(query: str) -> pd.DataFrame:
    with get_snowflake_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
            columns = [column[0].lower() for column in cursor.description]
    return pd.DataFrame(rows, columns=columns)


def format_currency(value: float) -> str:
    return f"${value:,.0f}"


def format_integer(value: int | float) -> str:
    return f"{int(value):,}"


def format_repo_name(full_name: str) -> str:
    return full_name.split("/")[-1].replace("-", " ").title()


def build_bar_chart(data: pd.DataFrame, category_col: str, value_col: str) -> alt.Chart:
    return (
        alt.Chart(data)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6, color="#ff4fa3")
        .encode(
            x=alt.X(
                f"{category_col}:N",
                sort="-y",
                axis=alt.Axis(
                    labelColor="#f7d3e5",
                    title=None,
                    labelAngle=-40,
                    labelPadding=10,
                ),
            ),
            y=alt.Y(
                f"{value_col}:Q",
                axis=alt.Axis(labelColor="#f7d3e5", title=None, gridColor="#4b1e36"),
            ),
            tooltip=[category_col, value_col],
        )
        .properties(height=360)
        .configure_view(strokeWidth=0)
        .configure(background="transparent")
    )


# ── NEW: styled HTML table renderer ──────────────────────────────────────────
def render_html_table(df: pd.DataFrame) -> None:
    """Render a DataFrame as a fully styled HTML table that matches the dark-pink theme."""
    header_cells = "".join(f"<th>{col}</th>" for col in df.columns)

    body_rows = ""
    for i, (_, row) in enumerate(df.iterrows()):
        row_class = "even" if i % 2 == 0 else "odd"
        cells = "".join(f"<td>{val}</td>" for val in row)
        body_rows += f'<tr class="{row_class}">{cells}</tr>'

    html = f"""
    <style>
      .styled-table-wrap {{
        width: 100%;
        overflow-x: auto;
        border-radius: 18px;
        border: 1px solid rgba(255, 92, 177, 0.22);
        box-shadow: 0 12px 28px rgba(0, 0, 0, 0.28);
        margin-bottom: 1rem;
      }}
      .styled-table {{
        width: 100%;
        border-collapse: collapse;
        font-family: inherit;
        font-size: 0.9rem;
      }}
      .styled-table thead tr {{
        background: linear-gradient(90deg, #4e1434 0%, #3a0d26 100%);
      }}
      .styled-table thead th {{
        padding: 0.75rem 1rem;
        text-align: left;
        color: #ffd6ea;
        font-weight: 700;
        letter-spacing: 0.04em;
        border-bottom: 1px solid rgba(255, 92, 177, 0.28);
        white-space: nowrap;
      }}
      .styled-table tbody tr.even {{
        background: rgba(28, 12, 22, 0.92);
      }}
      .styled-table tbody tr.odd {{
        background: rgba(44, 16, 34, 0.82);
      }}
      .styled-table tbody tr:hover {{
        background: rgba(94, 23, 61, 0.80) !important;
        transition: background 0.15s ease;
      }}
      .styled-table tbody td {{
        padding: 0.65rem 1rem;
        color: #fff2f8;
        border-bottom: 1px solid rgba(255, 143, 201, 0.07);
        white-space: nowrap;
      }}
      .styled-table tbody tr:last-child td {{
        border-bottom: none;
      }}
    </style>
    <div class="styled-table-wrap">
      <table class="styled-table">
        <thead><tr>{header_cells}</tr></thead>
        <tbody>{body_rows}</tbody>
      </table>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────────────────


def render_styles() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 15% 20%, rgba(255, 45, 149, 0.26), transparent 24%),
                radial-gradient(circle at 85% 18%, rgba(255, 122, 196, 0.18), transparent 22%),
                radial-gradient(circle at 50% 80%, rgba(255, 45, 149, 0.12), transparent 28%),
                linear-gradient(160deg, #090909 0%, #111111 48%, #190914 100%);
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .hero-card {
            padding: 1.4rem 1.6rem;
            border: 1px solid rgba(255, 92, 177, 0.18);
            border-radius: 22px;
            background: linear-gradient(135deg, rgba(19, 19, 19, 0.94), rgba(34, 10, 25, 0.88));
            backdrop-filter: blur(6px);
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.32);
            margin-bottom: 1rem;
        }
        .hero-kicker {
            color: #ff7cc5;
            font-size: 0.85rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }
        .hero-title {
            color: #fff4fb;
            font-size: 2.7rem;
            line-height: 1.05;
            font-weight: 800;
            margin: 0.35rem 0 0.75rem 0;
        }
        .hero-copy {
            color: #d7c5d0;
            font-size: 1rem;
            max-width: 52rem;
            margin: 0;
        }
        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(18, 18, 18, 0.9), rgba(40, 12, 28, 0.78));
            border: 1px solid rgba(255, 92, 177, 0.18);
            border-radius: 18px;
            padding: 0.85rem 1rem;
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.2);
        }
        div[data-testid="stMetricLabel"] {
            color: #ff9fd2;
        }
        div[data-testid="stMetricValue"] {
            color: #fff7fb;
        }
        .section-note {
            color: #d7bfd0;
            font-size: 0.92rem;
            margin-bottom: 0.5rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            background: rgba(16, 16, 16, 0.55);
            border-radius: 16px;
            padding: 0.35rem;
        }
        .stTabs [data-baseweb="tab"] {
            color: #f7d3e5;
            border-radius: 12px;
            background: transparent;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, rgba(255, 45, 149, 0.24), rgba(255, 122, 196, 0.18));
            color: white;
        }
        div[data-testid="stMarkdownContainer"] p {
            color: #ecd8e4;
        }
        h1, h2, h3 {
            color: #fff4fb !important;
        }
        label, .stSlider label {
            color: #ffd4e9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    st.set_page_config(
        page_title="Job Market Analytics",
        page_icon="J",
        layout="wide",
    )
    render_styles()

    st.markdown(
        """
        <div class="hero-card">
            <div class="hero-kicker">Job Market Analytics</div>
            <div class="hero-title">Track what data engineering teams hire for and what the tool ecosystem is building around.</div>
            <p class="hero-copy">
                This dashboard combines Snowflake marts for skill demand, salary benchmarks, and open-source tool activity.
                It is designed to answer one practical question: which modern data platform skills show up in hiring demand, and how does that compare to developer ecosystem momentum?
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    skill_df = load_dataframe(SKILL_DEMAND_SQL)
    github_df = load_dataframe(GITHUB_MOMENTUM_SQL)
    salary_df = load_dataframe(SALARY_BENCHMARKS_SQL)

    top_skill_mentions = int(skill_df["skill_mentions"].sum()) if not skill_df.empty else 0
    tracked_repos = int(len(github_df))
    salary_rows = int(len(salary_df))
    top_skill = skill_df.iloc[0]["skill"] if not skill_df.empty else "n/a"
    top_repo = (
        format_repo_name(str(github_df.iloc[0]["full_name"])) if not github_df.empty else "n/a"
    )

    metric_col_1, metric_col_2, metric_col_3, metric_col_4 = st.columns(4)
    metric_col_1.metric("Tracked skill mentions", f"{top_skill_mentions}")
    metric_col_2.metric("GitHub repos tracked", f"{tracked_repos}")
    metric_col_3.metric("Salary benchmark rows", f"{salary_rows}")
    metric_col_4.metric("Current leaders", f"{top_skill} / {top_repo}")

    skills_tab, salary_tab, tools_tab = st.tabs(
        ["Skill Demand", "Salary Benchmarks", "Tool Momentum"]
    )

    with skills_tab:
        st.subheader("Top Skill Demand")
        st.markdown(
            '<div class="section-note">These counts come from tracked skills matched against current data engineering and analytics engineering job descriptions.</div>',
            unsafe_allow_html=True,
        )
        skill_limit = st.slider("Number of skills", min_value=5, max_value=20, value=10)
        top_skills = skill_df.head(skill_limit).copy()
        top_skills["skill"] = top_skills["skill"].str.title()
        st.altair_chart(
            build_bar_chart(top_skills, "skill", "skill_mentions"),
            use_container_width=True,
        )
        skill_display_df = top_skills.rename(
            columns={
                "skill": "Skill",
                "skill_mentions": "Mentions",
                "distinct_jobs": "Jobs",
                "distinct_companies": "Companies",
            }
        )
        # ── CHANGED: st.dataframe → render_html_table ──
        render_html_table(skill_display_df)

    with salary_tab:
        st.subheader("Salary Benchmarks")
        st.caption(
            "Grouped by job title and source location so you can see where salary bands concentrate."
        )
        title_options = ["All"] + sorted(salary_df["job_title"].dropna().unique().tolist())
        selected_title = st.selectbox("Filter by job title", options=title_options, index=0)

        filtered_salary_df = salary_df.copy()
        if selected_title != "All":
            filtered_salary_df = filtered_salary_df[filtered_salary_df["job_title"] == selected_title]

        salary_display_df = filtered_salary_df.copy()
        if not salary_display_df.empty:
            salary_display_df["job_postings"] = salary_display_df["job_postings"].map(format_integer)
            salary_display_df["avg_salary_min"] = salary_display_df["avg_salary_min"].map(format_currency)
            salary_display_df["avg_salary_max"] = salary_display_df["avg_salary_max"].map(format_currency)
        salary_display_df = salary_display_df.rename(
            columns={
                "job_title": "Job Title",
                "location_display_name": "Location",
                "job_postings": "Postings",
                "avg_salary_min": "Avg Salary Min",
                "avg_salary_max": "Avg Salary Max",
            }
        )
        # ── CHANGED: st.dataframe → render_html_table ──
        render_html_table(salary_display_df)

    with tools_tab:
        st.subheader("Data Engineering Tool Momentum")
        st.markdown(
            '<div class="section-note">GitHub metrics here represent ecosystem activity around data platform and analytics engineering tools, rather than a direct one-to-one match for every hiring skill.</div>',
            unsafe_allow_html=True,
        )
        github_display_df = github_df.copy()
        github_display_df["tool"] = github_display_df["full_name"].map(format_repo_name)
        st.altair_chart(
            build_bar_chart(github_display_df, "tool", "momentum_score"),
            use_container_width=True,
        )
        github_display_df["stargazers_count"] = github_display_df["stargazers_count"].map(format_integer)
        github_display_df["forks_count"] = github_display_df["forks_count"].map(format_integer)
        github_display_df["subscribers_count"] = github_display_df["subscribers_count"].map(format_integer)
        github_display_df["open_issues_count"] = github_display_df["open_issues_count"].map(format_integer)
        github_display_df["momentum_score"] = github_display_df["momentum_score"].map(format_integer)
        github_display_df = github_display_df.rename(
            columns={
                "tool": "Tool",
                "stargazers_count": "Stars",
                "forks_count": "Forks",
                "subscribers_count": "Watchers",
                "open_issues_count": "Open Issues",
                "momentum_score": "Momentum Score",
            }
        )
        # ── CHANGED: st.dataframe → render_html_table ──
        render_html_table(
            github_display_df[["Tool", "Stars", "Forks", "Watchers", "Open Issues", "Momentum Score"]]
        )


if __name__ == "__main__":
    main()