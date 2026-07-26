from fastapi import FastAPI, HTTPException
from app.models import InvalidMandateRequest, InvalidMandateResponse, MandateRecord

app = FastAPI(title="Fraud Detection API")


# ---------------------------------------------------------------------------
# Placeholder data store – replace with real DB / model inference as needed
# ---------------------------------------------------------------------------
_INVALID_MANDATES: list[dict] = [
    {
        "mandateId": "M001",
        "employeeId": "E100",
        "amount": 450000.0,
        "fraudScore": 0.92,
        "flagReason": "Duplicate payment detected",
    },
    {
        "mandateId": "M002",
        "employeeId": "E101",
        "amount": 320000.0,
        "fraudScore": 0.87,
        "flagReason": "Ghost worker pattern",
    },
    {
        "mandateId": "M003",
        "employeeId": "E102",
        "amount": 610000.0,
        "fraudScore": 0.95,
        "flagReason": "Salary inflation anomaly",
    },
]


@app.post("/api/InvalidMandateRequest/Get", response_model=InvalidMandateResponse)
def get_invalid_mandate_requests(request: InvalidMandateRequest):
    """
    Return a paginated batch of payroll mandate records flagged as invalid.

    - **requestId**: Unique identifier for this request.
    - **batchNo**: 1-based page number (first batch = 1).
    - **batchsize**: Number of records to return per batch.
    """
    if request.batchsize <= 0:
        raise HTTPException(status_code=400, detail="batchsize must be greater than 0")
    if request.batchNo <= 0:
        raise HTTPException(status_code=400, detail="batchNo must be greater than 0")

    total = len(_INVALID_MANDATES)
    start = (request.batchNo - 1) * request.batchsize
    if start >= total:
        raise HTTPException(
            status_code=404,
            detail=f"batchNo {request.batchNo} exceeds available data (totalRecords={total})",
        )
    end = start + request.batchsize
    page_data = _INVALID_MANDATES[start:end]

    records = [MandateRecord(**item) for item in page_data]

    return InvalidMandateResponse(
        requestId=request.requestId,
        batchNo=request.batchNo,
        batchsize=request.batchsize,
        totalRecords=total,
        records=records,
    )
