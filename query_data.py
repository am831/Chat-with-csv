import semantic_kernel as sk
import pandas as pd
from semantic_kernel.core_skills import DataSkill
import semantic_kernel.connectors.ai.google_palm as sk_gp
import semantic_kernel.connectors.ai.open_ai as sk_oai

def create_gp_instance(api_key):
    kernel = sk.Kernel()
    palm_chat_completion = sk_gp.GooglePalmChatCompletion(
        "models/chat-bison-001", api_key
    )
    kernel.add_chat_service("models/chat-bison-001", palm_chat_completion)
    return kernel, palm_chat_completion

def create_oai_instance(api_key):
    kernel = sk.Kernel()
    openai_chat_completion = sk_oai.OpenAIChatCompletion("gpt-3.5-turbo", api_key)
    kernel.add_chat_service("chat_service", openai_chat_completion)
    return kernel, openai_chat_completion

async def query_ai(kernel, assistant, query: str, data: pd.DataFrame):
    data_skill = kernel.import_skill(
        DataSkill(data=data, service=assistant), skill_name="data"
    )
    query_async = data_skill["queryAsync"]
    result = await query_async.invoke_async(query)
    return result
