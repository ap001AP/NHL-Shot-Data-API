from pydantic import BaseModel, Field
from typing import Literal

class ShotRequest(BaseModel):
    x_coord: float = Field(..., example=58, description="Shot x-coordinate on ice")
    y_coord: float = Field(..., example=-25, description="Shot y-coordinate on ice")
    shot_type: Literal["wrist", "snap", "slap", "backhand", "tip-in", "wrap-around", "unknown"] = Field(..., example="wrist")
    away_skaters: int = Field(5, ge=3, le=6, example=5)
    home_skaters: int = Field(5, ge=3, le=6, example=5)
    period: int = Field(..., ge=1, le=6, example=1)

class ShotResponse(BaseModel):
    goal_probability: float = Field(..., description="Predicted probability this shot is a goal (xG)")
    is_high_danger: bool = Field(..., description="True if shot is from the high-danger slot area")
    distance: float = Field(..., description="Distance from goal in feet")
    angle: float = Field(..., description="Angle to goal in degrees")
    model_version: str = "1.0.0"