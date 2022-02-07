#!/usr/bin/env python
import click
from .fastq import compress_paired_end, compress_single_end


@click.group()
def cli():
    pass


@cli.command()
@click.argument("sample_name")
@click.option("--reference_genome_path", default=None)
@click.option("--reference_genome_alias", default=None)
@click.option("--config_path", default=None)
@click.option("--threads", default=16)
@click.option("--output", default=None)
def paired_fastq_compress(
    sample_name,
    reference_genome_path,
    reference_genome_alias,
    config_path,
    threads,
    output,
):
    compress_paired_end(
        sample_name,
        reference_genome_path,
        reference_genome_alias,
        config_path,
        threads,
        output,
    )


@cli.command()
@click.argument("fastq_path")
@click.option("--reference_genome_path", default=None)
@click.option("--reference_genome_alias", default=None)
@click.option("--config_path", default=None)
@click.option("--threads", default=16)
@click.option("--output", default=None)
def single_fastq_compress(
    fastq_path,
    reference_genome_path,
    reference_genome_alias,
    config_path,
    threads,
    output,
):
    compress_single_end(
        fastq_path,
        reference_genome_path,
        reference_genome_alias,
        config_path,
        threads,
        output,
    )


if __name__ == "__main__":
    cli()
