from pydantic import BaseModel,Field

class BaseAnswer(BaseModel):
    summary: str = Field(description="一句话总结回答核心内容")
    content: str = Field(description="详细的回答正文，分点说明时用换行分隔")