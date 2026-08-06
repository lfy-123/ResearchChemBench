from src.integrations.softcite import SoftciteClientPool


class FakeSoftciteClient:
    def __init__(self, name):
        self.name = name

    def annotate_tei(self, _path):
        return {"client": self.name}

    def characterize_context(self, _text):
        return {"client": self.name}

    def version(self):
        return {"client": self.name}


def test_softcite_pool_distributes_requests_round_robin():
    pool = SoftciteClientPool(
        [FakeSoftciteClient("first"), FakeSoftciteClient("second")]
    )

    assert pool.version()["client"] == "first"
    assert pool.annotate_tei("paper.tei.xml")["client"] == "second"
    assert pool.characterize_context("DFT") ["client"] == "first"
