#!/usr/bin/env python3
"""Minimal Python example for reading the Xinghe paper dataset."""

from pathlib import Path

from read_xinghe_dataset import XingheReader

CREDENTIAL_FILE = Path("/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt")
PAPER_PREFIX = "s3://private-cooperate-data/en-paper-hzzj/pdf/"


def main() -> None:
    with XingheReader(CREDENTIAL_FILE) as dataset:
        print("Authorized datasets:")
        for prefix in dataset.prefixes:
            print(f"  {prefix}")

        print("\nFirst 10 papers:")
        papers = list(dataset.list_objects(PAPER_PREFIX, limit=10))
        for paper in papers:
            print(f"  {paper}")

        if not papers:
            print("No paper was found under the selected prefix.")
            return

        first_paper = papers[0]
        print(f"\nFirst paper exists: {dataset.contains(first_paper)}")
        print(f"First paper size: {dataset.size(first_paper)} bytes")

        # To download the first paper, uncomment the following lines:
        # output = Path("data/xinghe/first_paper.pdf")
        # saved_path = dataset.download(first_paper, output, overwrite=False)
        # print(f"Downloaded to: {saved_path}")


if __name__ == "__main__":
    main()
