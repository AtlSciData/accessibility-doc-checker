from pathlib import Path

from app.server import app

ROOT = Path(__file__).resolve().parents[2]


def post_fixture(name):
    client = app.test_client()
    with open(ROOT / "fixtures" / "html" / name, "rb") as fh:
        return client.post(
            "/api/scan",
            data={"file": (fh, name)},
            content_type="multipart/form-data",
        )


def test_clean_file_scores_100():
    r = post_fixture("06-accessible-baseline.html")
    assert r.status_code == 200
    assert r.get_json()["score"] == 100


def test_images_without_alt_are_flagged():
    r = post_fixture("03-images-no-alt.html")
    body = r.get_json()
    assert body["score"] == 80
    assert "image-alt" in [v["id"] for v in body["violations"]]


def test_best_practice_rules_listed_as_advice():
    body = post_fixture("05-heading-table-link.html").get_json()
    assert "heading-order" in [v["id"] for v in body["advice"]]
    assert "heading-order" not in [v["id"] for v in body["violations"]]


def test_non_html_is_rejected():
    client = app.test_client()
    r = client.post(
        "/api/scan",
        data={"file": (__import__("io").BytesIO(b"hello"), "notes.txt")},
        content_type="multipart/form-data",
    )
    assert r.status_code == 400
