export interface RawRouteStats {
  FirstSeen: number
  TotalCount: number
}

export interface RawRoa {
  prefix: string
  metadata: Record<string, RawRouteStats>
}

export interface RawData {
  metadata: { generated: number }
  roas: RawRoa[]
}

export interface ProcessedVoter {
  host: string
  totalCount: number
  duration: number
  rate: number
}

export interface ProcessedRow {
  prefix: string
  count: number
  voters: ProcessedVoter[]
}

export interface ServerStatus {
  [host: string]: boolean
}

export interface ServerMeta {
  [host: string]: { url: string }
}

export interface FilterState {
  votes: number
  family: 'all' | 'v4' | 'v6'
}
