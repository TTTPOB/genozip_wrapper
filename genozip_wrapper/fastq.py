import subprocess
from typing import Union, List
from pathlib import Path
from .read_config import read_config, get_genome_path
import os


def get_mate_path(sample_name) -> List[Union[str, os.PathLike]]:
    r1, r2 = [f"{sample_name}_R{mate}.fastq.gz" for mate in (1, 2)]
    if not (Path(r1).exists() and Path(r2).exists()):
        r1, r2 = [f"{sample_name}_R{mate}.fastq" for mate in (1, 2)]
        if not (Path(r1).exists() and Path(r2).exists()):
            r1, r2 = [f"{sample_name}_R{mate}.fq.gz" for mate in (1, 2)]
            if not (Path(r1).exists() and Path(r2).exists()):
                r1, r2 = [f"{sample_name}_R{mate}.fq" for mate in (1, 2)]
    return (r1, r2)


def compress_paired_end(
    sample_name: str,
    reference_genome_path: Union[str, os.PathLike] = None,
    reference_genome_alias: str = None,
    config_path: Union[str, os.PathLike] = None,
    threads: int = 16,
    output=None,
):
    config = read_config(config_path)
    if reference_genome_path and reference_genome_alias:
        ValueError(
            "reference_genome_path and reference_genome_alias are mutually exclusive"
        )
    if reference_genome_path:
        reference_genome_path = Path(reference_genome_path)
    elif reference_genome_alias:
        reference_genome_path = get_genome_path(reference_genome_alias, config)

    if output == None:
        output = f"{sample_name}.genozip"

    r1, r2 = get_mate_path(sample_name)
    command = [
        "genozip",
        r1,
        r2,
        f"-@{threads}",
        "-o",
        output,
        "--pair",
    ]
    if reference_genome_path:
        command.extend(["--reference", str(reference_genome_path)])
    subprocess.run(command)

def compress_single_end(
    fastq_path: Union[str, os.PathLike],
    reference_genome_path: Union[str, os.PathLike] = None,
    reference_genome_alias: str = None,
    config_path: Union[str, os.PathLike] = None,
    threads: int = 16,
    output = None,
):
    config = read_config(config_path)
    if reference_genome_path and reference_genome_alias:
        ValueError(
            "reference_genome_path and reference_genome_alias are mutually exclusive"
        )
    if reference_genome_path:
        reference_genome_path = Path(reference_genome_path)
    elif reference_genome_alias:
        reference_genome_path = get_genome_path(reference_genome_alias, config)
    command = [
        "genozip",
        fastq_path,
        f"-@{threads}",
    ]
    if reference_genome_path:
        command.extend(["--reference", str(reference_genome_path)])
    if output:
        command.extend(["-o", str(output)])
    subprocess.run(command)
    