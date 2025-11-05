import datetime

import pydantic as p


class RecordMeta(p.BaseModel):
    """Metadata for a single SDCI record."""

    record_no: str
    """Record number. Example: 7028658-CN-010-002"""

    created: datetime.date
    """Calendar date the record was created."""

    record_type: str
    """Description of the record type. Example: 'Refrigeration Permit'"""

    status: str
    """Status of the record. Example: 'Completed'"""

    address: str = ""
    """Address associated with the record, if known. Example: '123 Main St'"""
