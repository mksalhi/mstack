import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register, RenderChildren } from 'claude-code'

import type { AgentType, Cache, Call, Draft, Last, Rate, Run, Snapshot, Tab, Todo } from '../types'

const PANE = 'sidebar'
const TABS: Tab[] = ['tokens', 'cache', 'context', 'turn', 'files', 'todos', 'prompts', 'agents', 'doubt', 'commit']
const BUILT_IN: AgentType[] = ['general-purpose', 'Explore', 'Plan'].map(type => ({ type, source: 'built-in' }))

const tab = atom({ plugin: 'sidebar', key: 'tab' } as const, 'tokens')
const rate = atom({ plugin: 'sidebar', key: 'rate' } as const, { live: 0, peak: 0, history: [], output: 0, ms: 0 } as Rate)
const cache = atom({ plugin: 'sidebar', key: 'cache' } as const, { samples: [], ttlMs: 300_000, clock: '' } as Cache)
const snap = atom({ plugin: 'sidebar', key: 'snap' } as const, null)
const calls = atom({ plugin: 'sidebar', key: 'calls' } as const, [])
const edits = atom({ plugin: 'sidebar', key: 'edits' } as const, {})
const todos = atom({ plugin: 'sidebar', key: 'todos' } as const, [])
const prompts = atom({ plugin: 'sidebar', key: 'prompts' } as const, [])
const agentTypes = atom({ plugin: 'sidebar', key: 'agentTypes' } as const, BUILT_IN)
const runs = atom({ plugin: 'sidebar', key: 'runs' } as const, [])
const doubt = atom({ plugin: 'sidebar', key: 'doubt' } as const, '')
const draft = atom({ plugin: 'sidebar', key: 'draft' } as const, { message: '', stat: '', result: '' } as Draft)

// Body columns the docked pane asks for; the person's own drag wins.
const DOCK_COLUMNS = 36
// Body rows it asks for when seated above the prompt instead: the one compact row.
const INLINE_ROWS = 1
const GREEN = '#3fb950'
const AMBER = '#d29922'
const RED = '#f85149'
const TRACK = 'stroke="#888" stroke-opacity=".35"'
const TICK = 500
const WINDOW = 3_000
const SPARK = 40
const BARS = '▁▂▃▄▅▆▇█'
// The stream carries text, not token counts: until a response ends and the API reports its real
// output_tokens, a token is this many characters. Each ended response re-fits it.
const START_CHARS_PER_TOKEN = 3.5
// From this prompt size up, an expired cache is worth a /compact before the next message.
const COMPACT_AT = 100_000

// $ per million tokens: [input, output, cache read, cache write], list prices (2026-09-25).
// Cache write is the 5-minute 1.25x of input. A model not here shows no price.
// ponytail: hand-kept table; the engine's own session total is the exact one if this drifts
const PRICES: Record<string, [number, number, number, number]> = {
  'claude-fable-5': [10, 50, 0.25, 12.5],
  'claude-opus-5-5': [4, 20, 0.2, 5],
  'claude-opus-5': [5, 25, 0.5, 6.25],
  'claude-opus-4': [5, 25, 0.5, 6.25],
  'claude-sonnet-5-5': [2, 10, 0.2, 2.5],
  'claude-sonnet-5': [2, 10, 0.2, 2.5],
  'claude-sonnet-4-6': [3, 15, 0.3, 3.75],
  'claude-haiku-4-5': [1, 5, 0.1, 1.25],
}

const DOUBT_PROMPT = `Argue against your last answer as a sceptical senior reviewer would. Under 250 words, markdown:
the strongest reason it is wrong or incomplete, what you did not verify, the cheapest check that would settle it,
and one line: would you still stand by it, yes or no.`

// The longest id first, so `claude-opus-5-5` is not read as `claude-opus-5`.
const priceOf = (model: string) =>
  Object.entries(PRICES)
    .sort(([a], [b]) => b.length - a.length)
    .find(([id]) => model.startsWith(id))?.[1]

const tokens = (count: number) => (count >= 10_000 ? `${(count / 1000).toFixed(1)}k` : count.toLocaleString('en-US'))
const usd = (amount: number) => `$${amount < 0.1 ? amount.toFixed(4) : amount.toFixed(2)}`
const seconds = (ms: number) => (ms < 1000 ? `${Math.round(ms)}ms` : `${(ms / 1000).toFixed(1)}s`)
const isTab = (word: string): word is Tab => (TABS as string[]).includes(word)
const heat = (percent: number) => (percent >= 85 ? RED : percent >= 65 ? AMBER : GREEN)

const spark = (history: number[]) => {
  const top = Math.max(1, ...history)

  return history.map(value => (value <= 0 ? '·' : BARS.charAt(Math.min(7, Math.floor((value / top) * 7.999))))).join('')
}

// The live rate as an area over the last SPARK ticks, newest at the right edge.
const chartOf = (history: number[], width: number, height: number, tone: string) => {
  const padded = [...Array(Math.max(0, SPARK - history.length)).fill(0), ...history] as number[]
  const top = Math.max(10, ...padded)
  const points = padded.map((value, i) => `${((i / (SPARK - 1)) * width).toFixed(1)},${(height - 2 - (value / top) * (height - 6)).toFixed(1)}`)

  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${width} ${height}" width="${width}" height="${height}" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M0 ${height - 0.5}H${width}" ${TRACK}/><polygon points="0,${height} ${points.join(' ')} ${width},${height}" fill="${tone}" fill-opacity=".18" stroke="none"/><polyline points="${points.join(' ')}" stroke="${tone}" stroke-width="1.5"/></svg>`
}

// A ring `share` full from the top.
const ringOf = (share: number, tone: string) =>
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 40 40" width="40" height="40" fill="none" stroke="${tone}" stroke-width="5" stroke-linecap="round"><circle cx="20" cy="20" r="15" ${TRACK}/>${
    share > 0 ? `<circle cx="20" cy="20" r="15" stroke-dasharray="${(Math.min(1, share) * 94.25).toFixed(2)} 100" transform="rotate(-90 20 20)"/>` : ''
  }</svg>`

const found = (file: string, written: string): Todo[] =>
  (written.match(/\b(TODO|FIXME)\b.*/g) ?? []).map(text => ({ file, text: text.trim().slice(0, 160) }))

// What is left of the cache entry, as the countdown prints it: m:ss under ten minutes, whole
// minutes above, so an idle hour-long cache redraws once a minute and not once a second.
const clockOf = (leftMs: number) => {
  if (leftMs <= 0) {
    return 'expired'
  }

  const total = Math.floor(leftMs / 1000)

  return total < 600 ? `${Math.floor(total / 60)}:${String(total % 60).padStart(2, '0')}` : `${Math.round(total / 60)}m`
}

// Characters seen as [at, count], the window's worth, for the live figure.
let seen: [number, number][] = []
let charsPerToken = START_CHARS_PER_TOKEN
let ticks = 0
let lastSnapAt = 0
let task = ''
let hasToastedDirty = false
// The two halves of the status line entry.
let contextText = ''
let cacheText = ''

const paintStatus = ($: EngineInterface) => {
  $.ui.status([contextText, cacheText].filter(Boolean).join(' · ') || undefined)
}

const snapshot = async ($: EngineInterface) => {
  lastSnapAt = await $.clock.now()
  const b = (await $.session.usage({ breakdown: 'summary' })).context.breakdown

  if (b === undefined) {
    return
  }

  const next: Snapshot = {
    rows: b.categories.map(({ name, tokens: count, color, kind }) => ({ name, tokens: count, color, kind })),
    total: b.totalTokens,
    max: b.rawMaxTokens,
    percent: b.percentage,
    model: b.model,
    compactAt: b.autoCompactThreshold,
  }
  contextText = `ctx ${b.percentage}%`
  paintStatus($)
  await update($, snap, () => next)
}

const refreshRuns = async ($: EngineInterface) => {
  const now: Run[] = (await $.agent.list()).map(({ id, type, description, status }) => ({ id, type, description, status }))

  if (JSON.stringify(now) !== JSON.stringify(await read($, runs))) {
    await update($, runs, () => now)
  }
}

const refreshAgentTypes = async ($: EngineInterface) => {
  const custom = (await $.session.usage({ breakdown: 'summary' })).context.breakdown?.agents ?? []
  const all = [...BUILT_IN, ...custom.map(a => ({ type: a.agentType, source: a.source }))]
  await update($, agentTypes, () => all)
}

const startAgent = async ($: EngineInterface, type: string) => {
  if (!task.trim()) {
    $.ui.toast('sidebar: type a task in the agents tab first')

    return
  }

  const spawned = await $.agent.spawn({ subagentType: type, prompt: task, description: task.slice(0, 40) })
  $.ui.toast(spawned.deny === undefined ? `Started ${type}` : `${type} refused: ${spawned.deny}`)
  await refreshRuns($)
}

const askDoubt = async ($: EngineInterface) => {
  await update($, doubt, () => 'Thinking it over…')
  const reply = await $.model.fork({ prompt: DOUBT_PROMPT })
  await update($, doubt, () => (reply.isAnswered ? reply.text : `No second opinion: ${reply.reason}.`))
}

const draftCommit = async ($: EngineInterface) => {
  const stat = (await $.process.run(['git', 'status', '--short'])).stdout.trim()

  if (!stat) {
    await update($, draft, () => ({ message: '', stat: '', result: 'Nothing to commit.' }))

    return
  }

  const diff = (await $.process.run(['git', 'diff', 'HEAD'])).stdout.slice(0, 12000)
  const reply = await $.model.complete({
    model: 'haiku',
    maxTokens: 200,
    prompt: `Write a git commit message for this change: one imperative subject line under 70 characters, then at most three short body lines only if they add something. No attribution lines, no code fences, nothing else.\n\n${stat}\n\n${diff}`,
  })
  await update($, draft, () => ({
    message: reply.isAnswered ? reply.text.trim() : '',
    stat,
    result: reply.isAnswered ? '' : `No draft: ${reply.reason}.`,
  }))
}

const commitAll = async ($: EngineInterface, message: string) => {
  await $.process.run(['git', 'add', '-A'])
  const ran = await $.process.run(['git', 'commit', '-m', message])
  const result = ran.exitCode === 0 ? (ran.stdout.trim().split('\n')[0] ?? 'Committed.') : `Commit failed: ${(ran.stderr || ran.stdout).trim().slice(0, 300)}`
  await update($, draft, now => ({ ...now, result }))
}

const tick = async ($: EngineInterface) => {
  const now = await $.clock.now()
  ticks += 1

  seen = seen.filter(([at]) => now - at <= WINDOW)

  const oldest = seen[0]?.[0] ?? now
  const newest = seen[seen.length - 1]?.[0] ?? 0
  const live =
    now - newest > 1_500 ? 0 : seen.reduce((sum, [, count]) => sum + count, 0) / charsPerToken / Math.max(1, (now - oldest) / 1000)

  await update($, rate, prev => {
    // Idle with nothing left to scroll off: no change, so no redraw.
    if (live === 0 && prev.live === 0 && prev.history.every(value => value === 0)) {
      return prev
    }

    return { ...prev, live, peak: Math.max(prev.peak, live), history: [...prev.history, live].slice(-SPARK) }
  })

  // Once a second: the cache countdown, written only when its text changes.
  if (ticks % 2 === 0) {
    const held = await read($, cache)
    const last = held.samples[held.samples.length - 1]

    if (last !== undefined) {
      const clock = clockOf(last.at + held.ttlMs - now)

      if (clock !== held.clock) {
        const total = last.read + last.write + last.fresh
        cacheText = `cache ${total === 0 ? 0 : Math.round((last.read / total) * 100)}% ${clock}`
        paintStatus($)
        await update($, cache, prev => ({ ...prev, clock }))
      }
    }
  }

  // Every four seconds: the agents' statuses.
  if (ticks % 8 === 0) {
    await refreshRuns($)
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'sidebar', description: `Open the sidebar, optionally on a tab: ${TABS.join(', ')}` })
    await $.command.register({ name: 'cache', description: 'Open the sidebar on the prompt-cache tab' })
    await $.command.register({ name: 'doubt', description: 'Get a second opinion against the last answer, off the record' })
    await $.command.register({ name: 'quick-commit', description: 'Draft a commit message for the working tree, then commit on one click' })
    void $.ui.open({ id: PANE, title: 'Sidebar', columns: DOCK_COLUMNS, rows: INLINE_ROWS })
    $.clock.every(TICK, () => void tick($))
    const started = await next(e)
    await snapshot($)
    await refreshAgentTypes($)

    return started
  })

  on('command.run', { command: 'sidebar' }, async ($, e) => {
    const word = e.args.trim().toLowerCase()

    if (isTab(word)) {
      await update($, tab, () => word)
    }

    await snapshot($)
    await refreshAgentTypes($)
    await $.ui.open({ id: PANE, title: 'Sidebar', columns: DOCK_COLUMNS, rows: INLINE_ROWS })

    return { text: 'Sidebar opened.' }
  })

  on('command.run', { command: 'cache' }, async $ => {
    await update($, tab, () => 'cache' as Tab)
    await $.ui.open({ id: PANE, title: 'Sidebar', columns: DOCK_COLUMNS, rows: INLINE_ROWS })

    return { text: 'Sidebar opened on cache.' }
  })

  on('command.run', { command: 'doubt' }, async $ => {
    await update($, tab, () => 'doubt' as Tab)
    await $.ui.open({ id: PANE, title: 'Sidebar', columns: DOCK_COLUMNS, rows: INLINE_ROWS })
    await askDoubt($)

    return { text: 'Second opinion is in the sidebar; the model does not see it.' }
  })

  on('command.run', { command: 'quick-commit' }, async $ => {
    await update($, tab, () => 'commit' as Tab)
    await draftCommit($)
    await $.ui.open({ id: PANE, title: 'Sidebar', columns: DOCK_COLUMNS, rows: INLINE_ROWS })

    return { text: 'Draft is in the sidebar.' }
  })

  on('prompt.submit', async ($, e, next) => {
    const text = e.text.trim()
    await update($, calls, () => [])

    if (text) {
      await update($, prompts, all => [...all.filter(one => one !== text), text].slice(-100))
    }

    return next(e)
  })

  on('turn.step', async function* ($, e, next) {
    // A subagent has its own prefix and its own stream: left out of every figure.
    if (e.agentId) {
      return yield* next(e)
    }

    const startedAt = await $.clock.now()
    let chars = 0
    let first: number | undefined
    let ended: number | undefined
    let usage: { model: string; input_tokens: number; output_tokens: number; cache_read_input_tokens: number; cache_creation_input_tokens: number } | null = null

    for await (const chunk of next(e)) {
      const count = chunk.kind === 'text' || chunk.kind === 'thinking' ? chunk.text.length : chunk.kind === 'input' ? chunk.json.length : 0

      if (count > 0) {
        const at = await $.clock.now()

        first ??= at
        ended = at
        chars += count
        seen.push([at, count])
      } else if (chunk.kind === 'stop') {
        usage = chunk.usage
      }

      yield chunk
    }

    if (usage === null) {
      return
    }

    const done = usage
    let session: number | undefined
    let isSubscription = false

    try {
      const used = await $.session.usage()
      session = used.cost?.usd
      // ponytail: a five-hour or weekly window under 100% means a subscription, whose cache
      // lives an hour; anything else gets five minutes. Env overrides and gateways are not read.
      isSubscription = used.rateLimits.some(l => (l.kind === 'five_hour' || l.kind === 'seven_day') && l.percentUsed < 100)
    } catch {
      // the pane just keeps its last total
    }

    const ttlMs = isSubscription ? 3_600_000 : 300_000
    const sample = { at: startedAt, model: done.model, read: done.cache_read_input_tokens, write: done.cache_creation_input_tokens, fresh: done.input_tokens }
    await update($, cache, prev => ({ samples: [...prev.samples, sample].slice(-30), ttlMs, clock: '' }))

    if (first === undefined || ended === undefined) {
      return
    }

    // From the first piece to the last, not from the request: the wait for the model is not output speed.
    const ms = Math.max(1, ended - first)

    if (done.output_tokens >= 50 && chars > 0) {
      charsPerToken = chars / done.output_tokens
    }

    const price = priceOf(done.model)
    const last: Last = {
      model: done.model,
      input: done.input_tokens + done.cache_read_input_tokens + done.cache_creation_input_tokens,
      cached: done.cache_read_input_tokens,
      output: done.output_tokens,
      ms,
      ...(price === undefined
        ? {}
        : {
            usd:
              (done.input_tokens * price[0] +
                done.output_tokens * price[1] +
                done.cache_read_input_tokens * price[2] +
                done.cache_creation_input_tokens * price[3]) /
              1e6,
          }),
    }

    await update($, rate, prev => ({
      ...prev,
      last,
      output: prev.output + done.output_tokens,
      ms: prev.ms + ms,
      ...(session === undefined ? {} : { usd: session }),
    }))
  })

  on('tool.call', async ($, e, next) => {
    const input = e as unknown as { command?: string; file_path?: string; pattern?: string; description?: string; new_string?: string; content?: string }
    const label = (input.file_path ?? input.command ?? input.pattern ?? input.description ?? '').split('\n')[0] ?? ''
    const call: Call = { id: e.tool_use_id, tool: e.tool, label, ms: null }
    const startedAt = await $.clock.now()
    await update($, calls, list => [...list, call].slice(-300))
    const ran = await next(e)
    const endedAt = await $.clock.now()
    await update($, calls, list => list.map(one => (one.id === call.id ? { ...one, ms: Math.round(endedAt - startedAt) } : one)))

    const file = input.file_path
    const hasWritten = (e.tool === 'Edit' || e.tool === 'Write') && file !== undefined && ran.deny === undefined && ran.isError !== true

    if (hasWritten) {
      await update($, edits, all => ({ ...all, [file]: (all[file] ?? 0) + 1 }))
      const mine = found(file, input.new_string ?? input.content ?? '')

      // A Write replaces the file, so its earlier TODOs are replaced too.
      if (mine.length > 0 || e.tool === 'Write') {
        await update($, todos, all => [...(e.tool === 'Write' ? all.filter(t => t.file !== file) : all), ...mine].slice(-100))
      }
    }

    if (e.tool === 'Agent') {
      await refreshRuns($)
    }

    // Context, live during a turn: at most once every 3s.
    if (endedAt - lastSnapAt > 3000) {
      await snapshot($)
    }

    return ran
  })

  on('turn.complete', async ($, e, next) => {
    const done = await next(e)
    await snapshot($)

    try {
      const status = await $.process.run(['git', 'status', '--porcelain'])
      const isDirty = status.exitCode === 0 && status.stdout.trim() !== ''

      if (isDirty && !hasToastedDirty) {
        $.ui.toast('Uncommitted changes: /quick-commit')
      }

      hasToastedDirty = isDirty
    } catch {
      // no git here: nothing to say
    }

    return done
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const table = $.ui.resolve(e)
    const { Box, Text, Button } = table
    const Svg = e.surface !== 'terminal' && 'Svg' in table ? table.Svg : undefined
    const Input = 'Input' in table ? table.Input : undefined
    const shown = await read($, tab)
    const { live, peak, history, last, output, ms, usd: session } = await read($, rate)
    const held = await read($, cache)
    const context = await read($, snap)
    const sample = held.samples[held.samples.length - 1]
    const prompt = sample === undefined ? 0 : sample.read + sample.write + sample.fresh
    const hit = sample === undefined || prompt === 0 ? 0 : sample.read / prompt
    const isExpired = held.clock === 'expired'
    const columns = e.props.bodyColumns
    const chartWidth = Math.max(60, (columns - 6) * 7)

    const row = (label: string, value: string, bold = false) => (
      <Box justifyContent="space-between" columnGap={2}>
        <Text dimColor>{label}</Text>
        <Text bold={bold}>{value}</Text>
      </Box>
    )

    const tile = (title: string, body: RenderChildren) => (
      <Box flexDirection="column" paddingX={1}>
        <Text dimColor>{title}</Text>
        {body}
      </Box>
    )

    const ring = (share: number, tone: string, alt: string) =>
      Svg === undefined ? null : <Svg source={ringOf(share, tone)} alt={alt} width={40} height={40} />

    // Inline above the prompt (not docked): one row, not tiles.
    if (e.props.placement === 'inline') {
      return (
        <Box columnGap={2}>
          <Text bold color={live > 0 ? GREEN : undefined}>
            {live > 0 ? `${Math.round(live)} tok/s` : 'idle'}
          </Text>
          <Text color={live > 0 ? GREEN : undefined} dimColor={live === 0}>
            {spark(history.slice(-12))}
          </Text>
          {context === null ? null : <Text color={heat(context.percent)}>{`ctx ${context.percent}%`}</Text>}
          {sample === undefined ? null : <Text color={isExpired ? RED : GREEN}>{`cache ${Math.round(hit * 100)}% ${held.clock}`}</Text>}
          <Text dimColor>{`session ${session === undefined ? '-' : usd(session)}`}</Text>
        </Box>
      )
    }

    // Rows a list may take: the body, less the tab bar, the tiles' headers and the gaps between them.
    const room = Math.max(3, e.props.scroll.bodyRows - 9)
    let tiles: RenderChildren

    if (shown === 'tokens') {
      tiles = [
        tile(
          'Output, live',
          <Box flexDirection="column">
            <Text bold color={live > 0 ? GREEN : undefined}>
              {live > 0 ? `${Math.round(live)} tok/s` : 'idle'}
            </Text>
            {Svg === undefined ? (
              <Text color={live > 0 ? GREEN : undefined} dimColor={live === 0}>
                {spark(history)}
              </Text>
            ) : (
              <Svg source={chartOf(history, chartWidth, 36, live > 0 ? GREEN : '#888')} alt="output tokens per second, last 20 seconds" width={chartWidth} height={36} />
            )}
          </Box>,
        ),
        tile(
          'Last response',
          last === undefined ? (
            <Text dimColor>No response yet.</Text>
          ) : (
            <Box alignItems="center" columnGap={2}>
              {last.input === 0 ? null : ring(last.cached / last.input, GREEN, 'share of input from the cache')}
              <Box flexDirection="column" flexGrow={1}>
                {row('input', `${tokens(last.input)} tok`, true)}
                {row('cached', last.input === 0 ? '-' : `${tokens(last.cached)} (${Math.round((last.cached / last.input) * 100)}%)`)}
                {row('output', `${tokens(last.output)} tok`)}
                {row('speed', `${Math.round(last.output / (last.ms / 1000))} tok/s over ${seconds(last.ms)}`)}
                {row('cost', last.usd === undefined ? 'no price for model' : usd(last.usd), true)}
              </Box>
            </Box>
          ),
        ),
        tile(
          'Session',
          <Box flexDirection="column">
            {row('output', `${tokens(output)} tok`)}
            {row('average', ms === 0 ? '-' : `${Math.round(output / (ms / 1000))} tok/s`)}
            {row('peak live', peak === 0 ? '-' : `${Math.round(peak)} tok/s`)}
            {row('cost', session === undefined ? '-' : usd(session), true)}
          </Box>,
        ),
      ]
    } else if (shown === 'cache') {
      tiles = [
        tile(
          'Requests',
          held.samples.length === 0 ? (
            <Text dimColor>No request yet.</Text>
          ) : (
            <Box flexDirection="column">
              {held.samples.slice(-Math.min(room, 8)).map(s => {
                const all = s.read + s.write + s.fresh

                return row(`read ${tokens(s.read)} · wrote ${tokens(s.write)}`, `${all === 0 ? 0 : Math.round((s.read / all) * 100)}%`)
              })}
            </Box>
          ),
        ),
        tile(
          'Prompt cache',
          sample === undefined ? (
            <Text dimColor>No request yet: the first one writes the cache.</Text>
          ) : (
            <Box alignItems="center" columnGap={2}>
              {ring(hit, isExpired ? RED : GREEN, 'share of the prompt read from the cache')}
              <Box flexDirection="column" flexGrow={1}>
                {row('read', `${tokens(sample.read)} (${Math.round(hit * 100)}%)`, true)}
                {row('wrote', tokens(sample.write))}
                {row('new', tokens(sample.fresh))}
                {row('expires in', `${held.clock || '-'} of ${held.ttlMs >= 3_600_000 ? '1h' : '5m'}`, true)}
                <Text color={isExpired ? RED : GREEN} wrap="wrap">
                  {!isExpired
                    ? 'warm: keep going'
                    : prompt >= COMPACT_AT
                      ? `expired: the next message rewrites ${tokens(prompt)} tokens. /compact first`
                      : 'expired: the next message rewrites the cache'}
                </Text>
              </Box>
            </Box>
          ),
        ),
      ]
    } else if (shown === 'context') {
      const listed = context === null ? [] : context.rows.filter(r => r.tokens > 0).sort((a, b) => b.tokens - a.tokens)

      tiles = [
        tile(
          'By category',
          context === null ? (
            <Text dimColor>No reading yet.</Text>
          ) : (
            <Box flexDirection="column">
              {listed.slice(0, room).map(r => (
                <Box justifyContent="space-between" columnGap={2}>
                  <Text dimColor={r.kind !== 'used'} wrap="truncate-end">
                    <Text color={r.color}>■</Text> {r.name}
                  </Text>
                  <Text dimColor={r.kind !== 'used'}>{tokens(r.tokens)}</Text>
                </Box>
              ))}
            </Box>
          ),
        ),
        tile(
          'Context window',
          context === null ? (
            <Text dimColor>Send a prompt first.</Text>
          ) : (
            <Box alignItems="center" columnGap={2}>
              {ring(context.percent / 100, heat(context.percent), 'share of the context window in use')}
              <Box flexDirection="column" flexGrow={1}>
                {row('used', `${context.percent}%`, true)}
                {row('tokens', `${tokens(context.total)} of ${tokens(context.max)}`)}
                {row('compacts at', context.compactAt === undefined ? 'off' : tokens(context.compactAt))}
                {row('model', context.model)}
              </Box>
            </Box>
          ),
        ),
      ]
    } else if (shown === 'turn') {
      const list = await read($, calls)
      const slowest = Math.max(1, ...list.map(c => c.ms ?? 0))

      tiles = [
        tile(
          'Tool calls',
          list.length === 0 ? (
            <Text dimColor>None this turn yet.</Text>
          ) : (
            <Box flexDirection="column">
              {list.slice(-room).map(c => (
                <Box justifyContent="space-between" columnGap={2}>
                  <Text wrap="truncate-end" color={c.ms !== null && c.ms === slowest && list.length > 1 ? AMBER : undefined}>
                    {c.tool} <Text dimColor>{c.label}</Text>
                  </Text>
                  <Text dimColor={c.ms === null}>{c.ms === null ? 'runs' : seconds(c.ms)}</Text>
                </Box>
              ))}
            </Box>
          ),
        ),
        tile(
          'This turn',
          <Box flexDirection="column">
            {row('calls', String(list.length), true)}
            {row('in tools', seconds(list.reduce((sum, c) => sum + (c.ms ?? 0), 0)))}
            {row('slowest', list.length === 0 ? '-' : seconds(slowest))}
          </Box>,
        ),
      ]
    } else if (shown === 'files') {
      const rows = Object.entries(await read($, edits)).sort((a, b) => b[1] - a[1])
      const hottest = rows[0]?.[1] ?? 1

      tiles = [
        tile(
          'Edited this session',
          rows.length === 0 ? (
            <Text dimColor>No edits yet.</Text>
          ) : (
            <Box flexDirection="column">
              {rows.slice(0, room).map(([path, n]) => (
                <Box justifyContent="space-between" columnGap={2}>
                  <Text wrap="truncate-start">{path.split('/').slice(-2).join('/')}</Text>
                  <Text color={n / hottest > 0.66 ? RED : n / hottest > 0.33 ? AMBER : GREEN}>{String(n)}</Text>
                </Box>
              ))}
            </Box>
          ),
        ),
        tile(
          'Edits',
          <Box flexDirection="column">
            {row('files', String(rows.length), true)}
            {row('edits', String(rows.reduce((sum, [, n]) => sum + n, 0)))}
          </Box>,
        ),
      ]
    } else if (shown === 'todos') {
      const all = await read($, todos)

      tiles = [
        tile(
          `TODOs written · ${all.length}`,
          all.length === 0 ? (
            <Text dimColor>None yet. Click one to have it resolved.</Text>
          ) : (
            <Box flexDirection="column">
              {all.slice(-Math.floor(room / 2)).map((t, i) => (
                <Box key={`todo-${i}`} flexDirection="column">
                  <Text wrap="truncate-start" dimColor>
                    {t.file.split('/').slice(-2).join('/')}
                  </Text>
                  <Button
                    key={`fix-${i}`}
                    plain
                    label={t.text}
                    onPress={async () => {
                      await update($, todos, list => list.filter(one => one.file !== t.file || one.text !== t.text))
                      void $.prompt.submit({ text: `Resolve this now, in ${t.file}: ${t.text}` })
                    }}
                  />
                </Box>
              ))}
            </Box>
          ),
        ),
      ]
    } else if (shown === 'prompts') {
      const all = await read($, prompts)
      const width = Math.max(10, columns - 8)

      tiles = [
        tile(
          `Prompts · ${all.length}`,
          all.length === 0 ? (
            <Text dimColor>None yet. Click one to reuse it.</Text>
          ) : (
            <Box flexDirection="column">
              {[...all]
                .reverse()
                .slice(0, room)
                .map((text, i) => {
                  const line = text.replace(/\s+/g, ' ')

                  return (
                    <Button
                      key={`prompt-${i}`}
                      plain
                      label={line.length > width ? `${line.slice(0, width - 1)}…` : line}
                      onPress={() => {
                        void $.prompt.fill({ text })
                      }}
                    />
                  )
                })}
            </Box>
          ),
        ),
      ]
    } else if (shown === 'agents') {
      const list = await read($, agentTypes)
      const all = await read($, runs)
      const running = (type: string) => all.filter(r => r.type === type && r.status === 'running').length

      tiles = [
        tile(
          'Runs',
          all.length === 0 ? (
            <Text dimColor>None yet.</Text>
          ) : (
            <Box flexDirection="column">
              {all.slice(-5).map(r => (
                <Box justifyContent="space-between" columnGap={2}>
                  <Text wrap="truncate-end" dimColor={r.status !== 'running'}>
                    {r.type} <Text dimColor>{r.description}</Text>
                  </Text>
                  <Text color={r.status === 'running' ? GREEN : r.status === 'failed' ? RED : undefined} dimColor={r.status !== 'running' && r.status !== 'failed'}>
                    {r.status}
                  </Text>
                </Box>
              ))}
            </Box>
          ),
        ),
        tile(
          `Agent types · ${list.length}`,
          <Box flexDirection="column">
            {Input === undefined ? null : (
              <Input
                key="task"
                label="task "
                placeholder="what should it do?"
                submitLabel="set"
                onInput={value => {
                  task = value
                }}
                onSubmit={value => {
                  task = value
                }}
              />
            )}
            {list.slice(0, Math.max(3, room - 8)).map((a, i) => (
              <Box key={`type-${i}`} justifyContent="space-between" columnGap={2}>
                <Button key={`start-${a.type}`} plain label={a.type} onPress={() => startAgent($, a.type)} />
                <Text color={running(a.type) > 0 ? GREEN : undefined} dimColor={running(a.type) === 0}>
                  {running(a.type) > 0 ? `${running(a.type)} running` : a.source}
                </Text>
              </Box>
            ))}
          </Box>,
        ),
      ]
    } else if (shown === 'doubt') {
      const text = await read($, doubt)
      const { Markdown } = table

      tiles = [
        tile(
          'Second opinion',
          <Box flexDirection="column">
            {text === '' ? <Text dimColor>Argues against the last answer. The model never sees it.</Text> : <Markdown text={text.slice(0, 10000)} />}
            <Button key="ask" variant="primary" label={text === '' ? 'Ask' : 'Ask again'} onPress={() => askDoubt($)} />
          </Box>,
        ),
      ]
    } else {
      const d = await read($, draft)

      tiles = [
        tile(
          'Commit',
          <Box flexDirection="column">
            {d.message === '' ? <Text dimColor>Drafts a message from the working tree.</Text> : <Text wrap="wrap">{d.message}</Text>}
            {d.stat === '' ? null : (
              <Text dimColor wrap="truncate-end">
                {d.stat.split('\n').slice(0, 6).join('\n')}
              </Text>
            )}
            {d.result === '' ? null : <Text color={d.result.startsWith('Commit failed') || d.result.startsWith('No draft') ? RED : GREEN}>{d.result}</Text>}
            <Box columnGap={2}>
              <Button key="draft" label={d.message === '' ? 'Draft' : 'Redraft'} onPress={() => draftCommit($)} />
              {d.message !== '' && d.result === '' ? <Button key="commit" variant="primary" label="Commit all" onPress={() => commitAll($, d.message)} /> : null}
            </Box>
          </Box>,
        ),
      ]
    }

    // Docked, the tiles gather at the bottom of the side, level with the prompt bar; the tabs sit under them.
    return (
      <Box flexDirection="column" justifyContent="flex-end" gap={1} height={e.props.scroll.bodyRows}>
        {tiles}
        <Box flexWrap="wrap" columnGap={2} paddingX={1}>
          {TABS.map(name => (
            <Button key={`tab-${name}`} plain label={name} dimColor={name !== shown} onPress={() => update($, tab, () => name)} />
          ))}
        </Box>
      </Box>
    )
  })
}
