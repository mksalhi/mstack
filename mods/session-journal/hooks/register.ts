import type { Register } from 'claude-code'

let prompt = ''
let tools = 0
const files = new Set<string>()

export const register: Register = on => {
  on('prompt.submit', ($, e, next) => {
    prompt = e.text.trim().replace(/\s+/g, ' ').slice(0, 100)
    tools = 0
    files.clear()

    return next(e)
  })

  on('tool.call', ($, e, next) => {
    tools += 1
    const path = (e as unknown as { file_path?: string }).file_path

    if ((e.tool === 'Edit' || e.tool === 'Write') && path) {
      files.add(path.split('/').pop() ?? path)
    }

    return next(e)
  })

  on('turn.complete', async ($, e, next) => {
    const done = await next(e)

    const home = await $.env.get('HOME').catch(() => undefined)

    if (!prompt || !home) {
      return done
    }

    // Local time: shift by the zone offset, then read the ISO fields.
    const now = new Date(await $.clock.now())
    const local = new Date(now.getTime() - now.getTimezoneOffset() * 60_000).toISOString()
    const path = `${home}/.claude/journal/${local.slice(0, 10)}.md`
    const project = (await $.session.cwd()).split('/').pop()
    const edited = files.size > 0 ? ` · edited ${[...files].slice(0, 6).join(', ')}` : ''
    const before = (await $.fs.exists(path)) ? await $.fs.read(path) : `# ${local.slice(0, 10)}\n\n`
    await $.fs.write(path, `${before}- ${local.slice(11, 16)} **${project}** ${prompt} · ${tools} tool calls${edited}\n`)
    prompt = ''

    return done
  })
}
