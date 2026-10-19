from evaluation.metrics import (
    hit_at_k,
    mean_reciprocal_rank,
    recall_at_k,
    reciprocal_rank,
)


def test_hit_at_k():

    retrieved = [
        "KB001",
        "KB002",
        "KB003",
    ]

    assert (
        hit_at_k(
            retrieved,
            "KB001",
            1,
        )
        == 1.0
    )

    assert (
        hit_at_k(
            retrieved,
            "KB003",
            2,
        )
        == 0.0
    )


def test_reciprocal_rank():

    retrieved = [
        "KB003",
        "KB001",
        "KB002",
    ]

    assert (
        reciprocal_rank(
            retrieved,
            "KB003",
        )
        == 1.0
    )

    assert (
        reciprocal_rank(
            retrieved,
            "KB001",
        )
        == 0.5
    )


def test_mrr():

    rankings = [
        ["KB001", "KB002"],
        ["KB002", "KB001"],
    ]

    expected = [
        "KB001",
        "KB002",
    ]

    result = mean_reciprocal_rank(
        rankings,
        expected,
    )

    assert result == 1.0


def test_recall_at_k():

    rankings = [
        ["KB001", "KB002"],
        ["KB003", "KB001"],
        ["KB004", "KB005"],
    ]

    expected = [
        "KB001",
        "KB001",
        "KB004",
    ]

    result = recall_at_k(
        rankings,
        expected,
        k=2,
    )

    assert result == 1.0