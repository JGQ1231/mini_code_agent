import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError
from .schemas import BaseAnswer

load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )
        self.model = os.getenv("LLM_MODEL","deepseek-chat")

    def chat(self,user_question:str)->BaseAnswer:
        system_prompt=""""
        你是一个专业的编程助手。请严格返回JSON格式，不要多余文字、不要markdown标记。
        json必须包含两个key：
        - summary: 一句话总结回答
        - content: 详细回答正文
        """

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role":"system","content":system_prompt},
                    {"role":"user","content":user_question}
                ],
                temperature=0.1,
                response_format={"type":"json_object"}
            )

            result_text=response.choices[0].message.content
            result =BaseAnswer.model_validate_json(result_text)
            return result

        except ValidationError as e:
            raise RuntimeError(f"大模型返回格式不符合要求: {e}")
        except Exception as e:
            raise RuntimeError(f"调用大模型失败: {str(e)}")


