import os

from src.gateway.model_gateway import check_reachability

REQUIRED_VARS = [
    "TELENAV_API_KEY",
]


def main() -> int:
    missing = [k for k in REQUIRED_VARS if not os.environ.get(k)]
    if missing:
        print(f"Missing env vars: {', '.join(missing)}")
        return 1

    reachable = check_reachability()
    print(f"Gateway reachable: {reachable}")
    print("ENV OK")
    return 0 if reachable else 2


if __name__ == "__main__":
    raise SystemExit(main())
