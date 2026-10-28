"""Download a test video only after verifying the URL and its terms of use."""
import argparse
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True, help="Direct video URL with permitted download/use")
    parser.add_argument("--filename", default="qsr_test_video.mp4")
    args = parser.parse_args()
    parsed = urlparse(args.url)
    if parsed.scheme != "https":
        raise SystemExit("Only HTTPS URLs are accepted by this helper.")
    target = Path("videos/input") / Path(args.filename).name
    target.parent.mkdir(parents=True, exist_ok=True)
    request = Request(args.url, headers={"User-Agent": "QSR-Queue-Management-System/1.0"})
    with urlopen(request, timeout=30) as response, target.open("wb") as out:
        total = 0
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > 500 * 1024 * 1024:
                raise SystemExit("Download exceeds 500 MB limit.")
            out.write(chunk)
    print(f"Downloaded {target}; verify source license/permission before use.")

if __name__ == "__main__":
    main()
