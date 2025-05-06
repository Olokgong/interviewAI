import random
from openai import OpenAI
import streamlit as st

st.title("interviewAI")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "interview_questions" not in st.session_state:
    question_pool = [
        "지원 직무를 수행하기 위해 했던 노력이나 활동에 어떤 것들이 있나요?",
        "주변에서 말하는 지원자의 장단점이 있다면 무엇인가요?",
        "지원자가 같이 일하고 싶은 동료는 어떤 동료고, 같이 일하고 싶지 않는 동료는 어떤 동료인가요?",
        "본인이 가장 힘들었던 경험과 그것을 극복한 사례를 말해주세요.",
        "본인이 스트레스를 받는 경우와 그것을 해소하는 방법에 대해 말해주세요.",
        "우리 회사가 지원자를 뽑아야 할 이유에 대해서 말해주세요.",
        "지원자가 생각하는 5년 후 목표가 있나요?",
        "본인은 리더형 vs 팔로우형 중 어떤 유형에 더 가깝나요?",
        "지금 지원한 직무와 실제 회사에 들어와서 배정받는 직무가 다른 경우엔 어떻게 대처할 건가요?",
        "팀 단위의 프로젝트를 할 때, 팀에서 지원자가 협력하는 방법에 대해 말해주세요.",
        "팀에서 퍼포먼스가 떨어지는 인원이 있을 경우에 어떻게 대처할 건가요?",
        "본인의 성공 경험과 실패 경험에 대해 말해주세요.",
        "지원한 직무에서 핵심 성과 지표를 설정한다면 무엇이라고 생각하시나요?",
        "혼자 일하는 것과 팀으로 일하는 것 중에 어떤 업무방법을 더 선호하세요?",
        "팀 프로젝트에서 팀원들을 리딩해본 경험이 있나요?",
        "팀원들과 협업하면서 불만족스러웠던 부분이 있었나요?",
        "지원한 직무에서 협업 및 커뮤니케이션 스킬이 왜 중요하다고 생각하시나요?",
        "회사에 입사해서 열심히 일을 했는데, 그만큼의 인정이나 보상이 따르지 않을 경우엔 어떻게 하실 건가요?",
        "인생에서 가장 도전적이었던 경험이 있다면 말해주세요.",
        "살면서 가장 힘들었던 경험이 있다면 말해주세요.",
        "팀 동료와 갈등이 발생한다면 어떻게 해결하실 건가요?",
        "인생에서 가장 중요하게 여기는 게 무엇인가요?",
        "최근 지원자의 최대 관심사는 무엇인가요?",
        "지원자의 좌우명이 있다면?",
        "살면서 도덕적으로 일탈을 해본 경험이 있나요?",
        "다른 지원자들과 차별화되는 지원자만의 강점이 있다면 말해주세요.",
        "지원한 직무에서 가장 중요한 역량이 무엇이라고 생각하나요?",
        "상사의 부당한 지시가 있다면 어떻게 대처하실 건가요?",
        "살면서 가장 노력했던 경험이 있다면 말해주세요.",
        "지원자가 가장 존경하는 인물, 롤모델이 있나요?"
    ]
    st.session_state.interview_questions = random.sample(question_pool, 3)
    st.session_state.answers = []
    st.session_state.question_index = -1
    st.session_state.feedback_given = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("지원 직무를 입력해주세요." if st.session_state.question_index == -1 else "답변을 입력해주세요."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if st.session_state.question_index == -1:
        st.session_state.job = prompt
        st.session_state.question_index = 0
        question = st.session_state.interview_questions[0]
        with st.chat_message("assistant"):
            st.markdown(f"1번 질문입니다:\n\n**{question}**")
        st.session_state.messages.append({"role": "assistant", "content": f"1번 질문입니다:\n\n**{question}**"})

    elif st.session_state.question_index < 3:
        st.session_state.answers.append(prompt)
        st.session_state.question_index += 1

        if st.session_state.question_index < 3:
            question = st.session_state.interview_questions[st.session_state.question_index]
            with st.chat_message("assistant"):
                st.markdown(f"{st.session_state.question_index + 1}번 질문입니다:\n\n**{question}**")
            st.session_state.messages.append({"role": "assistant", "content": f"{st.session_state.question_index + 1}번 질문입니다:\n\n**{question}**"})

# 답변이 모두 완료되었고, 피드백이 아직 출력되지 않았다면 피드백 출력
if st.session_state.question_index == 3 and not st.session_state.feedback_given:
    job = st.session_state.job
    feedback_prompt = f"""지원 직무는 '{job}'입니다. 다음은 그에 대해 받은 인터뷰 질문과 지원자의 응답입니다.\n\n"""

    for i, (q, a) in enumerate(zip(st.session_state.interview_questions, st.session_state.answers), 1):
        feedback_prompt += f"{i}번 질문: {q}\n지원자의 답변: {a}\n\n"

    # 새 피드백 요청: 각 질문별 분석 X, 전체 총평만 요청
    feedback_prompt += (
        "위 인터뷰 답변들을 바탕으로 전체적으로 평가해 주세요.\n"
        "답변에서 **지원 직무와 관련해 적절한 점**과 **부족한 점**을 중심으로 분석하고, "
        "**전체 총평**을 제공해 주세요. 개별 질문 분석은 하지 마세요."
    )

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": feedback_prompt}],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.feedback_given = True