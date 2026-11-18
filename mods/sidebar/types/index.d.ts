export type Tab = 'tokens' | 'cache' | 'context' | 'turn' | 'files' | 'todos' | 'prompts' | 'agents' | 'doubt' | 'commit'

export type Last = { model: string; input: number; cached: number; output: number; ms: number; usd?: number }
export type Rate = { live: number; peak: number; history: number[]; last?: Last; output: number; ms: number; usd?: number }

export type CacheSample = { at: number; model: string; read: number; write: number; fresh: number }
export type Cache = { samples: CacheSample[]; ttlMs: number; clock: string }

export type Row = { name: string; tokens: number; color: string; kind: 'used' | 'free' | 'buffer' | 'deferred' }
export type Snapshot = { rows: Row[]; total: number; max: number; percent: number; model: string; compactAt?: number }

export type Call = { id: string; tool: string; label: string; ms: number | null }
export type Todo = { file: string; text: string }
export type AgentType = { type: string; source: string }
export type Run = { id: string; type: string; description: string; status: string }
export type Draft = { message: string; stat: string; result: string }

declare module 'claude-code' {
  interface PluginState {
    sidebar: {
      tab: Tab
      rate: Rate
      cache: Cache
      snap: Snapshot | null
      calls: Call[]
      edits: Record<string, number>
      todos: Todo[]
      prompts: string[]
      agentTypes: AgentType[]
      runs: Run[]
      doubt: string
      draft: Draft
    }
  }
}
