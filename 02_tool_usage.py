import asyncio

from azure.core.exceptions import HttpResponseError
from agent_framework.azure import AzureOpenAIResponsesClient

from config import (
    endpoint,
    api_key,
    api_version,
    deployment,
)

# ==========================================
# 1. 도구(Tool) 정의
# ==========================================
def calculate_sum(a: int, b: int) -> int:
    """
    두 숫자의 합을 계산합니다.

    Args:
        a: 첫 번째 숫자
        b: 두 번째 숫자
    """
    print(f"   >>> [Tool] calculate_sum 호출됨: {a} + {b}")
    return a + b

async def main():
    print("🚀 [실습 2] 도구 사용 (Function Calling) 시작\n")

    if not endpoint or not api_key:
        print("❌ 오류: 환경 변수(OPEN_AI_ENDPOINT_5, OPEN_AI_KEY_5)를 설정해주세요.")
        return

    # 2. 클라이언트 생성
    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        deployment_name=deployment,
        api_version=api_version,
        api_key=api_key,
    )

    # 3. 에이전트 생성 및 도구 등록
    # - tools 리스트에 함수를 직접 전달하면 프레임워크가 자동으로 스키마를 생성합니다.
    agent = client.create_agent(
        name="MathBot",
        instructions="당신은 계산을 잘하는 AI 비서입니다. 질문에 답하기 위해 도구를 사용하세요.",
        tools=[calculate_sum]
    )

    # 4. 에이전트 실행
    user_prompt = "15 더하기 27은 뭐야?"
    print(f"👤 사용자: {user_prompt}")

    # 에이전트가 도구를 호출하고 결과를 포함하여 최종 답변을 생성합니다.
    response = await agent.run(user_prompt)

    print(f"\n🤖 에이전트:\n{response}")

if __name__ == "__main__":
    asyncio.run(main())
