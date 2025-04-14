from typing import List

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage

from src.reflexion_agent.main import parser_json
from src.reflexion_agent.schemas import Reflection, AnswerQuestion


load_dotenv()


def execute_tools(state: List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation = state[-1]
    parsed_tool_call = parser_json.invoke(tool_invocation)

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_call:
        for query in parsed_call["args"]["search_queries"]:
            tool_invocations.append(
                # ToolInvocation(
                #     tool="tavily_search_result_json",
                #     tool_input=query,
                # )
            )
            ids.append(parsed_call["id"])

    pass


if __name__ == "__main__":
    print("Tool Executor")
    human_message = HumanMessage(
        content="Write about AI-Powered SOC / autonomous soc problem domain,"
                " list startups that do that and raised capital."
    )
    answer = AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=[
            "AI-powered SOC startups funding",
            "AI SOC problem domain specifics",
            "Technologies used by AI-powered SOC startups",
        ],
        id="call_KpYHichFFEmLitHFvFhKy1Ra",
    )

    raw_res = execute_tools(
        state = [
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": AnswerQuestion.__name__,
                        "args": answer.model_dump(),
                        "id": "call_KpYHichFFEmLitHFvFhKy1Ra"
                    }
                ]
            )
        ]
    )

    print(raw_res)
