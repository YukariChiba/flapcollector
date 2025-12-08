from typing import TypedDict, Dict

class ServerConfig(TypedDict):
    url: str
    mode: str  # 'webhook' | 'poll'

class FlapInfo(TypedDict):
    FirstSeen: int
    RateSec: int
    TotalCount: int

class FlapEntry(TypedDict):
    prefix: str
    server: str
    info: FlapInfo

class AggregatedEntry(TypedDict):
    prefix: str
    asn: str
    maxLength: int
    metadata: Dict[str, FlapInfo]
    count: int # temp
