from pydantic import BaseModel


class RecommendationItem(BaseModel):
    priority: str
    category: str
    recommendation: str


class RecommendationResponse(BaseModel):
    recommendations: list[RecommendationItem]
