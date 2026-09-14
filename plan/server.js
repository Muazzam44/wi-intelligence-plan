#!/usr/bin/env node
/* Optional local server for the spec-driven-planner control board — STATEFUL mode.
 *
 *   node server.js            # then open http://localhost:4173/board.html
 *
 * file:// works fine for read-only viewing. Run this only when you want the board to
 * PERSIST edits (decision-wizard answers, status overrides). It:
 *   - serves this plan/ directory,
 *   - GET  /overrides         -> returns board-overrides.json (or {}),
 *   - POST /save              -> writes board-overrides.json (the board's saved state),
 *   - POST /commit-decisions  -> APPENDS resolved wizard decisions to registers/decisions.md
 *                                (append-only + idempotent by open-item id; promote to full ADRs as needed).
 * board-overrides.json is a sidecar; it never rewrites plan.json or the module specs
 * (those stay the single source of truth — regenerate with plan_lint.py --board).
 * /commit-decisions is the ONE opt-in write-back into the plan source (decisions.md only).
 */
/* Dynamic built-in imports keep this generated .js launcher runnable in both
 * CommonJS repositories and repositories whose nearest package.json declares
 * `"type": "module"`. The documented entrypoint remains `node server.js`. */
(async function main() {
const [httpModule, fsModule, pathModule, urlModule, childProcessModule] = await Promise.all([
  import("node:http"), import("node:fs"), import("node:path"), import("node:url"), import("node:child_process"),
]);
const http = httpModule.default, fs = fsModule.default, path = pathModule.default, url = urlModule.default;
const { spawnSync } = childProcessModule;
const ROOT = path.dirname(path.resolve(process.argv[1])), PORT = Number(process.env.PORT || 4173);
let boundPort = PORT;
const MIME = { ".html": "text/html", ".json": "application/json", ".js": "text/javascript",
  ".css": "text/css", ".md": "text/markdown", ".svg": "image/svg+xml", ".png": "image/png" };
const OVERRIDES = path.join(ROOT, "board-overrides.json");

function isWithinRoot(candidate) {
  const relative = path.relative(ROOT, candidate);
  return relative === "" || (relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative));
}

/* Crash-safe write: tmp sibling + rename, so a crash mid-write never leaves a torn
 * overrides file / register / module spec behind. */
function writeAtomic(p, data) {
  const tmp = p + ".tmp";
  fs.writeFileSync(tmp, data);
  fs.renameSync(tmp, p);
}

/* Plan activity derived from git history (read-only). Every status flip is a front-matter edit,
 * so `git log -p -- modules` IS the real build history — no side event log to maintain.
 * Gracefully returns {events: []} when git or a repo is absent. Cached briefly (?force=1 bypasses).
 * Each git call carries a hard timeout so a pathological repo can never freeze the server. */
const STATUS_VOCAB = new Set(["draft", "spec-approved", "in-progress", "implementation-verified",
  "blocked-needs-decision", "needs-revalidation", "superseded"]);
const FM_MAX_LINE = 40;  // front-matter heuristic: a status: line this deep is body text, not front matter
let _histCache = null, _histAt = 0;
function gitHistory(force) {
  const now = Date.now();
  if (!force && _histCache && now - _histAt < 10000) return _histCache;
  const git = (args) => spawnSync("git", args,
    { cwd: ROOT, encoding: "utf8", maxBuffer: 8 * 1024 * 1024, timeout: 8000, killSignal: "SIGKILL" });
  const out = { events: [] };
  try {
    const probe = git(["rev-parse", "--is-inside-work-tree"]);
    if (probe.error || probe.status !== 0 || !/true/.test(probe.stdout || "")) {
      out.note = "not a git repo (or git unavailable/timed out)"; _histCache = out; _histAt = now; return out;
    }
    // commits touching the plan dir
    const lg = git(["log", "-n", "80", "--date=iso-strict", "--format=%H%x09%ad%x09%s", "--", "."]);
    if (lg.error) out.note = "git log failed: " + lg.error.message;
    (lg.stdout || "").split("\n").forEach(line => {
      const [h, ad, ...s] = line.split("\t");
      if (h && ad) out.events.push({ at: ad, kind: "commit", title: s.join("\t"), meta: "commit " + h.slice(0, 7) });
    });
    // Status flips parsed from front-matter diffs under modules/. --unified=0 hunk headers give
    // exact new-file line numbers, so a status: inside a Markdown BODY (line > FM_MAX_LINE) or a
    // value outside the status vocabulary is rejected — body YAML examples don't fake events.
    const lp = git(["log", "-n", "80", "--date=iso-strict", "--format=C%x09%H%x09%ad%x09%s",
                    "-p", "--unified=0", "--no-textconv", "--", "modules"]);
    let at = "", file = "", from = "", newLine = 0;
    (lp.stdout || "").split("\n").forEach(line => {
      if (line.startsWith("C\t")) { const p = line.split("\t"); at = p[2] || ""; from = ""; return; }
      let m;
      if ((m = line.match(/^\+\+\+ b\/.*?([^\/]+)\.md$/))) { file = m[1]; from = ""; newLine = 0; return; }
      // @@ resets the pair state — a -status in one hunk must never pair with a +status in another
      if ((m = line.match(/^@@ -\d+(?:,\d+)? \+(\d+)/))) { newLine = parseInt(m[1], 10); from = ""; return; }
      // STRICT adjacency: `from` is a candidate ONLY for the immediately following line. Any
      // other diff line (another deletion, a context line, blank) clears it, so a `-status`,
      // then a `-body`, then a `+status` cannot pair across the gap.
      if ((m = line.match(/^-status:\s*(.+)$/))) { from = m[1].trim(); return; }
      if (line.startsWith("+") && !line.startsWith("+++")) {
        // a status EVENT needs a real transition: an ADJACENT -status/+status replacement pair
        // (with -U0 a front-matter flip is exactly that), both values in the vocabulary, near
        // the top of the file. A body example merely ADDING a status: line has no old value.
        // Residual known limit: an adjacent col-0 vocab-to-vocab edit inside a body code fence
        // in the first ~40 lines can still fabricate — diff-level parsing cannot see the
        // front-matter delimiters with -U0; the feed is display-only, so this is accepted.
        if ((m = line.match(/^\+status:\s*(.+)$/)) && file && from && newLine > 0 && newLine <= FM_MAX_LINE) {
          const to = m[1].trim();
          if (STATUS_VOCAB.has(to) && STATUS_VOCAB.has(from) && from !== to)
            out.events.push({ at, kind: "status", title: `${file}: ${from} → ${to}`, meta: "status · via git" });
        }
        from = "";   // consume the pending -status — pairing must be immediately adjacent
        newLine++; return;
      }
      from = "";   // ANY other line (a second -status, context, blank) breaks adjacency
    });
    out.events.sort((a, b) => String(b.at).localeCompare(String(a.at)));
    out.events = out.events.slice(0, 200);
  } catch (e) { out.note = String(e && e.message || e); }
  _histCache = out; _histAt = now;
  return out;
}

/* generation stamp baked into board.html at generation time (meta sdp-stamp) — the board
 * compares its own stamp against the served file's, immune to the initial-load mtime race. */
function boardStamp() {
  try {
    const fd = fs.openSync(path.join(ROOT, "board.html"), "r");
    const buf = Buffer.alloc(4096);
    const n = fs.readSync(fd, buf, 0, 4096, 0);
    fs.closeSync(fd);
    const m = buf.toString("utf8", 0, n).match(/name="sdp-stamp" content="([^"]*)"/);
    return m ? m[1] : "";
  } catch (e) { return ""; }
}

const server = http.createServer((req, res) => {
  const u = url.parse(req.url, true);
  if (req.method === "POST" && u.pathname === "/save") {
    let body = ""; req.on("data", c => (body += c)); req.on("end", () => {
      try { JSON.parse(body || "{}"); writeAtomic(OVERRIDES, body || "{}");
        res.writeHead(200, { "Content-Type": "application/json" }); res.end('{"ok":true}'); }
      catch (e) { res.writeHead(400); res.end(String(e)); }
    }); return;
  }
  if (u.pathname === "/overrides") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(fs.existsSync(OVERRIDES) ? fs.readFileSync(OVERRIDES) : "{}"); return;
  }
  if (u.pathname === "/status") {
    // liveness contract for the board: which dir this server serves, the board file's mtime,
    // and its embedded generation stamp. The board polls this and reloads itself when a regen
    // lands (auto-refresh); showing servedFrom makes a stale/wrong tab self-evident.
    let mtime = 0;
    try { mtime = fs.statSync(path.join(ROOT, "board.html")).mtimeMs; } catch (e) {}
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify({ servedFrom: ROOT, boardMtime: mtime, boardStamp: boardStamp(), port: boundPort })); return;
  }
  if (u.pathname === "/history") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(gitHistory(!!(u.query && u.query.force)))); return;
  }
  if (req.method === "POST" && u.pathname === "/commit-decisions") {
    let body = ""; req.on("data", c => (body += c)); req.on("end", () => {
      try {
        const dec = (JSON.parse(body || "{}").decisions) || {};
        const file = path.join(ROOT, "registers", "decisions.md");
        let md = fs.existsSync(file) ? fs.readFileSync(file, "utf8") : "# Decisions\n";
        const HEAD = "## Board-captured decisions";
        if (md.indexOf(HEAD) === -1)
          md += `\n\n${HEAD}\n\nResolved via the planning board's decision wizard. Promote to full ADRs as needed.\n\n| Open item | Decision | Status |\n|-----------|----------|--------|\n`;
        let added = 0;
        Object.keys(dec).forEach(id => {
          const d = dec[id];
          if (!d || d.status !== "resolved" || !d.note) return;
          if (md.indexOf(`| ${id} |`) !== -1) return; // idempotent
          md += `| ${id} | ${String(d.note).replace(/\|/g, "\\|").replace(/\r?\n/g, " ")} | resolved |\n`; added++;
        });
        writeAtomic(file, md);
        res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify({ ok: true, added }));
      } catch (e) { res.writeHead(400); res.end(String(e)); }
    }); return;
  }
  if (req.method === "POST" && u.pathname === "/commit-module") {
    let body = ""; req.on("data", c => (body += c)); req.on("end", () => {
      try {
        const d = JSON.parse(body || "{}");
        const rel = String(d.file || ("modules/" + d.id + ".md")).replace(/\\/g, "/");
        const fp = path.normalize(path.join(ROOT, rel));
        if (!isWithinRoot(fp) || !fs.existsSync(fp)) { res.writeHead(404); res.end("module file not found"); return; }
        let t = fs.readFileSync(fp, "utf8");
        const fmMatch = t.match(/^---\r?\n([\s\S]*?)\r?\n---/);   // tolerate CRLF — Windows editors produce it
        if (!fmMatch) { res.writeHead(400); res.end("no front-matter in module file"); return; }
        let fm = fmMatch[1];
        const wf = d.workflow || {};
        const wfStr = `workflow: {wip: ${!!wf.wip}, impl: ${!!wf.impl}, verify: ${!!wf.verify}, review: ${!!wf.review}}`;
        const notes = String(d.notes || "").replace(/\r?\n/g, " ").replace(/"/g, '\\"');
        const setKey = (block, key, line) => {
          const re = new RegExp("^" + key + ":.*$", "m");
          return re.test(block) ? block.replace(re, line) : block.replace(/\s*$/, "") + "\n" + line;
        };
        if (d.status) fm = setKey(fm, "status", `status: ${d.status}`);
        fm = setKey(fm, "workflow", wfStr);
        fm = setKey(fm, "tracker_notes", `tracker_notes: "${notes}"`);
        t = t.replace(/^---\r?\n[\s\S]*?\r?\n---/, "---\n" + fm + "\n---");
        writeAtomic(fp, t);
        res.writeHead(200, { "Content-Type": "application/json" }); res.end(JSON.stringify({ ok: true, file: rel }));
      } catch (e) { res.writeHead(400); res.end(String(e)); }
    }); return;
  }
  let p = path.normalize(path.join(ROOT, decodeURIComponent(u.pathname)));
  if (u.pathname === "/" || u.pathname === "") p = path.join(ROOT, "board.html");
  if (!isWithinRoot(p)) { res.writeHead(403); res.end("forbidden"); return; }
  fs.readFile(p, (e, data) => {
    if (e) { res.writeHead(404); res.end("not found"); }
    else { res.writeHead(200, { "Content-Type": MIME[path.extname(p)] || "application/octet-stream" }); res.end(data); }
  });
});
server.listen(PORT, "127.0.0.1", () => { // loopback ONLY — a dev tool exposing paths + git history must never bind the LAN
  const address = server.address();
  boundPort = address && typeof address === "object" ? address.port : PORT;
  console.log(`spec-driven-planner board (stateful) → http://localhost:${boundPort}/board.html  (Ctrl+C to stop)`);
});
})().catch(error => { console.error(error); process.exitCode = 1; });
