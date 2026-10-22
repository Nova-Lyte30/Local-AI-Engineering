"""Probe a local llama.cpp router with a reproducible long-context lookup task."""

import argparse
import json
import urllib.error
import urllib.request


LOCAL_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def post(base_url: str, endpoint: str, payload: dict, timeout: int = 180) -> dict:
    request = urllib.request.Request(
        base_url + endpoint,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    with LOCAL_OPENER.open(request, timeout=timeout) as response:
        return json.load(response)


def value(index: int) -> str:
    return f"K{(index * 7919 + 17) % 100000:05d}"


def make_prompt(filler_count: int) -> str:
    records = [
        f"R{index:03d} | lookup_value={value(index)} | department=D{index % 17:02d}"
        for index in range(1, 251)
    ]
    halfway = len(records) // 2
    filler = " blue" * filler_count
    return (
        "Read the indexed records. Ignore the filler paragraph. Find lookup_value "
        "for R001, R125, and R250 in that order. Reply with only their three "
        "values separated by one space.\n"
        + "\n".join(records[:halfway])
        + "\nFILLER START\n"
        + filler
        + "\nFILLER END\n"
        + "\n".join(records[halfway:])
        + "\nAnswer:"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--target-tokens", type=int, default=16180)
    parser.add_argument("--max-output", type=int, default=64)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    if args.target_tokens < 1:
        parser.error("--target-tokens must be positive")
    if args.max_output < 1:
        parser.error("--max-output must be positive")
    base_url = f"http://127.0.0.1:{args.port}"
    expected = " ".join(value(i) for i in (1, 125, 250))

    def token_count(filler_count: int) -> int:
        response = post(
            base_url,
            "/tokenize",
            {"model": args.model, "content": make_prompt(filler_count)},
        )
        return len(response["tokens"])

    minimum_tokens = token_count(0)
    if minimum_tokens > args.target_tokens:
        parser.error(
            f"--target-tokens must be at least {minimum_tokens} for the fixed records"
        )

    lo, hi = 0, args.target_tokens
    while lo < hi:
        middle = (lo + hi + 1) // 2
        if token_count(middle) <= args.target_tokens:
            lo = middle
        else:
            hi = middle - 1
    prompt = make_prompt(lo)
    count = token_count(lo)
    result = post(
        base_url,
        "/v1/chat/completions",
        {
            "model": args.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": args.max_output,
            "temperature": 0,
            "stream": False,
        },
        timeout=600,
    )
    choice = result["choices"][0]
    actual = choice["message"].get("content") or ""
    print(
        json.dumps(
            {
                "model": result.get("model"),
                "tokenized_content": count,
                "filler_count": lo,
                "prompt_tokens": result["usage"]["prompt_tokens"],
                "completion_tokens": result["usage"]["completion_tokens"],
                "finish_reason": choice.get("finish_reason"),
                "expected": expected,
                "actual": actual,
                "exact_match": actual.strip() == expected,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as error:
        print(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')}")
        raise SystemExit(1) from error
