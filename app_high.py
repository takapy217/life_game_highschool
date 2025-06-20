# app_high.py（完全版・use_container_width対応）
import streamlit as st
import json
import random
import os
import time
import streamlit.components.v1 as components

# セッション初期化
def init_session():
    defaults = {
        "player_name": "Tony",
        "player_gender": "male",
        "birth_year": 1972,
        "club": "",
        "path": "",
        "love_choice": "",
        "love_result": "",
        "high_stage": "start",
        "love_event_stage": "intro_short",
        "love_response_key": "",
        "love_event_count": 1,
        "exam_result": "",
        "friend_stage": "intro",
        "friend_response_key": "",
        "highschool_club": ""
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session()

# app_high.py の上部（init_sessionのあと）に追記：
# if st.button("（開発用）"):
#     st.session_state.high_stage = "path_select"
#     st.rerun()

# JSON読込
def load_story():
    with open("high_story.json", "r", encoding="utf-8") as f:
        return json.load(f)

story_data = load_story()



# ストーリー表示
def show_story(key):
    data = story_data.get(key, {})
    image = data.get("image")
    narration = data.get("narration", "")
    if image:
        path = os.path.join("assets", "high", image)
        if os.path.exists(path):
            st.image(path, use_container_width=True)
    st.markdown(narration.replace("{player_name}", st.session_state.player_name))

# 友情イベントの処理
def handle_friend_event():
    if "friend_stage" not in st.session_state or st.session_state.friend_stage not in ["intro_short", "intro_long", "choice", "response"]:
        st.session_state.friend_stage = "intro_short"

    gender = st.session_state.player_gender
    key = "friend_event"
    event_data = story_data.get(key, {})

    character_key = "male" if gender == "male" else "female"
    chara = event_data.get(character_key, {})

    if st.session_state.friend_stage == "intro_short":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        st.markdown(chara.get("intro_short", "").replace("{player_name}", st.session_state.player_name))

        if st.button("続きを読む"):
            st.session_state.friend_stage = "intro_long"
            st.rerun()

    elif st.session_state.friend_stage == "intro_long":
        image = chara.get("image")


        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        st.markdown(chara.get("intro_long", "").replace("{player_name}", st.session_state.player_name))

        if st.button("どんな話題で盛り上がる？"):
            st.session_state.friend_stage = "choice"
            st.rerun()


    elif st.session_state.friend_stage == "choice":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)

        # st.markdown("### 話題を選んでください：")
        for option in chara.get("choices", []):
            if st.button(option, key=f"{key}_{option}"):
                st.session_state.friend_response_key = option
                st.session_state.friend_stage = "response"
                st.rerun()

    elif st.session_state.friend_stage == "response":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)

        response = chara.get("responses", {}).get(st.session_state.friend_response_key, {})
        st.markdown(response.get("narration", "").replace("{player_name}", st.session_state.player_name))

        if st.button("2年生の2学期、さらなる出会いの予感☆"):
            st.session_state.friend_stage = "intro"
            st.session_state.high_stage = "love_event_2"
            st.rerun()

# 恋愛イベントの処理（3ステージ構成）
def handle_love_event(event_number):
    gender = st.session_state.player_gender
    key = f"love_{event_number}"

    event_data = story_data.get(key, {})
    opposite_key = "female" if gender == "male" else "male"
    character_key = event_data.get(opposite_key)

    if not character_key or character_key not in event_data:
        st.error(f"❌ キャラデータが見つかりません（event: {key}, 対象: {character_key}）")
        return

    chara = event_data[character_key]

    if st.session_state.love_event_stage == "intro_short":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        st.markdown(chara.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.love_event_stage = "intro"
            st.rerun()

    elif st.session_state.love_event_stage == "intro":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        st.markdown(chara.get("intro_long", "").replace("{player_name}", st.session_state.player_name))

        if st.button("なんて返す？"):
            st.session_state.love_event_stage = "choice"
            st.rerun()

    elif st.session_state.love_event_stage == "choice":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        # st.markdown("### どう返事する？")
        for option in chara.get("choices", []):
            if st.button(option, key=f"{key}_{option}"):
                st.session_state.love_response_key = option
                st.session_state.love_event_stage = "response"
                st.rerun()

    elif st.session_state.love_event_stage == "response":
        image = chara.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)
        response = chara.get("responses", {}).get(st.session_state.love_response_key, {})
        st.markdown(response.get("narration", "").replace("{player_name}", st.session_state.player_name))
        if st.button("次へ"):
            st.session_state.love_event_stage = "intro_short"
            current_stage = st.session_state.high_stage
            if current_stage == "love_event_1":
                st.session_state.high_stage = "stream_select"
                st.session_state.love_event_count = 2

            elif current_stage == "love_event_2":
                st.session_state.high_stage = "path_select"
                st.session_state.love_event_count = 3

            elif current_stage == "love_event_3":
                # ✅ 直で exam_results に進む進路
                direct_exam_results_paths = ["就職", "美容師", "プロ野球選手", "アメリカの大学", "ミュージシャン",
                                             "お笑い芸人"]
                if st.session_state.path in direct_exam_results_paths:
                    st.session_state.high_stage = "exam_results"
                else:
                    st.session_state.high_stage = "exam_result"
            st.rerun()

# 画面ごとの処理
if st.session_state.high_stage == "start":
    st.markdown("#### 1972年4月～1973年3月生まれ版")
    show_story("intro")

    # name = st.text_input("あなたの名前を入力してください", value=st.session_state.player_name)
    name = st.text_input("あなたの名前を入力してください")
    gender = st.radio("性別を選んでください", ["male", "female"],
                      index=0 if st.session_state.player_gender == "male" else 1)

    if st.button("ゲームスタート"):
        if name.strip() == "":
            st.warning("名前を入力してください。")
        else:
            st.session_state.player_name = name
            st.session_state.player_gender = gender
            st.session_state.high_stage = "start_transition"  # ←ここ変更
            st.rerun()

elif st.session_state.high_stage == "start_transition":
    show_story("start_transition")
    if st.button("次へ進む"):
        st.session_state.high_stage = "ceremony"
        st.rerun()


elif st.session_state.high_stage == "ceremony":
    show_story("ceremony")  # JSONから画像とナレーションを取得して表示
    if st.button("通学手段はどうする？"):
        st.session_state.high_stage = "commute"  # 通学選択ステージへ
        st.rerun()


elif st.session_state.high_stage == "commute":
    st.image(f"assets/high/tuugaku.png", use_container_width=True)
    # st.markdown("通学手段はどっち？？")
    if st.button("電車で通う"):
        st.session_state.high_stage = "commute_train"
        st.rerun()
    if st.button("自転車で通う"):
        st.session_state.high_stage = "commute_bike"
        st.rerun()

elif st.session_state.high_stage == "commute_train":
    show_story(f"train_{st.session_state.player_gender}")
    if st.button("部活は入る？"):
        st.session_state.high_stage = "club"
        st.rerun()

elif st.session_state.high_stage == "commute_bike":
    show_story(f"bike_{st.session_state.player_gender}")
    if st.button("部活を選ぼう"):
        st.session_state.high_stage = "club"
        st.rerun()

elif st.session_state.high_stage == "club":
    st.image("assets/high/bukatsu.png", use_container_width=True)

    # JSONから部活名を取得（キー名だけ）
    clubs_data = story_data.get("clubs", {})
    club_names = list(clubs_data.keys())

    selected_club = st.selectbox("どの部活に入る？それとも帰宅部？", club_names)

    if st.button("この部活に決める！"):
        st.session_state.club = selected_club
        st.session_state.high_stage = "club_story"
        st.rerun()



elif st.session_state.high_stage == "club_story":
    club_info = story_data.get("clubs", {}).get(st.session_state.club, {})
    gender = st.session_state.player_gender

    # narrationの処理：gender指定があるか確認
    narration_data = club_info.get("narration", "")
    if isinstance(narration_data, dict):
        narration = narration_data.get(gender, "")
    else:
        narration = narration_data

    image = club_info.get("image")

    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    st.markdown(narration.replace("{player_name}", st.session_state.player_name))

    if st.button("新たな出会いの予感☆"):
        st.session_state.high_stage = "love_event_1"
        st.rerun()




elif st.session_state.high_stage.startswith("love_event_"):
    event_num = int(st.session_state.high_stage.split("_")[-1])
    handle_love_event(event_num)

elif st.session_state.high_stage == "stream_select":
    story = story_data.get("stream_select", {})
    image = story.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    # 初回：短いナレーションを表示
    if "stream_select_stage" not in st.session_state:
        st.session_state.stream_select_stage = "short"

    if st.session_state.stream_select_stage == "short":
        st.markdown(story.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.stream_select_stage = "long"
            st.rerun()

    elif st.session_state.stream_select_stage == "long":
        st.markdown(story.get("intro_long", "").replace("{player_name}", st.session_state.player_name))

        if st.button("文系を選ぶ"):
            st.session_state.high_stage = "stream_lit"
            del st.session_state["stream_select_stage"]
            st.rerun()

        if st.button("理系を選ぶ"):
            st.session_state.high_stage = "stream_sci"
            del st.session_state["stream_select_stage"]
            st.rerun()

elif st.session_state.high_stage == "stream_lit":
    if "stream_lit_stage" not in st.session_state:
        st.session_state.stream_lit_stage = "short"

    story = story_data.get(f"文系_{st.session_state.player_gender}", {})
    image = story.get("image")

    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.stream_lit_stage == "short":
        st.markdown(story.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.stream_lit_stage = "long"
            st.rerun()

    elif st.session_state.stream_lit_stage == "long":
        st.markdown(story.get("intro_long", "").replace("{player_name}", st.session_state.player_name))
        if st.button("次へ進む"):
            st.session_state.high_stage = "friend_event"
            del st.session_state["stream_lit_stage"]
            st.rerun()
elif st.session_state.high_stage == "stream_sci":
    if "stream_sci_stage" not in st.session_state:
        st.session_state.stream_sci_stage = "short"

    story = story_data.get(f"理系_{st.session_state.player_gender}", {})
    image = story.get("image")

    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.stream_sci_stage == "short":
        st.markdown(story.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.stream_sci_stage = "long"
            st.rerun()

    elif st.session_state.stream_sci_stage == "long":
        st.markdown(story.get("intro_long", "").replace("{player_name}", st.session_state.player_name))
        if st.button("次へ進む"):
            st.session_state.high_stage = "friend_event"
            del st.session_state["stream_sci_stage"]
            st.rerun()


elif st.session_state.high_stage == "friend_event":
    handle_friend_event()

elif st.session_state.high_stage == "path_select":
    story = story_data.get("path_select", {})
    image = story.get("image")

    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    # 初回表示かどうかを管理
    if "path_select_stage" not in st.session_state:
        st.session_state.path_select_stage = "short"

    if st.session_state.path_select_stage == "short":
        st.markdown(story.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.path_select_stage = "long"
            st.rerun()

    elif st.session_state.path_select_stage == "long":
        st.markdown(story.get("intro_long", "").replace("{player_name}", st.session_state.player_name))

        # ✅ 修正ポイント①：JSONから取得
        paths = story_data.get("paths", {})
        path_options = list(paths.keys())

        # ✅ 修正ポイント②：不要な選択肢を排除＆条件で追加
        if "プロ野球選手" in path_options:
            path_options.remove("プロ野球選手")  # デフォルトに含まれている可能性を排除

        if "美容師" not in path_options:
            path_options.append("美容師")  # 美容師は男女どちらでも表示

        # ✅ 男子＆野球部だけにプロ野球を追加
        if (
            st.session_state.player_gender == "male"
            and st.session_state.club == "野球部"
            and "プロ野球選手" not in path_options
        ):
            path_options.append("プロ野球選手")

        # ✅ 選択表示
        selected = st.selectbox("進路を選んでください", path_options)

        if st.button("この進路に決定"):
            st.session_state.path = selected
            st.session_state.path_select_stage = None  # リセット
            st.session_state.next_after_path_story = "love_event_3"  # 恋愛3へ必ず進む
            st.session_state.high_stage = "selected_path_story"
            st.rerun()


elif st.session_state.high_stage == "selected_path_story":
    path_key = st.session_state.path
    path_data = (
        story_data.get("paths", {}).get(path_key)
        or story_data.get(f"path_{path_key}", {})
    )

    if path_data:
        image = path_data.get("image")
        if image:
            st.image(f"assets/high/{image}", use_container_width=True)

        if "selected_path_story_stage" not in st.session_state:
            st.session_state.selected_path_story_stage = "short"

        # 1回目：短い小説
        if st.session_state.selected_path_story_stage == "short":
            short = path_data.get("narration_short", "")
            st.markdown(short.replace("{player_name}", st.session_state.player_name))
            if st.button("続きを読む"):
                st.session_state.selected_path_story_stage = "long"
                st.rerun()

        # 2回目：長い小説
        elif st.session_state.selected_path_story_stage == "long":
            long = path_data.get("narration", "")
            st.markdown(long.replace("{player_name}", st.session_state.player_name))
            if st.button("高校3年、更なる出会いの予感☆"):
                st.session_state.selected_path_story_stage = None  # リセット
                next_stage = st.session_state.get("next_after_path_story", "love_event_3")
                if next_stage == "love_event_3":
                    st.session_state.love_event_count = 3
                st.session_state.high_stage = next_stage
                st.rerun()
    else:
        st.warning(f"⚠️ {path_key} に対応するストーリーが見つかりません。")


elif st.session_state.high_stage == "love_result":
    # st.write("🎯 love_result ステージ突入！")
    # st.write("▶️ love_result =", st.session_state.love_result)
    # st.write("▶️ love_choice =", st.session_state.love_choice)

    if st.session_state.love_result == "none":
        # ✅ 告白しないパターンは専用フローへ遷移
        st.session_state.high_stage = "no_love_closure"
        st.session_state.no_love_friend = "隼" if st.session_state.player_gender == "male" else "結衣"
        st.rerun()

    else:
        # 成功または失敗の共通処理へ（既存のまま）
        love_name = st.session_state.love_choice
        result_key = "love_result_success" if st.session_state.love_result == "success" else "love_result_fail"
        result_data = story_data.get(result_key, {}).get(love_name)

        if not result_data:
            st.error(f"❌ 結果データが見つかりません（key: {result_key} / name: {love_name}）")
        else:
            if "love_result_stage" not in st.session_state:
                st.session_state.love_result_stage = "short"

            image = result_data.get("image")
            if image:
                st.image(f"assets/high/{image}", use_container_width=True)

            if st.session_state.love_result_stage == "short":
                short_intro = result_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name)
                st.markdown(short_intro)
                if st.button("続きを読む", key="btn_love_result_more"):
                    st.session_state.love_result_stage = "long"
                    st.rerun()

            elif st.session_state.love_result_stage == "long":
                narration = result_data.get("narration", "").replace("{player_name}", st.session_state.player_name)
                st.markdown(narration)
                if st.button("卒業へ", key="btn_love_result_graduation"):
                    st.session_state.high_stage = "graduation"
                    st.session_state.love_result_stage = "short"
                    st.rerun()

elif st.session_state.high_stage == "exam_result":
    result_data = story_data.get("exam_result", {})
    image = result_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    st.markdown(result_data.get("narration", "").replace("{player_name}", st.session_state.player_name))

    if st.button("次へ", key="btn_exam_result_next"):
        if st.session_state.path in ["最難関大学", "有名私立大学", "地元大学", "とにかく国立大学"]:
            st.session_state.high_stage = "exam_results"
        else:
            st.session_state.high_stage = "love_confess"
        st.rerun()



elif st.session_state.high_stage == "exam_results":
    if "exam_stage" not in st.session_state:
        st.session_state.exam_stage = "short"

    path_key = st.session_state.path.strip()
    exam_data = story_data.get("exam_results", {}).get(path_key, {})

    image = exam_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.exam_stage == "short":
        st.markdown(exam_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.exam_stage = "long"
            st.rerun()
    else:
        st.markdown(exam_data.get("intro_long", "").replace("{player_name}", st.session_state.player_name))
        if st.button("次へ"):
            st.session_state.high_stage = "love_confess"
            st.session_state.exam_stage = None
            st.rerun()


elif st.session_state.high_stage == "exam_result_show":
    if "exam_stage" not in st.session_state:
        st.session_state.exam_stage = "short"

    path_key = st.session_state.path.strip()  # 「難関大学」など
    exam_data = story_data.get("exam_results", {}).get(path_key, {})  # ←★ここ修正！

    image = exam_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.exam_stage == "short":
        st.markdown(exam_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.exam_stage = "long"
            st.rerun()
    else:
        st.markdown(exam_data.get("intro_long", "").replace("{player_name}", st.session_state.player_name))
        if st.button("次へ"):
            st.session_state.high_stage = "love_confess"
            st.session_state.exam_stage = None
            st.rerun()

elif st.session_state.high_stage == "love_confess":
    if "love_confess_stage" not in st.session_state:
        st.session_state.love_confess_stage = "short"

    confess_data = story_data.get("love_confess", {})
    image = confess_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.love_confess_stage == "short":
        st.markdown(confess_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.love_confess_stage = "long"
            st.rerun()

    elif st.session_state.love_confess_stage == "long":
        st.markdown(confess_data.get("intro_long", "").replace("{player_name}", st.session_state.player_name))

        # ✅ 告白対象リストの表示（元のロジック）
        if st.session_state.player_gender == "male":
            love_names = ["結衣", "琴音", "渚"]
        else:
            love_names = ["隼", "悠真", "晴"]
        love_names.append("誰にも告白しない")

        for name in love_names:
            label = f"{name} に告白する" if name != "誰にも告白しない" else name
            if st.button(label):
                st.session_state.love_choice = name
                time.sleep(1)
                if name != "誰にも告白しない":
                    success = random.random() < 0.6
                    st.session_state.love_result = "success" if success else "fail"
                else:
                    st.session_state.love_result = "none"
                st.session_state.high_stage = "love_result"
                st.session_state.love_confess_stage = None  # ← 念のため初期化
                st.rerun()

elif st.session_state.high_stage == "no_love_closure":
    friend_name = st.session_state.get("no_love_friend", "隼")
    story_key = "no_love_friend_hayato" if friend_name == "隼" else "no_love_friend_yui"
    story = story_data.get(story_key, {})

    if "no_love_stage" not in st.session_state:
        st.session_state.no_love_stage = "short"

    image = story.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.no_love_stage == "short":
        short = story.get("intro_short", "").replace("{player_name}", st.session_state.player_name)
        st.markdown(short)
        if st.button("続きを読む", key="btn_no_love_more"):
            st.session_state.no_love_stage = "long"
            st.rerun()

    elif st.session_state.no_love_stage == "long":
        narration = story.get("narration", "").replace("{player_name}", st.session_state.player_name)
        st.markdown(narration)
        if st.button("卒業へ", key="btn_no_love_graduation"):
            st.session_state.high_stage = "graduation"
            st.session_state.no_love_stage = "short"
            st.rerun()



elif st.session_state.high_stage == "graduation":
    # st.write("🎓 現在：graduation ステージ！")  # ← ✅ログ表示
    if "graduation_stage" not in st.session_state:
        st.session_state.graduation_stage = "short"

    grad_data = story_data.get("graduation", {})
    image = grad_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    if st.session_state.graduation_stage == "short":
        st.markdown(grad_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name))
        if st.button("続きを読む"):
            st.session_state.graduation_stage = "long"
            st.rerun()

        # import time  # ← 忘れずにインポート！

    elif st.session_state.graduation_stage == "long":
        st.markdown(grad_data.get("narration", "").replace("{player_name}", st.session_state.player_name))
        if st.button("エンディングへ"):
            # st.balloons()  # 🎈風船を表示！
            # time.sleep(2)  # 🎈風船を見せるために2秒待つ（1.5〜2秒がおすすめ）
            st.session_state.high_stage = "ending_intro"  # ←ここを忘れず修正！
            st.session_state.graduation_stage = None  # クリアしておく
            st.rerun()


elif st.session_state.high_stage == "ending_intro":
    ending_data = story_data.get("ending", {})
    image = ending_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    intro_short = ending_data.get("intro_short", "").replace("{player_name}", st.session_state.player_name)
    st.markdown(intro_short)

    if st.button("次へ"):
        st.session_state.high_stage = "ending"
        st.rerun()

elif st.session_state.high_stage == "ending":
    ending_data = story_data.get("ending", {})
    image = ending_data.get("image")
    if image:
        st.image(f"assets/high/{image}", use_container_width=True)

    intro_long = ending_data.get("intro_long", "").replace("{player_name}", st.session_state.player_name)
    st.markdown(intro_long)

    if st.button("次へ"):
        st.session_state.high_stage = "ending_finish"
        st.rerun()

elif st.session_state.high_stage == "ending_finish":
    ending_data = story_data.get("ending", {})
    image = ending_data.get("image")
    if image:
        st.image(f"assets/high/high_thankyou.png", use_container_width=True)
        # st.markdown("Thanks for playing!")

    if st.button("最初に戻る"):
        st.session_state.clear()
        st.rerun()











