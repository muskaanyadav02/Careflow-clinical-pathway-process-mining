
import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# 1. CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data" / "processed"

QUALITY_FILE = DATA_DIR / "data_quality_report.json"
ACTIVITY_FILE = DATA_DIR / "activity_counts.csv"
BOTTLENECK_FILE = DATA_DIR / "bottleneck_summary.csv"

BG = "#080F1C"
SIDEBAR = "#0B1424"
PANEL = "#101D30"
PANEL_LIGHT = "#14243A"
BORDER = "#22354D"
TEXT = "#EDF4FC"
MUTED = "#91A4BB"
TEAL = "#2DD4BF"
CYAN = "#38BDF8"
PURPLE = "#A78BFA"
AMBER = "#FBBF24"
RED = "#FB7185"

st.set_page_config(
    page_title="CareFlow | Clinical Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM DESIGN SYSTEM
# ============================================================

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    :root {{
        --bg: {BG};
        --panel: {PANEL};
        --border: {BORDER};
        --text: {TEXT};
        --muted: {MUTED};
        --teal: {TEAL};
        --cyan: {CYAN};
    }}

    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(ellipse at 85% 0%, rgba(45,212,191,.075), transparent 35%),
            radial-gradient(ellipse at 10% 15%, rgba(56,189,248,.055), transparent 30%),
            {BG};
        color: {TEXT};
    }}

    [data-testid="stHeader"] {{
        background: rgba(8,15,28,.82);
    }}

    [data-testid="stSidebar"] {{
        background: {SIDEBAR};
        border-right: 1px solid {BORDER};
    }}

    [data-testid="stSidebar"] > div:first-child {{
        padding-top: 1.4rem;
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: {MUTED};
    }}

    [data-testid="stSidebar"] [data-testid="stRadio"] label {{
        padding: 7px 4px;
    }}

    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: {TEXT} !important;
        letter-spacing: -.35px;
    }}

    p, li, label {{
        color: {TEXT};
    }}

    [data-testid="stMetric"] {{
        background: linear-gradient(145deg, {PANEL_LIGHT}, {PANEL});
        border: 1px solid {BORDER};
        border-radius: 13px;
        padding: 17px 19px;
        min-height: 112px;
    }}

    [data-testid="stMetricLabel"] {{
        color: {MUTED} !important;
        font-size: .83rem;
    }}

    [data-testid="stMetricValue"] {{
        color: {TEXT} !important;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.8rem;
    }}

    [data-testid="stMetricDelta"] {{
        font-size: .76rem;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        border-color: {BORDER};
        border-radius: 14px;
    }}

    .hero {{
        position: relative;
        overflow: hidden;
        padding: 27px 30px;
        margin-bottom: 23px;
        border: 1px solid #25435A;
        border-radius: 17px;
        background: linear-gradient(115deg, #12243A 0%, #102A39 58%, #12333C 100%);
    }}

    .hero:after {{
        content: "";
        position: absolute;
        width: 220px;
        height: 220px;
        right: -50px;
        top: -105px;
        border-radius: 50%;
        border: 1px solid rgba(45,212,191,.20);
        box-shadow: 0 0 0 25px rgba(45,212,191,.025),
                    0 0 0 50px rgba(45,212,191,.02);
    }}

    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        color: #F8FAFC;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -.8px;
        margin: 0;
    }}

    .hero-subtitle {{
        color: #A8C0D5;
        font-size: .94rem;
        margin-top: 8px;
        margin-bottom: 0;
        max-width: 700px;
        line-height: 1.6;
    }}

    .eyebrow {{
        color: {TEAL};
        text-transform: uppercase;
        font-size: .70rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 9px;
    }}

    .section-heading {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.12rem;
        font-weight: 600;
        color: {TEXT};
        margin: 12px 0 4px;
    }}

    .section-subtitle {{
        color: {MUTED};
        font-size: .83rem;
        margin: 0 0 15px;
        line-height: 1.5;
    }}

    .panel {{
        background: linear-gradient(145deg, {PANEL}, #0D1829);
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px 20px;
        margin-bottom: 12px;
    }}

    .insight-label {{
        color: {MUTED};
        font-size: .75rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 9px;
    }}

    .insight-value {{
        color: {TEXT};
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 600;
        line-height: 1.4;
    }}

    .insight-detail {{
        color: {MUTED};
        font-size: .82rem;
        margin-top: 7px;
        line-height: 1.5;
    }}

    .status-pill {{
        display: inline-block;
        color: #6EE7B7;
        background: rgba(16,185,129,.12);
        border: 1px solid rgba(52,211,153,.3);
        padding: 6px 11px;
        border-radius: 30px;
        font-size: .76rem;
        font-weight: 700;
        letter-spacing: .4px;
    }}

    .footer {{
        border-top: 1px solid {BORDER};
        padding-top: 17px;
        margin-top: 32px;
        color: {MUTED};
        font-size: .75rem;
        line-height: 1.8;
    }}

    div.stButton > button {{
        border-radius: 9px;
        border: 1px solid {BORDER};
    }}

    [data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 10px;
        overflow: hidden;
    }}

    div[data-baseweb="select"] > div {{
        background: {PANEL};
        border-color: {BORDER};
    }}

    hr {{
        border-color: {BORDER};
    }}

    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. DATA LOADING AND VALIDATION
# ============================================================

@st.cache_data
def load_data():
    with QUALITY_FILE.open("r", encoding="utf-8") as f:
        quality = json.load(f)

    activities = pd.read_csv(ACTIVITY_FILE)
    transitions = pd.read_csv(BOTTLENECK_FILE)

    return quality, activities, transitions


if not all(p.exists() for p in [QUALITY_FILE, ACTIVITY_FILE, BOTTLENECK_FILE]):
    st.error(
        "Required analysis files were not found. "
        "Check that these files exist inside data/processed."
    )
    st.stop()

try:
    quality, activities, transitions = load_data()

    required_activity_cols = {"Activity_Name", "event_count"}
    required_transition_cols = {
        "from_activity",
        "to_activity",
        "transition_count",
        "average_time_minutes",
        "median_time_minutes",
        "maximum_time_minutes",
    }

    if not required_activity_cols.issubset(activities.columns):
        st.error("activity_counts.csv has unexpected column names.")
        st.stop()

    if not required_transition_cols.issubset(transitions.columns):
        st.error("bottleneck_summary.csv has unexpected column names.")
        st.stop()

    numeric_cols = [
        "event_count",
    ]
    for col in numeric_cols:
        activities[col] = pd.to_numeric(activities[col], errors="coerce")

    for col in [
        "transition_count",
        "average_time_minutes",
        "median_time_minutes",
        "maximum_time_minutes",
    ]:
        transitions[col] = pd.to_numeric(transitions[col], errors="coerce")

    activities = activities.dropna(subset=["Activity_Name", "event_count"])
    transitions = transitions.dropna(
        subset=[
            "from_activity",
            "to_activity",
            "transition_count",
            "average_time_minutes",
            "median_time_minutes",
            "maximum_time_minutes",
        ]
    )

    activities["event_count"] = activities["event_count"].astype(int)
    transitions["transition_count"] = transitions["transition_count"].astype(int)

except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
    st.error(f"Unable to load the project analysis files: {exc}")
    st.stop()


# ============================================================
# 4. HELPER FUNCTIONS
# ============================================================

def section_title(title, subtitle=None):
    st.markdown(f'<div class="section-heading">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(
            f'<div class="section-subtitle">{subtitle}</div>',
            unsafe_allow_html=True,
        )


def insight_card(label, value, detail=""):
    st.markdown(
        f"""
        <div class="panel">
            <div class="insight-label">{label}</div>
            <div class="insight-value">{value}</div>
            <div class="insight-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def style_plot(fig, height=370):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="DM Sans, sans-serif",
            color=TEXT,
            size=11,
        ),
        height=height,
        margin=dict(l=15, r=18, t=28, b=15),
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=MUTED),
        ),
        hoverlabel=dict(
            bgcolor=PANEL_LIGHT,
            bordercolor=BORDER,
            font=dict(color=TEXT),
        ),
    )

    fig.update_xaxes(
        gridcolor="rgba(145,164,187,.12)",
        zerolinecolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
    )
    fig.update_yaxes(
        gridcolor="rgba(145,164,187,.10)",
        zerolinecolor=BORDER,
        linecolor=BORDER,
        tickfont=dict(color=MUTED),
    )
    return fig


def transition_label(df):
    return df["from_activity"] + " → " + df["to_activity"]


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown(
        f"""
        <div style="padding: 4px 4px 22px;">
            <div style="display:flex;align-items:center;gap:11px;">
                <div style="
                    background:linear-gradient(135deg,{TEAL},{CYAN});
                    width:42px;height:42px;border-radius:12px;
                    display:flex;align-items:center;justify-content:center;
                    color:#071521;font-size:22px;font-weight:800;">
                    C
                </div>
                <div>
                    <div style="font-size:1.15rem;font-weight:700;color:{TEXT};
                                font-family:'Space Grotesk',sans-serif;">
                        CareFlow
                    </div>
                    <div style="font-size:.69rem;color:{MUTED};">
                        CLINICAL INTELLIGENCE
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="eyebrow">WORKSPACE</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Activity Explorer",
            "Pathway Explorer",
            "Bottleneck Intelligence",
            "Data Quality",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div style="padding:4px 2px 10px;">
            <div style="font-size:.72rem;color:{MUTED};margin-bottom:8px;">
                DATASET STATUS
            </div>
            <span class="status-pill">● {quality.get("status", "UNKNOWN")}</span>
            <div style="margin-top:13px;font-size:.77rem;color:{MUTED};line-height:1.8;">
                Simulated hospital event log<br>
                {int(quality.get("unique_cases", 0)):,} cases ·
                {int(quality.get("total_events", 0)):,} events
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("CareFlow · Process Mining")
    st.caption("Data Engineering & Analytics")


# ============================================================
# 6. PAGE HEADER
# ============================================================

page_details = {
    "Executive Overview": (
        "Clinical Pathway Intelligence",
        "A unified view of hospital activity, transition patterns, and event-log quality.",
    ),
    "Activity Explorer": (
        "Activity Explorer",
        "Understand which activities appear in the hospital event log and how frequently.",
    ),
    "Pathway Explorer": (
        "Clinical Pathway Explorer",
        "Explore the observed connections between activities using transition counts.",
    ),
    "Bottleneck Intelligence": (
        "Bottleneck Intelligence",
        "Investigate transitions with higher elapsed durations to identify opportunities for review.",
    ),
    "Data Quality": (
        "Data Quality & Validation",
        "Review the event log validation results and confirm the reliability checks performed.",
    ),
}

heading, subtitle = page_details[page]

st.markdown(
    f"""
    <div class="hero">
        <div class="eyebrow">CAREFLOW / ANALYTICS WORKSPACE</div>
        <div class="hero-title">{heading}</div>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown("### Operational Snapshot")
    st.caption("Metrics calculated from the generated project analysis files.")

    total_events = int(quality.get("total_events", 0))
    unique_cases = int(quality.get("unique_cases", 0))
    unique_activities = int(quality.get("unique_activities", len(activities)))
    status = str(quality.get("status", "UNKNOWN"))

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Events", f"{total_events:,}")
    c2.metric("Cases Analysed", f"{unique_cases:,}")
    c3.metric("Unique Activities", f"{unique_activities:,}")
    c4.metric("Validation", status)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    left, right = st.columns([1.15, 1])

    with left:
        section_title(
            "Activity Distribution",
            "Recorded event count for each hospital activity.",
        )

        act = activities.sort_values("event_count", ascending=True)

        fig = px.bar(
            act,
            x="event_count",
            y="Activity_Name",
            orientation="h",
            text="event_count",
            color="event_count",
            color_continuous_scale=[
                [0, "#164E63"],
                [0.55, TEAL],
                [1, CYAN],
            ],
            labels={
                "event_count": "Recorded Events",
                "Activity_Name": "Activity",
            },
        )
        fig.update_traces(
            textposition="outside",
            textfont=dict(color=TEXT, size=10),
            marker_line_width=0,
            hovertemplate="<b>%{y}</b><br>Events: %{x:,}<extra></extra>",
        )
        fig.update_layout(
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Events",
        )
        st.plotly_chart(
            style_plot(fig, 390),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    with right:
        section_title(
            "Transitions to Investigate",
            "Ranked by average elapsed time between recorded activities.",
        )

        ranked = transitions.sort_values(
            "average_time_minutes", ascending=False
        ).head(6).copy()
        ranked["Transition"] = transition_label(ranked)

        fig = px.bar(
            ranked.sort_values("average_time_minutes", ascending=True),
            x="average_time_minutes",
            y="Transition",
            orientation="h",
            text="average_time_minutes",
            color="average_time_minutes",
            color_continuous_scale=[
                [0, "#164E63"],
                [0.65, TEAL],
                [1, AMBER],
            ],
            labels={
                "average_time_minutes": "Average Minutes",
                "Transition": "Transition",
            },
        )
        fig.update_traces(
            texttemplate="%{x:.2f} min",
            textposition="outside",
            textfont=dict(color=TEXT, size=10),
            hovertemplate="<b>%{y}</b><br>Average: %{x:.2f} min<extra></extra>",
        )
        fig.update_layout(
            coloraxis_showscale=False,
            yaxis_title="",
            xaxis_title="Average elapsed time (minutes)",
        )
        st.plotly_chart(
            style_plot(fig, 390),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    st.markdown("### Key Findings")

    highest_activity = activities.loc[activities["event_count"].idxmax()]
    longest_transition = transitions.loc[
        transitions["average_time_minutes"].idxmax()
    ]
    max_repeat = activities.loc[
        activities["Activity_Name"] == "Repeat Lab Test",
        "event_count",
    ]

    a, b, c = st.columns(3)

    with a:
        insight_card(
            "Most Recorded Activity",
            str(highest_activity["Activity_Name"]),
            f"{int(highest_activity['event_count']):,} recorded events",
        )

    with b:
        insight_card(
            "Highest Average Transition",
            f"{longest_transition['average_time_minutes']:.2f} min",
            f"{longest_transition['from_activity']} → "
            f"{longest_transition['to_activity']}",
        )

    with c:
        if len(max_repeat):
            repeat_count = int(max_repeat.iloc[0])
            insight_card(
                "Repeat Lab Test Events",
                f"{repeat_count:,}",
                "Worth examining alongside lab-result and pathway context.",
            )
        else:
            insight_card(
                "Transition Records",
                f"{len(transitions):,}",
                "Transitions available for analysis.",
            )

    st.markdown("### Event Log Quality")

    missing_total = sum(
        int(v) for v in quality.get("missing_values", {}).values()
    )
    duplicate_total = int(quality.get("duplicate_events", 0))
    invalid_total = int(quality.get("invalid_timestamps", 0))
    chronology_total = int(quality.get("chronological_violations", 0))

    q1, q2, q3, q4 = st.columns(4)
    q1.metric("Missing Required Values", f"{missing_total:,}")
    q2.metric("Duplicate Events", f"{duplicate_total:,}")
    q3.metric("Invalid Timestamps", f"{invalid_total:,}")
    q4.metric("Chronology Violations", f"{chronology_total:,}")

    st.caption(
        "Transition durations are elapsed times between recorded events. "
        "They should not automatically be interpreted as confirmed waiting times."
    )


# ============================================================
# 8. ACTIVITY EXPLORER
# ============================================================

elif page == "Activity Explorer":

    section_title(
        "Explore Activity Frequency",
        "Filter the observed activity counts and compare their distribution.",
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        query = st.text_input(
            "Search activity",
            placeholder="e.g. Lab, Treatment, Discharge",
        )

    with col2:
        sort_order = st.selectbox(
            "Sort activities",
            ["Highest count first", "Lowest count first", "Alphabetical"],
        )

    filtered = activities.copy()

    if query.strip():
        filtered = filtered[
            filtered["Activity_Name"].str.contains(
                query.strip(), case=False, na=False
            )
        ]

    if sort_order == "Highest count first":
        filtered = filtered.sort_values("event_count", ascending=False)
    elif sort_order == "Lowest count first":
        filtered = filtered.sort_values("event_count", ascending=True)
    else:
        filtered = filtered.sort_values("Activity_Name")

    a, b = st.columns(2)
    a.metric("Activities Displayed", len(filtered))
    b.metric(
        "Events in Displayed Activities",
        f"{int(filtered['event_count'].sum()):,}",
    )

    if filtered.empty:
        st.warning("No activities match your search.")
    else:
        left, right = st.columns([1.2, 1])

        with left:
            fig = px.bar(
                filtered.sort_values("event_count"),
                x="event_count",
                y="Activity_Name",
                orientation="h",
                text="event_count",
                color="event_count",
                color_continuous_scale=["#164E63", TEAL, CYAN],
                labels={
                    "event_count": "Event Count",
                    "Activity_Name": "Activity",
                },
            )
            fig.update_traces(
                textposition="outside",
                textfont=dict(color=TEXT),
            )
            fig.update_layout(coloraxis_showscale=False, yaxis_title="")
            st.plotly_chart(
                style_plot(fig, max(330, 42 * len(filtered) + 100)),
                use_container_width=True,
            )

        with right:
            fig = px.pie(
                filtered,
                names="Activity_Name",
                values="event_count",
                hole=0.67,
                color_discrete_sequence=[
                    TEAL, CYAN, PURPLE, AMBER,
                    "#60A5FA", "#F472B6", "#A3E635", "#818CF8",
                ],
            )
            fig.update_traces(
                textposition="outside",
                textinfo="percent",
                marker=dict(line=dict(color=BG, width=3)),
                hovertemplate="%{label}<br>Events: %{value:,}<br>Share: %{percent}<extra></extra>",
            )
            fig.update_layout(
                annotations=[
                    dict(
                        text=f"{int(filtered['event_count'].sum()):,}<br><sup>events</sup>",
                        x=0.5,
                        y=0.5,
                        font=dict(size=22, color=TEXT),
                        showarrow=False,
                    )
                ],
                showlegend=True,
                legend=dict(orientation="h", y=-0.13),
            )
            st.plotly_chart(
                style_plot(fig, 390),
                use_container_width=True,
            )

        section_title("Activity Records", "Counts from the generated activity summary.")

        st.dataframe(
            filtered.rename(
                columns={
                    "Activity_Name": "Activity",
                    "event_count": "Event Count",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download filtered activity data",
            data=filtered.to_csv(index=False).encode("utf-8"),
            file_name="careflow_activity_analysis.csv",
            mime="text/csv",
        )


# ============================================================
# 9. CLINICAL PATHWAY EXPLORER
# ============================================================

elif page == "Pathway Explorer":

    section_title(
        "Observed Activity Connections",
        "The diagram is constructed from the transition summary supplied to the dashboard.",
    )

    st.info(
        "This is an observed transition-flow view, not a reconstruction of every "
        "individual patient's complete journey. Link widths represent transition "
        "counts in the summary file."
    )

    path_data = transitions.copy()

    minimum_count = int(path_data["transition_count"].min())
    maximum_count = int(path_data["transition_count"].max())

    min_transition_count = st.slider(
        "Minimum transition count",
        min_value=minimum_count,
        max_value=maximum_count,
        value=minimum_count,
    )

    path_data = path_data[
        path_data["transition_count"] >= min_transition_count
    ].copy()

    if path_data.empty:
        st.warning("No transitions meet this filter.")
    else:
        nodes = sorted(
            set(path_data["from_activity"].astype(str))
            | set(path_data["to_activity"].astype(str))
        )
        node_index = {name: i for i, name in enumerate(nodes)}

        node_colors = [
            TEAL if "Registration" in n
            else CYAN if "Discharge" in n
            else PURPLE if "Lab" in n
            else "#60A5FA" if "Doctor" in n
            else AMBER if "Treatment" in n
            else "#64748B"
            for n in nodes
        ]

        fig = go.Figure(
            data=[
                go.Sankey(
                    arrangement="snap",
                    node=dict(
                        pad=24,
                        thickness=19,
                        line=dict(color=BORDER, width=1),
                        label=nodes,
                        color=node_colors,
                        hovertemplate="%{label}<extra></extra>",
                    ),
                    link=dict(
                        source=[
                            node_index[str(x)]
                            for x in path_data["from_activity"]
                        ],
                        target=[
                            node_index[str(x)]
                            for x in path_data["to_activity"]
                        ],
                        value=path_data["transition_count"].tolist(),
                        customdata=path_data[
                            [
                                "average_time_minutes",
                                "median_time_minutes",
                                "maximum_time_minutes",
                            ]
                        ].to_numpy(),
                        color="rgba(45,212,191,0.25)",
                        hovertemplate=(
                            "%{source.label} → %{target.label}"
                            "<br>Transitions: %{value:,}"
                            "<br>Average duration: %{customdata[0]:.2f} min"
                            "<br>Median duration: %{customdata[1]:.2f} min"
                            "<br>Maximum duration: %{customdata[2]:.2f} min"
                            "<extra></extra>"
                        ),
                    ),
                )
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color=TEXT, size=11),
            height=550,
            margin=dict(l=15, r=15, t=25, b=15),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        section_title(
            "Transition Register",
            "Filter and inspect the links used in the flow diagram.",
        )

        show_cols = [
            "from_activity",
            "to_activity",
            "transition_count",
            "average_time_minutes",
            "median_time_minutes",
            "maximum_time_minutes",
        ]

        st.dataframe(
            path_data[show_cols].sort_values(
                "transition_count", ascending=False
            ).rename(
                columns={
                    "from_activity": "From Activity",
                    "to_activity": "To Activity",
                    "transition_count": "Transition Count",
                    "average_time_minutes": "Average (min)",
                    "median_time_minutes": "Median (min)",
                    "maximum_time_minutes": "Maximum (min)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# 10. BOTTLENECK INTELLIGENCE
# ============================================================

elif page == "Bottleneck Intelligence":

    section_title(
        "Transition Duration Analysis",
        "Compare transition durations and prioritize records for further investigation.",
    )

    metric = st.selectbox(
        "Duration metric",
        [
            "average_time_minutes",
            "median_time_minutes",
            "maximum_time_minutes",
        ],
        format_func=lambda value: {
            "average_time_minutes": "Average duration",
            "median_time_minutes": "Median duration",
            "maximum_time_minutes": "Maximum duration",
        }[value],
    )

    left, right = st.columns([1, 1])

    with left:
        minimum_count = st.number_input(
            "Minimum transition count",
            min_value=0,
            max_value=int(transitions["transition_count"].max()),
            value=0,
            step=10,
        )

    with right:
        top_n = st.slider(
            "Number of transitions",
            min_value=3,
            max_value=max(3, min(10, len(transitions))),
            value=min(10, len(transitions)),
        )

    filtered = transitions[
        transitions["transition_count"] >= minimum_count
    ].copy()

    if filtered.empty:
        st.warning("No transitions match these filters.")
    else:
        filtered["Transition"] = transition_label(filtered)
        ranked = filtered.sort_values(metric, ascending=False).head(top_n)

        first, second, third = st.columns(3)

        highest_average = filtered.loc[
            filtered["average_time_minutes"].idxmax()
        ]
        highest_median = filtered.loc[
            filtered["median_time_minutes"].idxmax()
        ]
        highest_maximum = filtered.loc[
            filtered["maximum_time_minutes"].idxmax()
        ]

        first.metric(
            "Highest Average",
            f"{highest_average['average_time_minutes']:.2f} min",
        )
        second.metric(
            "Highest Median",
            f"{highest_median['median_time_minutes']:.2f} min",
        )
        third.metric(
            "Highest Maximum",
            f"{highest_maximum['maximum_time_minutes']:.2f} min",
        )

        fig = px.bar(
            ranked.sort_values(metric, ascending=True),
            x=metric,
            y="Transition",
            orientation="h",
            color=metric,
            text=metric,
            color_continuous_scale=["#164E63", TEAL, AMBER],
            hover_data=["transition_count"],
            labels={
                metric: "Duration (minutes)",
                "Transition": "Activity Transition",
                "transition_count": "Transition Count",
            },
        )
        fig.update_traces(
            texttemplate="%{x:.2f}",
            textposition="outside",
            textfont=dict(color=TEXT, size=10),
            hovertemplate=(
                "<b>%{y}</b><br>Duration: %{x:.2f} minutes"
                "<br>Transition count: %{customdata[0]:,}<extra></extra>"
            ),
        )
        fig.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Elapsed duration (minutes)",
            yaxis_title="",
        )

        st.plotly_chart(
            style_plot(fig, max(390, 42 * len(ranked) + 100)),
            use_container_width=True,
        )

        section_title(
            "Compare Average, Median and Maximum",
            "Select transitions to compare their recorded durations.",
        )

        available = ranked["Transition"].tolist()
        selected = st.multiselect(
            "Transitions to compare",
            options=available,
            default=available[: min(5, len(available))],
        )

        compare = ranked[ranked["Transition"].isin(selected)]

        if not compare.empty:
            long_data = compare.melt(
                id_vars=["Transition", "transition_count"],
                value_vars=[
                    "average_time_minutes",
                    "median_time_minutes",
                    "maximum_time_minutes",
                ],
                var_name="Duration Type",
                value_name="Minutes",
            )

            long_data["Duration Type"] = long_data["Duration Type"].map(
                {
                    "average_time_minutes": "Average",
                    "median_time_minutes": "Median",
                    "maximum_time_minutes": "Maximum",
                }
            )

            fig = px.bar(
                long_data,
                x="Transition",
                y="Minutes",
                color="Duration Type",
                barmode="group",
                color_discrete_map={
                    "Average": TEAL,
                    "Median": CYAN,
                    "Maximum": AMBER,
                },
                hover_data=["transition_count"],
            )
            fig.update_layout(
                xaxis_title="Transition",
                yaxis_title="Elapsed time (minutes)",
                xaxis_tickangle=-25,
            )

            st.plotly_chart(
                style_plot(fig, 430),
                use_container_width=True,
            )

        section_title("Detailed Transition Data")

        table = filtered.sort_values(metric, ascending=False).copy()
        table["Transition"] = transition_label(table)

        display_cols = [
            "Transition",
            "transition_count",
            "average_time_minutes",
            "median_time_minutes",
            "maximum_time_minutes",
        ]

        st.dataframe(
            table[display_cols].rename(
                columns={
                    "transition_count": "Transition Count",
                    "average_time_minutes": "Average (min)",
                    "median_time_minutes": "Median (min)",
                    "maximum_time_minutes": "Maximum (min)",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download transition analysis",
            data=table[display_cols].to_csv(index=False).encode("utf-8"),
            file_name="careflow_transition_analysis.csv",
            mime="text/csv",
        )

        st.caption(
            "Interpretation note: long elapsed durations are investigation signals, "
            "not proof of a clinical bottleneck. Validate the context before "
            "recommending operational changes."
        )


# ============================================================
# 11. DATA QUALITY
# ============================================================

elif page == "Data Quality":

    section_title(
        "Event Log Validation",
        "Results loaded from the pipeline-generated quality report.",
    )

    status = str(quality.get("status", "UNKNOWN")).upper()

    if status == "PASSED":
        st.success("The generated quality report indicates that validation passed.")
    else:
        st.warning(f"Reported validation status: {status}")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Events",
        f"{int(quality.get('total_events', 0)):,}",
    )
    c2.metric(
        "Unique Cases",
        f"{int(quality.get('unique_cases', 0)):,}",
    )
    c3.metric(
        "Unique Activities",
        f"{int(quality.get('unique_activities', 0)):,}",
    )
    c4.metric(
        "Duplicate Events",
        f"{int(quality.get('duplicate_events', 0)):,}",
    )

    st.markdown("### Validation Checks")

    missing_values = quality.get("missing_values", {})
    checks = [
        {
            "Check": f"Missing values — {col}",
            "Result": "PASS" if int(value) == 0 else "CHECK",
            "Count": int(value),
        }
        for col, value in missing_values.items()
    ]

    checks.extend(
        [
            {
                "Check": "Duplicate events",
                "Result": "PASS"
                if int(quality.get("duplicate_events", 0)) == 0
                else "CHECK",
                "Count": int(quality.get("duplicate_events", 0)),
            },
            {
                "Check": "Invalid timestamps",
                "Result": "PASS"
                if int(quality.get("invalid_timestamps", 0)) == 0
                else "CHECK",
                "Count": int(quality.get("invalid_timestamps", 0)),
            },
            {
                "Check": "Chronological violations",
                "Result": "PASS"
                if int(quality.get("chronological_violations", 0)) == 0
                else "CHECK",
                "Count": int(quality.get("chronological_violations", 0)),
            },
        ]
    )

    check_df = pd.DataFrame(checks)

    def quality_color(value):
        if value == "PASS":
            return f"color: {TEAL}; font-weight: 700"
        return f"color: {AMBER}; font-weight: 700"

    st.dataframe(
        check_df.style.map(quality_color, subset=["Result"]),
        use_container_width=True,
        hide_index=True,
    )

    left, right = st.columns([1, 1])

    with left:
        section_title("Activity Summary")
        st.dataframe(
            activities.sort_values("event_count", ascending=False).rename(
                columns={
                    "Activity_Name": "Activity",
                    "event_count": "Events",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    with right:
        section_title("Report Information")
        input_file = str(quality.get("input_file", "Not specified"))

        st.markdown(
            f"""
            <div class="panel">
                <div class="insight-label">Reported status</div>
                <div class="insight-value">{status}</div>
                <div class="insight-detail">
                    Source: pipeline-generated data quality report.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_input(
            "Input dataset path",
            value=input_file,
            disabled=True,
        )

        st.download_button(
            "Download quality report (JSON)",
            data=json.dumps(quality, indent=2).encode("utf-8"),
            file_name="careflow_data_quality_report.json",
            mime="application/json",
        )

    with st.expander("View raw quality report"):
        st.json(quality)


# ============================================================
# 12. FOOTER
# ============================================================

st.markdown(
    f"""
    <div class="footer">
        <b style="color:{TEXT};">CAREFLOW</b>
        &nbsp; · &nbsp; Clinical Pathway Process Mining<br>
        Analytics interface powered by Streamlit and Plotly.<br>
        All displayed figures are sourced from the project's generated analysis files.
        This dashboard supports investigation and does not replace clinical judgement.
    </div>
    """,
    unsafe_allow_html=True,
)
