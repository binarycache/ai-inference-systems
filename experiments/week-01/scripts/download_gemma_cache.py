"""Download google/gemma-3-270m into the Hugging Face cache (default: ~/.cache/huggingface)."""

from __future__ import annotations

import os
import sys

from huggingface_hub import get_token, snapshot_download

REPO_ID = "google/gemma-3-270m"


def main() -> None:
    token = os.environ.get("HF_TOKEN") or get_token()
    if not token:
        print(
            "No Hugging Face token found. Do one of:\n"
            "  - Set HF_TOKEN in the environment, or\n"
            "  - Run: huggingface-cli login\n"
            "Also accept the Gemma license on the model page:\n"
            f"  https://huggingface.co/{REPO_ID}",
            file=sys.stderr,
        )
        sys.exit(1)

    path = snapshot_download(repo_id=REPO_ID, repo_type="model", token=token)
    print(path)


if __name__ == "__main__":
    main()
