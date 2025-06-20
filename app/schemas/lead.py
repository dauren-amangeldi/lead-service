from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class LeadBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phonecc: str
    phone: str
    user_ip: str
    aff_sub: str
    aff_sub2: str
    aff_sub3: str
    aff_sub4: str
    aff_id: str
    status_id: int


class LeadCreate(BaseModel):
    first_name: str = Field(default="empty", description="First name of the lead")
    last_name: str = Field(default="empty", description="Last name of the lead")
    email: str = Field(default="empty", description="Email address of the lead")
    password: str = Field(default="empty", description="Password for the lead")
    phonecc: str = Field(default="empty", description="Phone country code (e.g. +1)")
    phone: str = Field(default="empty", description="Phone number without country code")
    aff_sub: str = Field(default="empty", description="Affiliate sub-parameter 1")
    aff_sub2: str = Field(default="empty", description="Affiliate sub-parameter 2")
    aff_sub4: str = Field(default="empty", description="Affiliate sub-parameter 4")


class LeadResponse(BaseModel):
    status: str = Field(..., description="Status of the lead creation request")
    lead_id: int = Field(..., description="ID of the created lead")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "lead_id": 1
            }
        }


class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 