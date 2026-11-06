# --- 화면 7: 감옥 열쇠 퍼즐 (파이프 퍼즐을 풀어야 열쇠를 시도할 수 있다) ---
elif st.session_state.step == "prison_key":
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
                radial-gradient(ellipse at 50% 30%, #4a2a12 0%, #1a0e07 55%, #0a0604 100%) !important;
        }}
        .stApp, .stApp * {{
            font-family: {APP_FONT_FAMILY} !important;
        }}
        .secret-room {{
            max-width: 560px;
            margin: 90px auto 28px auto;
            text-align: center;
            color: #f3e9dc;
        }}
        .secret-room .sr-title {{
            font-size: 34px;
            font-weight: bold;
            letter-spacing: 4px;
            color: #fce080;
            text-shadow: 0 0 22px rgba(252, 224, 128, 0.55);
            margin-bottom: 18px;
            /* 아래 글과의 간격은 그대로 두고, 제목만 위로 올린다. */
            position: relative;
            top: -30px;
        }}
        .secret-room .sr-text {{
            font-size: 17px;
            line-height: 1.8;
            word-break: keep-all;
        }}
        div.stButton > button, div[data-testid="stButton"] > button {{
            background-color: #ffffff !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: 1px solid #cccccc !important;
            border-radius: 8px !important;
        }}
        div.stButton > button:hover, div[data-testid="stButton"] > button:hover {{
            background-color: #e0e0e0 !important;
            color: #000000 !important;
        }}
        /* 돌아가기 버튼은 작게 만들고, 비밀번호를 맞게 넣기 전에는 흐리게 잠가 둔다. */
        .st-key-secret_room_back {{
            align-self: center;
        }}
        div[data-testid="stButton"] > button {{
            width: auto !important;
            min-width: 110px;
            min-height: 32px !important;
            padding: 4px 20px !important;
            font-size: 14px !important;
        }}
        div[data-testid="stButton"] > button:disabled {{
            opacity: 0.35 !important;
            cursor: not-allowed !important;
        }}
        div[data-testid="stTextInput"] {{
            width: 240px;
            max-width: 100%;
            margin: 0 auto;
        }}
        div[data-baseweb="input"] input {{
            text-align: center;
        }}
        button[data-testid="stPasswordInputVisibilityButton"],
        button[aria-label="View password"],
        button[aria-label="Show password"],
        button[aria-label="Hide password"] {{
            display: none !important;
        }}
        </style>
        <div class="secret-room">
            <div class="sr-title">Lucky!</div>
            <div class="sr-text">
                축하합니다. 당신은 1 / 500 (0.2%)을 뚫었습니다.<br>
                현재 부스에 있는 운영팀에게 이 사실을 알려주세요!
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    # 풍선은 도착했을 때 한 번만 날린다. (비밀번호를 넣을 때마다 스크립트가 다시 실행되기 때문)
    if not st.session_state.get("secret_room_celebrated"):
        st.balloons()
        st.session_state.secret_room_celebrated = True

    # 감옥 퍼즐 화면에서 이곳으로 왔다면 돌아갈 때 게임이 새로 로드되므로, 그때의 스톱워치 값을 다시 만든다.
    st.session_state.pop("prison_key_html", None)

    # 비밀의 방 안의 버튼은 다시 주사위를 굴리지 않는 일반 버튼이다.
    # 돌아가기 버튼은 비밀번호를 맞게 넣어야 눌린다. (Enter 를 눌러야 입력이 반영된다.)
    secret_pw = st.text_input(
        "비밀번호",
        type="password",
        key="secret_room_pw",
        label_visibility="collapsed",
        placeholder="비밀번호 입력 후 Enter",
    )
    secret_unlocked = secret_pw == SECRET_ROOM_PASSWORD
    if secret_pw and not secret_unlocked:
        st.error("비밀번호가 맞지 않아요. 운영팀에게 문의해 주세요.")
    if st.button(
        "돌아가기" if secret_unlocked else "🔒 돌아가기",
        key="secret_room_back",
        disabled=not secret_unlocked,
    ):
        del st.session_state["secret_room_pw"]
        st.session_state.pop("secret_room_celebrated", None)
        st.session_state.step = st.session_state.get(
            "secret_room_prev_step", "select_grade"
        )
        st.rerun()

# --- 단서 화면: 검은 화면에 단서(녹색 장갑 또는 파란색 시계)를 보여 준 뒤 원래 화면으로 자동 복귀 ---
elif st.session_state.step == "stalker_clue":
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: #000000 !important;
        }}
        .stalker-clue {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            z-index: 999999;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 22px;
            padding: 24px;
            box-sizing: border-box;
            background: #000000;
        }}
        .stalker-clue-count {{
            color: #8a8f98 !important;
            font-family: {APP_FONT_FAMILY} !important;
            font-size: 16px;
            font-weight: bold;
            line-height: 1;
        }}
        .stalker-clue-text {{
            color: #ffffff !important;
            font-family: {APP_FONT_FAMILY} !important;
            font-size: clamp(22px, 6vw, 34px);
            font-weight: bold;
            letter-spacing: 2px;
            line-height: 1.6;
            text-align: center;
            word-break: keep-all;
            text-wrap: balance;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 문장은 그대로 두고 그 아래 숫자만 1초마다 바꿔서 남은 시간(5, 4, 3, 2, 1)을 보여 준다.
    clue_box = st.empty()
    clue_text = html_escape(st.session_state.get("clue_text", STALKER_CLUE_TEXTS["green"]))
    for seconds_left in range(STALKER_CLUE_SECONDS, 0, -1):
        clue_box.markdown(
            '<div class="stalker-clue">'
            f'<span class="stalker-clue-text">{clue_text}</span>'
            f'<span class="stalker-clue-count">{seconds_left}</span>'
            "</div>",
            unsafe_allow_html=True,
        )
        time.sleep(1)

    # 시간이 다 되면 단서를 띄우기 직전의 화면으로 돌아간다.
    # 다음 화면이 그려질 때까지 마지막 숫자 '1' 이 멈춘 채 남아 있지 않도록, 문구부터 지운다.
    clue_box.empty()
    st.session_state.step = st.session_state.get("clue_return_step", "select_problem")
    st.rerun()

# --- 그 외 모든 화면 (중생대 문제 선택 및 풀이 등) ---
else:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: #f4f4f4 !important; /* 이미지 로딩 실패 시 글씨가 보이도록 밝은 배경 설정 */
            background-image: url("https://i.postimg.cc/fyDLcqj7/Agent-Image-A-sw-eeping-cinematic-vista-of-the-Mesozoic-era-at-golden-hour-a-herd-of-long-necked-sa.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
        .stApp p, .stApp span, .stApp div, .stApp markdown {{
            color: #000000 !important;
            font-weight: bold !important;
        }}
        .stApp, .stApp * {{
            font-family: {APP_FONT_FAMILY} !important;
        }}
        div[data-testid="stTextInput"] label {{
            display: none !important;
        }}
        button[data-testid="stPasswordInputVisibilityButton"], 
        button[aria-label="View password"], 
        button[aria-label="Hide password"] {{
            display: none !important;
        }}
        div[data-baseweb="input"] {{
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 1px solid #cccccc !important;
        }}
        div[data-baseweb="input"] input {{
            color: #000000 !important;
            background-color: #ffffff !important;
            font-weight: bold !important;
        }}
        div.stButton > button, 
        div[data-testid="stButton"] > button, 
        button[kind="secondary"] {{
            background-color: #ffffff !important;
            color: #000000 !important;
            font-weight: bold !important;
            border: 1px solid #cccccc !important;
            border-radius: 8px !important;
        }}
        div.stButton > button:hover, 
        div[data-testid="stButton"] > button:hover, 
        button[kind="secondary"]:hover {{
            background-color: #e0e0e0 !important;
            color: #000000 !important;
        }}
        div.stButton > button[kind="primary"], 
        div[data-testid="stButton"] > button[kind="primary"], 
        div.stButton > button[data-testid="baseButton-primary"] {{
            background-color: #66BB6A !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border: none !important;
        }}
        div.stButton > button[kind="primary"]:hover, 
        div[data-testid="stButton"] > button[kind="primary"]:hover, 
        div.stButton > button[data-testid="baseButton-primary"]:hover {{
            background-color: #4CAF50 !important;
            color: #ffffff !important;
        }}
        {READABLE_TEXT_CSS}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- 화면 1: 학년 선택 ---
    if st.session_state.step == "select_grade":
        readable_box(
            "<h2>현재 시대 : 중생대</h2><p>본인의 현재 학년을 선택해주세요.</p>",
            gap_below=True,
        )

        cols = st.columns(2)
        for col, (label, grade) in zip(cols, [("초5 문제", 5), ("초6 문제", 6)]):
            if lucky_button(label, use_container_width=True, dg=col, key=f"grade_{grade}"):
                st.session_state.grade = grade
                st.session_state.pop("fast_pass_cache", None)
                st.session_state.title, st.session_state.problems = (
                    generate_problems(grade, st.session_state.difficulty)
                )
                st.session_state.solved_indices = set()
                reset_stalker_clue()
                st.session_state.step = "select_problem"
                st.rerun()

        st.write("")
        st.write("")
        st.write("")
        st.session_state.is_dev_mode = st.checkbox(
            "개발자 옵션 (정답 및 풀이 확인 기능 켜기)",
            value=st.session_state.is_dev_mode,
        )

    # --- 화면 2: 문제 선택 ---
    elif st.session_state.step == "select_problem":
        readable_box(
            f"<h3>{html_escape(st.session_state.title)}</h3>"
            "<p>3문제를 모두 풀거나, 매우 어려움 문제를 풀면 아래에 버튼이 생깁니다</p>"
        )
        st.markdown("---")

        # 문제 3개 + 따로 떨어진 빨간 '매우 어려움' 문제(고른 학년의 문제) 1개. (이 문제의 정답은 타임머신 암호 1592 다.)
        fast_title, fast_problem = fast_pass_for_grade()
        entries = list(st.session_state.problems) + [fast_problem]

        def solved_card(label, ans, color):
            """풀고 난 문제 칸: 완료 표시와 정답을 보여 주는 흰 카드."""
            st.markdown(
                f"""
                <div style="
                    background-color: rgba(255, 255, 255, 0.85);
                    border: 2px solid {color};
                    border-radius: 10px;
                    padding: 12px 8px;
                    text-align: center;
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
                ">
                    <div style="color: {color}; font-size: 13px; font-weight: bold; margin-bottom: 4px;">✅ {label} 완료</div>
                    <div style="color: #000000; font-size: 18px; font-weight: bold;">정답: {ans}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        def open_problem(i):
            """i번 문제 풀이 화면으로 간다. (단서를 아직 못 봤다면 먼저 검은 단서 화면으로 간다.)"""
            if i == FAST_PASS_INDEX:
                # 매우 어려움 문제로 곧장 넘어가도 단서를 놓치지 않도록, 아직 못 봤다면 먼저 보여 준다.
                if not st.session_state.stalker_clue_shown:
                    go_stalker_clue()
            elif is_stalker_clue_button(i):
                # 무작위로 뽑힌 '단서 버튼'을 처음 누르면 문제 대신 검은 단서 화면으로 간다.
                go_stalker_clue()
            st.session_state.current_problem = entries[i]
            st.session_state.current_problem_idx = i
            st.session_state.current_title = (
                fast_title if i == FAST_PASS_INDEX else st.session_state.title
            )
            st.session_state.step = "solve"
            st.rerun()

        cols = st.columns(3)
        for i in range(3):
            with cols[i]:
                if i in st.session_state.solved_indices:
                    solved_card(f"문제 {i+1}", entries[i][2], "#2e7d32")
                elif lucky_button(f"문제 {i+1} 📝", key=f"prob_btn_{i}", use_container_width=True):
                    open_problem(i)

        # 학년별 '매우 어려움' 문제: 문제 번호 없이 빨간 버튼으로 따로 둔다.
        st.markdown(
            """
            <style>
            .st-key-fast_pass_btn div[data-testid="stButton"] > button {
                background-color: #d32f2f !important;
                border: 1px solid #b71c1c !important;
            }
            .st-key-fast_pass_btn div[data-testid="stButton"] > button:hover {
                background-color: #b71c1c !important;
                border-color: #7f0000 !important;
            }
            .st-key-fast_pass_btn div[data-testid="stButton"] > button,
            .st-key-fast_pass_btn div[data-testid="stButton"] > button *,
            .st-key-fast_pass_btn div[data-testid="stButton"] > button:hover * {
                color: #ffffff !important;
                font-weight: 900 !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
        st.write("")
        _, hard_col, _ = st.columns([1, 1, 1])
        with hard_col:
            if FAST_PASS_INDEX in st.session_state.solved_indices:
                solved_card("매우 어려움", fast_problem[2], "#c62828")
            elif lucky_button("매우 어려움", key="fast_pass_btn", use_container_width=True):
                open_problem(FAST_PASS_INDEX)

        # 문제 3개를 모두 풀었거나, 매우 어려움 문제를 풀었으면 타임머신으로 갈 수 있다.
        solved = st.session_state.solved_indices
        if FAST_PASS_INDEX in solved or {0, 1, 2} <= solved:
            st.write("")
            st.write("")
            st.markdown("---")
            if lucky_button(
                "🚀 타임머신 작동자에게 가기", type="primary", use_container_width=True
            ):
                st.session_state.step = "timemachine"
                st.session_state.timemachine_success = False
                st.rerun()

    # --- 화면 4: 완료 화면 ---
    elif st.session_state.step == "end":
        current_ans = st.session_state.current_problem[2]

        readable_box(
            "<h2>정답을 기억하세요</h2>"
            f"<h3>정답: {html_escape(str(current_ans))}</h3>"
        )
        st.markdown("---")

        if lucky_button("문제 목록으로 돌아가기 📝", use_container_width=True):
            st.session_state.step = "select_problem"
            st.rerun()
