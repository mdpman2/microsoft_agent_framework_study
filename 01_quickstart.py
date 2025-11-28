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
    print("[Experiment 1] Microsoft Agent Framework quickstart\n")

    if not endpoint or not api_key:
        print("Environment error: set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env.")
        return

    client = AzureOpenAIResponsesClient(
        endpoint=endpoint,
        deployment_name=deployment,
        api_version=api_version,
        api_key=api_key,
    )

    try:
        agent = client.create_agent(
            name="HaikuBot",
            instructions="Respond in Korean with concise haiku-style summaries.",
        )

        user_prompt = "Microsoft Agent Framework와 Azure AI Foundry Agents의 차이를 두 문장으로 설명해줘."
        print(f"User: {user_prompt}")

        response = await agent.run(user_prompt)

        print(f"\nAssistant:\n{response}")
    except HttpResponseError as http_err:
        print(f"Azure OpenAI error: {http_err.message or http_err}")
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Unexpected error: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
