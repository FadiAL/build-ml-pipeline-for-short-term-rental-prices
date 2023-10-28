#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    logger.info("Starting W&B run")
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    logger.info(f"Downloading artifact {args.input_artifact}")
    local_path = run.use_artifact(args.input_artifact).file()

    logger.info("Loading artifact with pandas")
    df = pd.read_csv(local_path)

    logger.info(f"Filtering price to range ({args.min_price}, {args.max_price})")
    idx = df["price"].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info("Converting 'last_review' to datetime")
    df["last_review"] = pd.to_datetime(df["last_review"])

    logger.info("Saving cleaned data to csv with pandas")
    df.to_csv("clean_sample.csv", index=False)

    logger.info("Logging artifact to W&B")
    artifact = wandb.Artifact(
      args.output_artifact,
      type=args.output_type,
      description=args.output_description
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input artifact to clean",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Output artifact name to save to W&B",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="Type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Description of output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price to restrict",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price to restrict",
        required=True
    )


    args = parser.parse_args()

    go(args)