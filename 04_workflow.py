import asyncio

from azure.core.exceptions import HttpResponseError
from agent_framework.azure import AzureOpenAIResponsesClient

from config import (
    endpoint,
    api_key,
    api_version,
    deployment,
)

async def main():
    print("🚀 [실습 4] 순차적 워크플로우 (Sequential Workflow) 시작\n")

    if not endpoint or not api_key:
        print("❌ 오류: 환경 변수 설정을 확인하세요.")
        return

    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        deployment_name=deployment,
        api_version=api_version,
        api_key=api_key,
    )

    # 1. 에이전트 생성
    # - Planner: 여행 계획을 세우는 에이전트
    planner = client.create_agent(
        name="Planner",
        instructions="당신은 여행 플래너입니다. 주어진 목적지에 대한 3일치 여행 일정을 간략하게 작성하세요."
    )

    # - Writer: 일정을 블로그 포스트로 작성하는 에이전트
    writer = client.create_agent(
        name="Writer",
        instructions="당신은 여행 블로거입니다. 주어진 여행 일정을 바탕으로 매력적인 블로그 포스팅을 작성하세요."
    )

    # 2. 워크플로우 실행 (수동 순차 실행)
    # 프레임워크의 Graph 기능을 사용하지 않고, Python 코드로 제어 흐름을 구현하는 가장 기초적인 방법입니다.

    destination = "제주도"
    print(f"📍 목적지: {destination}")

    # Step 1: Planner 실행
    print("\n[Step 1] Planner가 일정을 계획 중입니다...")
    plan_response = await planner.run(f"{destination} 여행 일정을 짜줘.")
    print(f"📝 Planner 결과:\n{plan_response}")

    # Step 2: Writer 실행 (Planner의 출력을 입력으로 사용)
    print("\n[Step 2] Writer가 블로그 글을 작성 중입니다...")
    blog_post = await writer.run(f"다음 일정을 바탕으로 블로그 글을 써줘:\n{plan_response}")

    print(f"\n✨ 최종 블로그 포스트:\n{blog_post}")

if __name__ == "__main__":
    asyncio.run(main())
