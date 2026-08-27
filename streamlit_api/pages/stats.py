import pandas as pd
import streamlit as st

from api_client import (
    get_team_goal_diff,
    get_top_scorers,
)


st.title("📊 월드컵 통계")


tab1, tab2 = st.tabs(
    [
        "⚽ 득점 선수",
        "🌎 팀 순위",
    ]
)


# -----------------------------
# 득점 상위 선수
# -----------------------------
with tab1:

    st.subheader(
        "90분당 득점 상위 선수"
    )

    limit = st.slider(
        "표시 인원",
        min_value=5,
        max_value=30,
        value=10,
    )

    if st.button(
        "득점 통계 불러오기",
        key="top_scorer_button",
    ):

        try:
            data = get_top_scorers(
                limit=limit
            )

            df = pd.DataFrame(data)

            if df.empty:
                st.warning(
                    "데이터가 없습니다."
                )

            else:
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                if (
                    "player" in df.columns
                    and "goals_per_90"
                    in df.columns
                ):
                    chart_df = (
                        df[
                            [
                                "player",
                                "goals_per_90",
                            ]
                        ]
                        .set_index("player")
                    )

                    st.bar_chart(
                        chart_df
                    )

        except Exception as e:
            st.error(str(e))


# -----------------------------
# 팀 순위
# -----------------------------
with tab2:

    st.subheader(
        "팀별 득실차 / 승점"
    )

    if st.button(
        "팀 통계 불러오기",
        key="team_stats_button",
    ):

        try:
            data = (
                get_team_goal_diff()
            )

            df = pd.DataFrame(data)

            if df.empty:
                st.warning(
                    "데이터가 없습니다."
                )

            else:
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                if (
                    "team" in df.columns
                    and "goal_diff"
                    in df.columns
                ):
                    chart_df = (
                        df[
                            [
                                "team",
                                "goal_diff",
                            ]
                        ]
                        .set_index("team")
                    )

                    st.bar_chart(
                        chart_df
                    )

        except Exception as e:
            st.error(str(e))
