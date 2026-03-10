"""
Mia Labs Pre-Reasoning Engine — CLI Client
Thin wrapper around the public API. No engine code here.

Default action: show the API help guide (GET /help).
Start with --form to learn the grammar, then --analyze to run.

Usage:
    python engine.py                          # Show API help (start here)
    python engine.py --form                   # Grammar guide — signal words
    python engine.py --analyze "problem"      # Analyze problem text
    python engine.py --analyze-file path.txt  # Analyze from file
    python engine.py --submit "problem"       # URL-based submit (returns ID)
    python engine.py --recover ID             # Recover results by ID
    python engine.py --health                 # Engine status
    python engine.py --info                   # Engine metadata
"""
import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

API = "https://www.mia-labs.com/api/engine"
TIMEOUT = 30


def _get(endpoint):
    """GET request to engine API."""
    url = f"{API}/{endpoint}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _post(endpoint, data):
    """POST request to engine API."""
    url = f"{API}/{endpoint}"
    try:
        payload = json.dumps(data).encode("utf-8")
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body)
            detail = err.get("detail", body)
        except json.JSONDecodeError:
            detail = body
        print(f"HTTP {e.code}: {detail}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def _format_help(data):
    """Pretty-print the /help JSON response."""
    print(f"\n  {data.get('name', 'Pre-Reasoning Engine')}")
    print(f"  {data.get('tagline', '')}")
    print(f"  v{data.get('version', '?')}\n")

    if data.get("what"):
        print(f"  {data['what']}\n")

    if data.get("important"):
        print(f"  IMPORTANT: {data['important']}\n")

    if data.get("start_here"):
        print(f"  START HERE: {data['start_here']}\n")

    if data.get("quickstart"):
        print("  QUICKSTART:")
        for step in data["quickstart"]:
            print(f"    {step}")
        print()

    if data.get("endpoints"):
        print("  ENDPOINTS:")
        for endpoint, desc in data["endpoints"].items():
            print(f"    {endpoint:30s} {desc}")
        print()

    if data.get("output_structure"):
        print("  OUTPUT STRUCTURE:")
        for key, desc in data["output_structure"].items():
            print(f"    {key:20s} {desc}")
        print()

    if data.get("grounding_level") and isinstance(data["grounding_level"], dict):
        print("  GROUNDING LEVELS:")
        gl = data["grounding_level"]
        for level in ["grounding", "enhancing", "unlocking", "humanly_grounded"]:
            if level in gl:
                print(f"    {level:20s} {gl[level]}")
        print()

    if data.get("writing_tips"):
        print("  WRITING TIPS:")
        for tip in data["writing_tips"]:
            print(f"    - {tip}")
        print()

    print(f"  API base: {API}")
    print(f"  CLI:      python engine.py --form | --analyze | --submit | --recover | --health | --info\n")


def cmd_help():
    """Fetch and display the API help guide (GET /help)."""
    data = _get("help")
    _format_help(data)


def cmd_form():
    """Fetch the grammar guide — signal words and patterns (GET /form)."""
    data = _get("form")
    if isinstance(data, dict):
        print(json.dumps(data, indent=2))
    else:
        print(data)


def cmd_analyze(text):
    """Analyze problem text (POST /analyze)."""
    if len(text.strip()) < 10:
        print("Error: input too short (min 10 chars)", file=sys.stderr)
        sys.exit(1)
    if len(text) > 10000:
        print("Error: input too long (max 10,000 chars)", file=sys.stderr)
        sys.exit(1)

    result = _post("analyze", {"text": text})

    print(result.get("trace", "(no trace returned)"))
    print()

    meta = []
    if "n_blocks" in result:
        meta.append(f"blocks={result['n_blocks']}")
    if "grounding_level" in result:
        meta.append(f"grounding={result['grounding_level']}")
    if "has_cycles" in result:
        meta.append(f"cycles={'yes' if result['has_cycles'] else 'no'}")
    if "root_blockers" in result:
        meta.append(f"root_blockers={len(result['root_blockers'])}")
    if "critical_path_length" in result:
        meta.append(f"critical_path={result['critical_path_length']}")
    if "l1_enhanced" in result:
        meta.append(f"llm_enhanced={'yes' if result['l1_enhanced'] else 'no'}")
    if meta:
        print(f"[{', '.join(meta)}]")


def cmd_submit(text):
    """Submit via URL-based flow — no POST needed (GET /submit?text=...)."""
    if len(text.strip()) < 10:
        print("Error: input too short (min 10 chars)", file=sys.stderr)
        sys.exit(1)
    encoded = urllib.parse.quote(text[:10000])
    data = _get(f"submit?text={encoded}")
    if "recover_id" in data:
        print(f"Submitted. Recover ID: {data['recover_id']}")
        print(f"Retrieve with: python engine.py --recover {data['recover_id']}")
    if "trace" in data:
        print()
        print(data["trace"])


def cmd_recover(recover_id):
    """Recover results from a previous /submit call (GET /recover/ID)."""
    data = _get(f"recover/{recover_id}")
    if "trace" in data:
        print(data["trace"])
        print()
        meta = []
        if "n_blocks" in data:
            meta.append(f"blocks={data['n_blocks']}")
        if "grounding_level" in data:
            meta.append(f"grounding={data['grounding_level']}")
        if meta:
            print(f"[{', '.join(meta)}]")
    else:
        print(json.dumps(data, indent=2))


def cmd_health():
    """Check engine status (GET /health)."""
    data = _get("health")
    print(f"Status: {data.get('status', '?')}")
    print(f"Engine: {data.get('engine', '?')}")
    print(f"Version: {data.get('version', '?')}")


def cmd_info():
    """Get engine metadata (GET /info)."""
    data = _get("info")
    print(json.dumps(data, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="Mia Labs Pre-Reasoning Engine CLI — run with no args to see the full API guide",
        add_help=False,
    )
    parser.add_argument("--analyze", type=str, help="Problem text to analyze (POST /analyze)")
    parser.add_argument("--analyze-file", type=str, help="File containing problem text")
    parser.add_argument("--submit", type=str, help="URL-based submit, returns recover ID (GET /submit)")
    parser.add_argument("--recover", type=str, help="Recover results by ID (GET /recover/ID)")
    parser.add_argument("--form", action="store_true", help="Grammar guide — signal words (GET /form)")
    parser.add_argument("--health", action="store_true", help="Check engine status (GET /health)")
    parser.add_argument("--info", action="store_true", help="Get engine metadata (GET /info)")
    parser.add_argument("--help", action="store_true", help="Show full API guide (GET /help)")

    args = parser.parse_args()

    # Default: fetch and display the API help guide
    if args.help or len(sys.argv) == 1:
        cmd_help()
    elif args.form:
        cmd_form()
    elif args.analyze:
        cmd_analyze(args.analyze)
    elif args.analyze_file:
        try:
            with open(args.analyze_file, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError:
            print(f"File not found: {args.analyze_file}", file=sys.stderr)
            sys.exit(1)
        cmd_analyze(text)
    elif args.submit:
        cmd_submit(args.submit)
    elif args.recover:
        cmd_recover(args.recover)
    elif args.health:
        cmd_health()
    elif args.info:
        cmd_info()
    else:
        cmd_help()


if __name__ == "__main__":
    main()
