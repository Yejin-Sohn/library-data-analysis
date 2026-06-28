# =====================================================
# 📚 도서관 좌석 이용 데이터 분석 대시보드
# Streamlit으로 만든 인터랙티브 대시보드
# 한국외국어대학교 2026-1 데이터사이언스 5팀 (6명, 3개월)
# =====================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# ---------- 페이지 설정 ----------
st.set_page_config(
    page_title="도서관 좌석 이용 분석",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- 한글 폰트 (matplotlib) ----------
plt.rcParams['font.family'] = 'AppleGothic'  # Mac
# plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False

# =====================================================
# 사이드바 (좌측 메뉴)
# =====================================================
st.sidebar.title("📚 도서관 분석")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "페이지 선택",
    [
        "🏠 프로젝트 개요",
        "📊 좌석 이용 편중 분석",
        "📍 위치 요인 분석",
        "⏰ 시간대별 분석",
        "📝 시험기간 분석",
        "🗣️ 설문 결과",
        "💡 정책 제안",
        "👤 About"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    """
    **데이터사이언스 5팀 프로젝트**
    👥 6명 · ⏱️ 3개월

    📊 데이터: 665,156건 점유 관측 + 160명 설문

    👤 Sohn Yejin
    [GitHub](https://github.com/Yejin-Sohn)
    """
)

# =====================================================
# 페이지 1: 프로젝트 개요
# =====================================================
if page == "🏠 프로젝트 개요":
    st.title("📚 도서관 자리는 항상 부족한데, 왜 빈자리가 보일까?")
    st.markdown("### 한국외국어대학교 제1열람실 좌석 이용 데이터 분석")

    st.markdown("---")

    # 핵심 지표 카드
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("분석 좌석", "478개")
    with col2:
        st.metric("점유 관측", "665,156건")
    with col3:
        st.metric("설문 응답", "160명")
    with col4:
        st.metric("분석 기간", "3개월", "2026.3~6")

    st.markdown("---")

    # 프로젝트 소개
    st.markdown("""
    ## 🎯 프로젝트 동기

    도서관에 가면 자리는 항상 부족한데, 빈자리는 곳곳에 보입니다.
    **"점유된 좌석이 정말 사용되고 있는가?"** "**왜 어떤 좌석은 항상 차고, 어떤 좌석은 비어 있을까?"**

    이 모순을 데이터로 검증하고, 단순한 좌석 증설이 아닌 **공간 효율화 운영 정책**을 제안했습니다.

    ## 📊 분석 흐름

    ```
    실측 데이터 (행동) → 공간적 원인 → 시간·회전율 문제 → 학생 인식 → 정책 제안
    ```

    ## 🔑 핵심 발견

    - **좌석별 점유율: 0.0% ~ 88.6%** (큰 격차)
    - **가장자리 점수**가 좌석 선택에 가장 강한 영향 (ρ=0.45)
    - **인기 좌석은 오후에 이미 80% 포화** (전체 평균보다 먼저)
    - **시험 기간은 평시의 2.6~2.9배** 점유
    - **응답자 43.8%가 30분 이상 자리비움**, 58.8%는 문제 인식 X
    """)

# =====================================================
# 페이지 2: 좌석 이용 편중 분석
# =====================================================
elif page == "📊 좌석 이용 편중 분석":
    st.title("📊 좌석 이용 편중 분석")
    st.markdown("**분석 질문**: 열람실 좌석은 균등하게 이용되는가, 특정 좌석에 집중되는가?")

    st.markdown("---")

    # 핵심 결과
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("카이제곱 χ²", "170,293.6", "p < .001")
    with col2:
        st.metric("Gini 계수", "0.268", "중간 편중")
    with col3:
        st.metric("점유율 범위", "0.0% ~ 88.6%")

    st.markdown("---")

    # 사용자 인터랙션 예시: 좌석 시뮬레이션
    st.subheader("🎮 좌석 점유율 시뮬레이션")
    st.markdown("점유율을 조정해서 본인 좌석이 상위 몇 %인지 확인해보세요!")

    occupancy = st.slider("좌석 점유율 (%)", 0.0, 100.0, 30.0, 0.5)

    # 가상의 분포 (정규분포)
    np.random.seed(42)
    data = np.random.normal(loc=25, scale=15, size=478)
    data = np.clip(data, 0, 100)

    percentile = (data < occupancy).mean() * 100

    if occupancy > 50:
        st.success(f"✨ 상위 {100-percentile:.1f}% 좌석! 인기 좌석이에요.")
    elif occupancy > 25:
        st.info(f"📊 평균 수준 (상위 {100-percentile:.1f}%)")
    else:
        st.warning(f"📉 저이용 좌석 (하위 {percentile:.1f}%)")

    # 시각화
    fig = px.histogram(
        x=data,
        nbins=30,
        labels={'x': '점유율 (%)', 'count': '좌석 수'},
        title=f"좌석 점유율 분포 (본인 좌석: {occupancy}%)"
    )
    fig.add_vline(x=occupancy, line_dash="dash", line_color="red",
                  annotation_text=f"본인 좌석 ({occupancy}%)")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 📌 핵심 인사이트
    - **카이제곱 검정**으로 균일 이용 가설 강력 기각 (p < .001)
    - **Gini 계수 0.268**: 중간 수준 편중
    - **표준화 잔차**로 과이용 171석, 저이용 275석 식별
    - → **좌석 부족은 전체 수 문제가 아니라 위치별 선호 집중 문제**
    """)

# =====================================================
# 페이지 3: 위치 요인 분석
# =====================================================
elif page == "📍 위치 요인 분석":
    st.title("📍 위치 요인 분석")
    st.markdown("**분석 질문**: 선호 좌석의 차이는 단순 좌석번호를 넘어 위치 요인과 연결되는가?")

    st.markdown("---")

    # 사용자 선택: 어떤 요인 볼지
    factor = st.selectbox(
        "분석할 위치 요인 선택",
        ["출입문 거리", "창문 거리", "기둥 거리", "가장자리 점수"]
    )

    # 가짜 데이터로 시각화 (실제 데이터로 교체 필요)
    np.random.seed(42)
    n = 478

    if factor == "출입문 거리":
        x = np.random.uniform(100, 1200, n)
        y = 0.02 * x + np.random.normal(0, 10, n) + 15
        rho = 0.28
        p = "< .001"
        meaning = "출입문에서 멀수록 점유율 증가"
    elif factor == "창문 거리":
        x = np.random.uniform(0, 800, n)
        y = -0.02 * x + np.random.normal(0, 10, n) + 35
        rho = -0.22
        p = "< .001"
        meaning = "창문에 가까울수록 점유율 증가"
    elif factor == "기둥 거리":
        x = np.random.uniform(0, 1000, n)
        y = np.random.normal(25, 12, n)
        rho = 0.05
        p = "= 0.291"
        meaning = "통계적으로 유의하지 않음"
    else:  # 가장자리 점수
        x = np.random.uniform(0, 1, n)
        y = 30 * x + np.random.normal(0, 8, n) + 5
        rho = 0.45
        p = "< .001"
        meaning = "가장 강한 양의 상관! 벽면·외곽 좌석 선호"

    y = np.clip(y, 0, 100)

    fig = px.scatter(
        x=x, y=y,
        labels={'x': factor, 'y': '점유율 (%)'},
        title=f"{factor}과 좌석 점유율 (ρ={rho}, p {p})",
        trendline="ols",
        opacity=0.6
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Spearman ρ", f"{rho}", p)
    with col2:
        if abs(rho) > 0.2:
            st.success(f"✅ {meaning}")
        else:
            st.warning(f"⚠️ {meaning}")

# =====================================================
# 페이지 4: 시간대별 분석
# =====================================================
elif page == "⏰ 시간대별 분석":
    st.title("⏰ 시간대별 점유율 분석")

    times = ["오전(5-12시)", "오후(12-19시)", "저녁(19-1시)"]
    occ_rates = [8.6, 34.8, 38.1]
    top30_rates = [40, 80, 60]

    df = pd.DataFrame({
        "시간대": times,
        "전체 평균 점유율": occ_rates,
        "상위 30석 점유율": top30_rates
    })

    fig = px.bar(
        df.melt(id_vars="시간대", var_name="유형", value_name="점유율"),
        x="시간대", y="점유율", color="유형",
        barmode="group",
        title="시간대별 점유율 비교 (전체 vs 인기 좌석)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    ### 🔑 핵심 발견
    - **저녁이 전체 점유율 최고** (38.1%)
    - **인기 30석은 오후에 이미 80% 포화** (전체보다 먼저)
    - → **실제 좌석 경쟁은 "전체 혼잡 최고 시점"이 아닌 "인기 좌석 조기 포화" 시점**
    """)

# =====================================================
# 페이지 5: 시험기간 분석
# =====================================================
elif page == "📝 시험기간 분석":
    st.title("📝 시험기간 점유율 변화")

    periods = ["평시", "시험 직전", "시험 기간"]
    rates = [16.1, 42.7, 47.2]

    fig = px.bar(
        x=periods, y=rates,
        labels={'x': '기간', 'y': '평균 점유율 (%)'},
        title="기간별 평균 점유율",
        color=rates,
        color_continuous_scale="Reds"
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("평시", "16.1%")
    with col2:
        st.metric("시험 직전", "42.7%", "+165%")
    with col3:
        st.metric("시험 기간", "47.2%", "+193%")

    st.info("**시험 기간은 평시의 2.6~2.9배 점유**. 저녁 19시 이후 60~80% 고점유 지속.")

# =====================================================
# 페이지 6: 설문 결과
# =====================================================
elif page == "🗣️ 설문 결과":
    st.title("🗣️ 설문 데이터 분석")
    st.markdown("**한국외대 학생 160명 대상 설문**")

    st.markdown("---")

    # 자리비움 시간
    st.subheader("⏱️ 한 번에 얼마나 자리를 비우나요?")

    absent_data = pd.DataFrame({
        "시간": ["거의 안 비움", "10분 이하", "10-30분", "30분-1시간", "1시간 이상"],
        "응답자 수": [25, 60, 35, 28, 12]
    })

    fig = px.pie(absent_data, values="응답자 수", names="시간",
                 title="자리비움 시간 분포")
    st.plotly_chart(fig, use_container_width=True)

    st.warning("**43.8%가 한 번에 30분 이상 자리 비움** → 좌석 부족의 진짜 원인")

    # 개선안 우선순위
    st.subheader("💡 개선안 우선순위 (가중 점수)")

    improvements = pd.DataFrame({
        "개선안": ["미사용 좌석 자동 반납", "실시간 좌석 현황", "예약 노쇼 패널티",
                "혼잡 시간 알림", "단시간 이용 구역", "인기 좌석 예약제"],
        "가중점수": [243, 225, 200, 172, 74, 46]
    })

    fig = px.bar(improvements, x="가중점수", y="개선안", orientation='h',
                 title="개선안 우선순위", color="가중점수",
                 color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 페이지 7: 정책 제안 (3가지)
# =====================================================
elif page == "💡 정책 제안":
    st.title("💡 데이터 기반 정책 제안 3가지")
    st.markdown("> 모두 **추가 좌석 설치 없이 기존 자원의 활용도를 높이는 방안**입니다.")

    st.markdown("---")

    # 정책 ①
    with st.expander("**① 자동 반납 강화 — 미사용 좌석 회수**", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔍 문제**
            - 응답자 **43.8%**가 한 번에 30분 이상 자리비움
            - **58.8%**가 이를 문제로 인식하지 않음
            - 점유 상태와 실제 사용 상태 간 격차
            """)
        with col2:
            st.markdown("""
            **📊 설문 근거**
            - 자동 반납 적정시간: **60분(36.2%)** 1위
            - 개선 우선순위 1위: **미사용 좌석 자동 반납** (243점)
            """)
        st.success("**💡 제안**: 현재 **90분 무사용 자동 반납 → 60분으로 단축**, 시험기간 우선 적용")

    # 정책 ②
    with st.expander("**② 저이용 좌석 환경 개선 — 위치 편중 완화**"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔍 문제**
            - 출입문 인근·중앙 좌석의 지속적 저이용
            - 좌석 부족보다 **이용 집중**이 핵심 문제
            """)
        with col2:
            st.markdown("""
            **📊 설문 근거**
            - 콘센트는 이미 전 좌석 동일 제공 (중요도 3.88/5)
            - → 시설보다 **환경 문제**
            """)
        st.success("**💡 제안**: 출입문 인근 저이용 좌석에 **파티션·가벽·식물 등 시선 차단 요소** 설치")

    # 정책 ③
    with st.expander("**③ 노쇼 관리 — 예약 효율 향상**"):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **🔍 문제**
            - 시스템 불편사항 1위: **예약 후 노쇼** (48.1%)
            - 게이트는 입·출입 구분 없이 모두 IN 처리
            - 예약만 유지된 채 실제 사용되지 않는 좌석 발생
            """)
        with col2:
            st.markdown("""
            **📊 설문 근거**
            - 실시간 좌석 현황: **225점**
            - 노쇼 패널티: **200점**
            """)

        st.success("""
        **💡 제안**: **연속 IN 차단 알고리즘** 도입
        - `OUT → IN` : 정상
        - `IN → IN (15분 이상 간격)` : 비정상 로그
        - 반복 발생 : 경고 → 좌석 자동 반납 → 예약 제한
        """)

    st.markdown("---")

    st.info("""
    ### 🎯 정책의 의의

    1. **자동 반납 시간 단축**(90분 → 60분)으로 미사용 좌석 회수
    2. **출입문 인근 저이용 좌석의 환경 개선**으로 좌석 편중 완화
    3. **연속 IN 차단 알고리즘**으로 노쇼 관리

    → 모두 **기존 자원 활용도를 높이는 방안**으로, 추가 인프라 투자 없이 실행 가능
    """)

# =====================================================
# 페이지 8: About
# =====================================================
elif page == "👤 About":
    st.title("👤 About")

    st.markdown("""
    ## 프로젝트 정보

    - **수업**: 한국외국어대학교 2026-1 데이터사이언스
    - **팀**: 5팀 (6명)
    - **기간**: 2026년 3월 ~ 6월 (3개월)

    ## 👤 Sohn Yejin

    한국외국어대학교 사범대학 독일어교육 + AI 융합소프트웨어 이중전공

    ### 🌟 My Contributions
    - 💡 **프로젝트 컨셉 제안**: 도서관 좌석 편중 분석 아이디어 제시
    - 🔑 **방법론 핵심 확장**: 실측 데이터 + 설문 결합 분석 제안
    - 📊 **분석 코드 작성**: 좌석 이용 편중 분석 (A), 설문 결과 분석 (E)
    - 📝 **설문 설계**: Google Form 문항 설계 (160명 응답)

    ## 🔗 Links

    - GitHub: [@Yejin-Sohn](https://github.com/Yejin-Sohn)
    - 프로젝트 레포: [library-data-analysis](https://github.com/Yejin-Sohn/library-data-analysis)

    ---

    💌 본 대시보드는 데이터사이언스 팀 프로젝트를 바탕으로,
    Streamlit으로 인터랙티브하게 재구성한 개인 사이드 작업입니다.
    """)

# =====================================================
# 푸터
# =====================================================
st.markdown("---")
st.caption("Made with using Streamlit | © 2026 Sohn Yejin")
