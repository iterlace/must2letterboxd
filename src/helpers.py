from typing import Sequence, Any, Generator, List


def generate_batches(seq: List[Any], n: int) -> Generator[List[Any], None, None]:
    for i in range(0, len(seq), n):
        yield seq[i:i + n]
