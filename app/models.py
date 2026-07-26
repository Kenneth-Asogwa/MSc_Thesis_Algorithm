from pydantic import BaseModel
from typing import Optional, List


class InvalidMandateRequest(BaseModel):
    requestId: str
    batchNo: int
    batchsize: int


class MandateRecord(BaseModel):
    mandateId: str
    employeeId: str
    amount: float
    fraudScore: float
    flagReason: str


class InvalidMandateResponse(BaseModel):
    requestId: str
    batchNo: int
    batchsize: int
    totalRecords: int
    records: List[MandateRecord]
