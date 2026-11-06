# --- 화면 7: 감옥 열쇠 퍼즐 (파이프 퍼즐을 풀어야 열쇠를 시도할 수 있다) ---
if st.session_state.step == "prison_key":
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #120c09 !important;
            background-image: none !important;
        }
        .stApp h2, .stApp p, .stApp li {
            color: #f3e9dc !important;
        }
        /* 감옥 화면은 위·아래에 빈 공간 없이 화면을 꽉 채운다.
           페이지 안쪽 여백과, 비어 있는 요소 사이에도 생기는 요소 간격(gap)을 모두 없앤다. */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        [data-testid="stMainBlockContainer"] > [data-testid="stVerticalBlock"] {
            gap: 0 !important;
        }
        /* iframe 은 기본이 글자처럼 놓이는 inline 이라 아래에 글줄 여백(약 8px)이 남아 맨 아래가 스크롤된다. 블록으로 둔다. */
        iframe {
            display: block !important;
            margin-bottom: 0px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 스톱워치: 난이도를 고른 뒤 지금까지 흐른 시간을 게임 화면에 넘겨 준다.
    # 화면 내용(srcdoc)이 다시 실행될 때마다 바뀌면 게임이 처음부터 다시 로드되므로, 한 번만 만들어 둔다.
    if "prison_key_html" not in st.session_state:
        started = st.session_state.get("stopwatch_start", time.monotonic())
        elapsed_ms = max(0, round((time.monotonic() - started) * 1000))
        # 화면에 보이는 스톱워치 합계에는 오답 벌칙 시간이 더해져 있으므로, 퍼즐 크기도 같은 값으로 정한다.
        total_ms = elapsed_ms + st.session_state.get("wrong_answer_count", 0) * WRONG_ANSWER_PENALTY_SECONDS * 1000
        grid_size = pipe_puzzle_grid_size(st.session_state.get("difficulty", 1), total_ms)
        st.session_state.prison_key_html = PRISON_KEY_PUZZLE_HTML.replace(
            "__ELAPSED_BEFORE_MS__", str(elapsed_ms)
        ).replace("__PRISON_CLUE__", html_escape(prison_clue_text())).replace("__GRID_SIZE__", str(grid_size))
    st.iframe(st.session_state.prison_key_html, height=900)

# --- 비밀의 방: 어떤 버튼이든 500분의 1 확률로 누르면 도착하는 화면 ---
elif st.session_state.step == "secret_room":
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(ellipse at 50% 30%, #
