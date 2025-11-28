# 06_observability_tracing.py
"""
OpenTelemetry 설정 함수를 통해 Microsoft Agent Framework에 내장된 텔레메트리를 켜고,
에이전트 실행 시 생성되는 추적(Trace)·스팬(Span)을 콘솔이나 외부 백엔드(Azure Monitor, Grafana 등)로 내보내는 예제입니다.​

이걸 통해 다음 같은 것들을 확인할 수 있습니다.​

어떤 에이전트가 언제 호출되었는지(대화 흐름)

모델 호출 시간, 응답 시간, 실패 여부 같은 성능 메트릭

도구 호출·서브에이전트 호출 등 멀티 에이전트 워크플로우의 호출 경로(분산 트레이싱)
"""
import asyncio

from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework.observability import setup_observability

from config import (
    endpoint,
    api_key,
    api_version,
    deployment,
)

def setup_tracing() -> None:
    # Agent Framework 내장 옵저버빌리티 설정 (콘솔로 OpenTelemetry 출력)
    setup_observability(enable_sensitive_data=True)


async def main() -> None:
    setup_tracing()

    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        api_key=api_key,
        api_version=api_version,
        deployment_name=deployment,
    )

    agent = client.create_agent(
        name="TracingBot",
        instructions="모든 답변은 한국어로, 짧고 명확하게 답해줘.",
    )

    result = await agent.run("Observability 기능을 한 문단으로 설명해줘.")
    print("\nAssistant:\n", result)


if __name__ == "__main__":
    asyncio.run(main())