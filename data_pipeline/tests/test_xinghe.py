import pytest

from src.integrations.xinghe import XingheObjectStore


class FailingObjectClient:
    def get_object(self, **_kwargs):
        raise RuntimeError("missing object")


def test_copy_to_cleans_temporary_file_when_get_object_fails(tmp_path):
    store = XingheObjectStore.__new__(XingheObjectStore)
    store.prefixes = ("s3://bucket/root/",)
    store.client = FailingObjectClient()
    destination = tmp_path / "si.pdf"

    with pytest.raises(RuntimeError, match="missing object"):
        store.copy_to("s3://bucket/root/si.pdf", destination)

    assert list(tmp_path.iterdir()) == []
