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
    print("🚀 [실습 3] 대화형 챗봇 (Chat Loop) 시작\n")
    print("종료하려면 'exit' 또는 'quit'를 입력하세요.\n")

    if not endpoint or not api_key:
        print("❌ 오류: 환경 변수 설정을 확인하세요.")
        return

    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        deployment_name=deployment,
        api_version=api_version,
        api_key=api_key,
    )

    agent = client.create_agent(
        name="ChatBot",
        instructions="당신은 친절한 대화 상대입니다. 한국어로 자연스럽게 대화하세요."
    )

    # 대화 루프
    while True:
        user_input = input("👤 사용자: ")
        if user_input.lower() in ["exit", "quit"]:
            print("대화를 종료합니다.")
            break

        # agent.run()은 기본적으로 상태를 유지하지 않는 단발성 실행일 수 있습니다.
        # 프레임워크 버전에 따라 대화 기록 관리가 다를 수 있으나,
        # 여기서는 기본 run 메서드를 사용하여 연속적인 대화를 시도합니다.
        # (참고: 실제 상태 관리가 필요한 경우 별도의 Thread 관리 객체를 사용해야 할 수 있습니다)
        response = await agent.run(user_input)

        print(f"🤖 에이전트: {response}\n")

if __name__ == "__main__":
    asyncio.run(main())
