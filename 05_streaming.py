# 05_streaming.py
# IDE/터미널에서 “한 줄씩” 출력되는 것을 보면서 스트리밍 동작을 눈으로 확인
import asyncio

from azure.core.exceptions import HttpResponseError
from agent_framework.azure import AzureOpenAIResponsesClient

from config import (
    endpoint,
    api_key,
    api_version,
    deployment,
)

async def main() -> None:
    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment,
    )

    agent = client.create_agent(
        name="StreamingBot",
        instructions="답변을 한국어로 하고, 설명은 자세히 풀어서 말해줘.",
    )

    user_prompt = "Microsoft Agent Framework의 핵심 개념을 설명해줘."
    print(f"User: {user_prompt}\n")
    print("Assistant (streaming):\n")

    async for update in agent.run_stream(user_prompt):
        if getattr(update, "text", None):
            print(update.text, end="", flush=True)

    print("\n\n[done]")


if __name__ == "__main__":
    asyncio.run(main())