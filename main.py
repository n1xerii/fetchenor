from tawpy import Tenor
import requests
import argparse

def main():
    tenor = Tenor()

    # Args
    parser = argparse.ArgumentParser(description="Fetch GIFs from Tenor")
    parser.add_argument("--query", type=str, help="Search term")
    parser.add_argument("--trending", action="store_true", help="Fetch trending gifs")
    parser.add_argument("--limit", type=int, default=1, help="Number of gifs")

    args = parser.parse_args()

    # Variables
    filename = None

    # Mode
    if args.query:
        print(f"Searching GIFs for: {args.query}.")
        gifs = tenor.search_for_gifs(query=args.query, limit=args.limit)
        filename = args.query
    else:
        print("Fetching trending GIFs.")
        gifs = tenor.trending_gifs(limit=args.limit)
        filename = "trending"

    # Download
    for i, gif in enumerate(gifs):
        try:
            response = requests.get(gif, timeout=8)
            response.raise_for_status()

            with open(f"gif_{filename}_{i}.gif", "wb") as f:
                f.write(response.content)

            print(f"Downloaded gif_{i}.gif")

        except requests.RequestException as e:
            print(f"Failed to download {gif}: {e}")

if __name__ == "__main__":
    main()