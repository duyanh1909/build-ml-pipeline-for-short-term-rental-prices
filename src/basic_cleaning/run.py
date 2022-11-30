#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the results in Weights & Biases
"""
import argparse
import logging
import wandb

import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    logger.info("Dowload input artifact")
    path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(path)

    # Drop outliers
    logger.info("Drop outliers")
    min_price = args.min_price
    max_price = args.max_price
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    filename = args.output_artifact

    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(40.5, 41.2)
    df = df[idx].copy()

    df.to_csv(filename, index=False)

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file(filename)

    logger.info("Logging artifact W&B")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="The name of input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="The name of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="The type of output artifact",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="The description of output artifact",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=int,
        help="The minimum price value",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=int,
        help="The maximum price value",
        required=True
    )

    args = parser.parse_args()

    go(args)
