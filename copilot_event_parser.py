#!/usr/bin/env python3
import argparse
import json
import pathlib
import sys


def _iter_events(path: pathlib.Path):
    with path.open("r", encoding="utf-8") as handle:
        for line_number, raw in enumerate(handle, start=1):
            if not raw.strip():
                continue
            try:
                value = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"event on line {line_number} must be an object")
            yield value


def resolve_model(path: pathlib.Path) -> str:
    observed = set()
    for event in _iter_events(path):
        event_type = event.get("type")
        data = event.get("data")
        if not isinstance(data, dict):
            continue

        model = None
        if event_type == "session.auto_mode_resolved":
            model = data.get("chosenModel")
        elif event_type in {"model.call_start", "assistant.message"}:
            model = data.get("model")

        if model is not None:
            if not isinstance(model, str) or not model.strip():
                raise ValueError(f"{event_type} contains an invalid model identifier")
            observed.add(model.strip())

    if len(observed) != 1:
        rendered = ", ".join(sorted(observed)) or "none"
        raise ValueError(f"expected exactly one actual model, observed: {rendered}")
    return next(iter(observed))


def attest_runtime(path: pathlib.Path) -> dict:
    model = resolve_model(path)
    efforts = set()
    tool_sets = set()
    tool_calls = 0

    for event in _iter_events(path):
        event_type = event.get("type")
        data = event.get("data")
        if not isinstance(data, dict):
            continue

        if event_type == "tool.execution_start":
            tool_calls += 1
            continue

        if event_type != "session.usage_checkpoint":
            continue

        states = data.get("promptCacheBreakState")
        if not isinstance(states, list):
            continue
        for state in states:
            if not isinstance(state, dict):
                continue
            models = state.get("models")
            if not isinstance(models, dict):
                continue
            for record in models.values():
                if not isinstance(record, dict) or record.get("model") != model:
                    continue
                effort = record.get("reasoning_effort")
                if effort is not None:
                    if not isinstance(effort, str) or not effort.strip():
                        raise ValueError("usage checkpoint contains an invalid reasoning effort")
                    efforts.add(effort.strip())

                tools = record.get("tools")
                if tools is not None:
                    if not isinstance(tools, list):
                        raise ValueError("usage checkpoint tools must be a list")
                    names = []
                    for tool in tools:
                        if not isinstance(tool, dict):
                            raise ValueError("usage checkpoint tool entry must be an object")
                        name = tool.get("name")
                        if not isinstance(name, str) or not name.strip():
                            raise ValueError("usage checkpoint contains an invalid tool name")
                        names.append(name.strip())
                    if len(names) != len(set(names)):
                        raise ValueError("usage checkpoint tool set contains duplicates")
                    tool_sets.add(tuple(sorted(names)))

    if len(efforts) != 1:
        rendered = ", ".join(sorted(efforts)) or "none"
        raise ValueError(f"expected exactly one actual reasoning effort, observed: {rendered}")
    if len(tool_sets) != 1:
        rendered = "; ".join(",".join(tool_set) for tool_set in sorted(tool_sets)) or "none"
        raise ValueError(f"expected exactly one actual tool set, observed: {rendered}")

    return {
        "model": model,
        "reasoning_effort": next(iter(efforts)),
        "tool_calls": tool_calls,
        "tool_set": list(next(iter(tool_sets))),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    resolve = subparsers.add_parser("resolve-model")
    resolve.add_argument("events", type=pathlib.Path)
    resolve.add_argument("--json", action="store_true")

    attest = subparsers.add_parser("attest-runtime")
    attest.add_argument("events", type=pathlib.Path)
    attest.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)
    try:
        if args.command == "resolve-model":
            result = {"model": resolve_model(args.events)}
        else:
            result = attest_runtime(args.events)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, sort_keys=True))
    elif args.command == "resolve-model":
        print(result["model"])
    else:
        print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
