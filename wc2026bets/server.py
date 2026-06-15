#!/usr/bin/env python3
"""
GROUNDTRUTH results backend.
Fetches finished 2026 World Cup matches and serves them to the web app so the
"Sync latest results" button can update ratings and predictions automatically.

WHAT IT DOES
  GET /health   -> {"ok": true, "source": "...", "key": true/false}
  GET /results  -> {"results": [{home, away, home_goals, away_goals, group, utcDate}, ...]}
  POST /scout   -> optional LLM scout (keeps your LLM key server-side). Body:
                   {home, away, home_notes, away_notes}
                   -> {home_adjust, away_adjust, home_reason, away_reason}

DATA SOURCE (free)
  Uses football-data.org v4, competition "WC". Get a free token at
  football-data.org/client/register and set it as an environment variable:
      Windows (PowerShell):  setx FOOTBALL_DATA_KEY "your_token_here"
      (then open a NEW terminal)
  World Cup is on football-data.org's free tier. If you prefer another source,
  replace fetch_results() below; just return the same list shape.

OPTIONAL LLM SCOUT (server-side key)
  Set ONE of these to enable POST /scout:
      OPENROUTER_API_KEY   (uses openrouter.ai, model from OPENROUTER_MODEL,
                            default openai/gpt-4o-mini)
      ANTHROPIC_API_KEY    (uses Anthropic, model claude-sonnet-4-6)
  If neither is set, /scout returns an error and the app's paste mode still works.

RUN
  python server.py        (or double-click run_groundtruth_live.bat)
  Then in the app: Scout -> Settings -> Results backend URL = http://localhost:8787
  Uses only the Python standard library. No pip install needed.
"""
import os, json, urllib.request, urllib.error
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = 8787
FD_KEY = os.environ.get("FOOTBALL_DATA_KEY", "")
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OR_MODEL = os.environ.get("OPENROUTER_MODEL", "openai/gpt-4o-mini")
ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# Map data-source names -> the app's canonical team names.
NAME_MAP = {
    "Korea Republic": "South Korea", "South Korea": "South Korea",
    "Republic of Korea": "South Korea",
    "Côte d'Ivoire": "Ivory Coast", "Cote d'Ivoire": "Ivory Coast",
    "IR Iran": "Iran", "Iran": "Iran",
    "Czech Republic": "Czechia", "Czechia": "Czechia",
    "United States": "USA", "USA": "USA", "United States of America": "USA",
    "Türkiye": "Turkey", "Turkiye": "Turkey", "Turkey": "Turkey",
    "Cabo Verde": "Cape Verde", "Cape Verde": "Cape Verde",
    "Bosnia-Herzegovina": "Bosnia and Herzegovina",
    "Bosnia and Herzegovina": "Bosnia and Herzegovina",
    "DR Congo": "DR Congo", "Congo DR": "DR Congo",
    "Curacao": "Curaçao", "Curaçao": "Curaçao",
}
def canon(name):
    return NAME_MAP.get(name, name)


def fetch_results():
    """Return finished WC 2026 matches in the app's shape."""
    if not FD_KEY:
        return {"error": "FOOTBALL_DATA_KEY not set. See setup at top of server.py."}
    url = "https://api.football-data.org/v4/competitions/WC/matches?status=FINISHED"
    req = urllib.request.Request(url, headers={"X-Auth-Token": FD_KEY})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": f"football-data {e.code}: {e.read().decode()[:160]}"}
    except Exception as e:
        return {"error": str(e)}
    out = []
    for m in data.get("matches", []):
        ft = (m.get("score") or {}).get("fullTime") or {}
        hg, ag = ft.get("home"), ft.get("away")
        if hg is None or ag is None:
            continue
        out.append({
            "home": canon((m.get("homeTeam") or {}).get("name", "")),
            "away": canon((m.get("awayTeam") or {}).get("name", "")),
            "home_goals": hg, "away_goals": ag,
            "group": (m.get("group") or "").replace("GROUP_", ""),
            "utcDate": m.get("utcDate", ""),
        })
    return {"results": out}


SCOUT_PROMPT = """You are a football scout. Convert qualitative team news into a small Elo rating adjustment for ONE upcoming match.
Match: {home} vs {away}.
{home} news: {hn}
{away} news: {an}
Output ONLY valid JSON, no prose. Each adjustment is an integer from -45 to 45 (negative = weaker for this match, positive = stronger). Be conservative; most within +-20; use 0 if no meaningful news.
JSON: {{"home_adjust": <int>, "away_adjust": <int>, "home_reason": "<=12 words", "away_reason": "<=12 words"}}"""

def run_scout(body):
    prompt = SCOUT_PROMPT.format(home=body.get("home", "Home"), away=body.get("away", "Away"),
                                 hn=body.get("home_notes", "").strip() or "(none)",
                                 an=body.get("away_notes", "").strip() or "(none)")
    if OR_KEY:
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
            data=json.dumps({"model": OR_MODEL, "max_tokens": 400,
                "response_format": {"type": "json_object"},
                "messages": [{"role": "user", "content": prompt}]}).encode(),
            headers={"Authorization": "Bearer " + OR_KEY, "Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=40) as r:
            d = json.loads(r.read())
        txt = d["choices"][0]["message"]["content"]
    elif ANTHROPIC_KEY:
        req = urllib.request.Request("https://api.anthropic.com/v1/messages",
            data=json.dumps({"model": "claude-sonnet-4-6", "max_tokens": 400,
                "messages": [{"role": "user", "content": prompt}]}).encode(),
            headers={"x-api-key": ANTHROPIC_KEY, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"})
        with urllib.request.urlopen(req, timeout=40) as r:
            d = json.loads(r.read())
        txt = "".join(b.get("text", "") for b in d.get("content", []) if b.get("type") == "text")
    else:
        return {"error": "No LLM key set (OPENROUTER_API_KEY or ANTHROPIC_API_KEY)."}
    return json.loads(txt.replace("```json", "").replace("```", "").strip())


class H(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    def _send(self, code, obj):
        b = json.dumps(obj).encode()
        self.send_response(code); self.send_header("Content-Type", "application/json")
        self._cors(); self.send_header("Content-Length", str(len(b))); self.end_headers()
        self.wfile.write(b)
    def do_OPTIONS(self):
        self.send_response(204); self._cors(); self.end_headers()
    def do_GET(self):
        if self.path.startswith("/health"):
            self._send(200, {"ok": True, "source": "football-data.org/WC", "key": bool(FD_KEY)})
        elif self.path.startswith("/results"):
            self._send(200, fetch_results())
        else:
            self._send(404, {"error": "not found"})
    def do_POST(self):
        if not self.path.startswith("/scout"):
            return self._send(404, {"error": "not found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            self._send(200, run_scout(json.loads(self.rfile.read(n) or b"{}")))
        except Exception as e:
            self._send(200, {"error": str(e)})
    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"GROUNDTRUTH backend on http://localhost:{PORT}")
    print("football-data key:", "set" if FD_KEY else "MISSING (set FOOTBALL_DATA_KEY)")
    print("LLM scout:", "OpenRouter" if OR_KEY else "Anthropic" if ANTHROPIC_KEY else "off")
    print("In the app: Scout -> Settings -> Results backend URL = http://localhost:%d" % PORT)
    print("Leave this window open. Ctrl+C to stop.")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
