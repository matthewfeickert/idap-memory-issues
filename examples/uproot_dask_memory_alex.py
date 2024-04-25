import gc
import warnings
from pathlib import Path

import awkward as ak
import uproot

warnings.filterwarnings("ignore")


BRANCH_LIST = [
    "AnalysisJetsAuxDyn.pt",
    "AnalysisJetsAuxDyn.eta",
    "AnalysisJetsAuxDyn.phi",
    "AnalysisJetsAuxDyn.m",
    "AnalysisElectronsAuxDyn.pt",
    "AnalysisElectronsAuxDyn.eta",
    "AnalysisElectronsAuxDyn.phi",
    "AnalysisElectronsAuxDyn.m",
    "AnalysisMuonsAuxDyn.pt",
    "AnalysisMuonsAuxDyn.eta",
    "AnalysisMuonsAuxDyn.phi",
    "AnalysisJetsAuxDyn.EnergyPerSampling",
    "AnalysisJetsAuxDyn.SumPtTrkPt500",
    "AnalysisJetsAuxDyn.TrackWidthPt1000",
    "PrimaryVerticesAuxDyn.z",
    "PrimaryVerticesAuxDyn.x",
    "PrimaryVerticesAuxDyn.y",
    "AnalysisJetsAuxDyn.NumTrkPt500",
    "AnalysisJetsAuxDyn.NumTrkPt1000",
    "AnalysisJetsAuxDyn.SumPtChargedPFOPt500",
    "AnalysisJetsAuxDyn.Timing",
    "AnalysisJetsAuxDyn.JetConstitScaleMomentum_eta",
    "AnalysisJetsAuxDyn.ActiveArea4vec_eta",
    "AnalysisJetsAuxDyn.DetectorEta",
    "AnalysisJetsAuxDyn.JetConstitScaleMomentum_phi",
    "AnalysisJetsAuxDyn.ActiveArea4vec_phi",
    "AnalysisJetsAuxDyn.JetConstitScaleMomentum_m",
    "AnalysisJetsAuxDyn.JetConstitScaleMomentum_pt",
    "AnalysisJetsAuxDyn.EMFrac",
    "AnalysisJetsAuxDyn.Width",
    "AnalysisJetsAuxDyn.ActiveArea4vec_m",
    "AnalysisJetsAuxDyn.ActiveArea4vec_pt",
    "AnalysisJetsAuxDyn.DFCommonJets_QGTagger_TracksWidth",
    "AnalysisJetsAuxDyn.PSFrac",
    "AnalysisJetsAuxDyn.JVFCorr",
    "AnalysisJetsAuxDyn.DFCommonJets_QGTagger_TracksC1",
    "AnalysisJetsAuxDyn.DFCommonJets_fJvt",
    "AnalysisJetsAuxDyn.DFCommonJets_QGTagger_NTracks",
    "AnalysisJetsAuxDyn.GhostMuonSegmentCount",
    "AnalysisMuonsAuxDyn.momentumBalanceSignificance",
    "AnalysisMuonsAuxDyn.topoetcone20_CloseByCorr",
    "AnalysisMuonsAuxDyn.scatteringCurvatureSignificance",
    "AnalysisMuonsAuxDyn.scatteringNeighbourSignificance",
    "AnalysisMuonsAuxDyn.neflowisol20_CloseByCorr",
    "AnalysisMuonsAuxDyn.topoetcone20",
    "AnalysisMuonsAuxDyn.topoetcone30",
    "AnalysisMuonsAuxDyn.topoetcone40",
    "AnalysisMuonsAuxDyn.neflowisol20",
    "AnalysisMuonsAuxDyn.segmentDeltaEta",
    "AnalysisMuonsAuxDyn.DFCommonJetDr",
    "AnalysisMuonsAuxDyn.InnerDetectorPt",
    "AnalysisMuonsAuxDyn.MuonSpectrometerPt",
    "AnalysisMuonsAuxDyn.spectrometerFieldIntegral",
    "AnalysisMuonsAuxDyn.EnergyLoss",
    "AnalysisJetsAuxDyn.NNJvtPass",
    "AnalysisElectronsAuxDyn.topoetcone20_CloseByCorr",
    "AnalysisElectronsAuxDyn.topoetcone20ptCorrection",
    "AnalysisElectronsAuxDyn.topoetcone20",
    "AnalysisMuonsAuxDyn.ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500_CloseByCorr",
    "AnalysisElectronsAuxDyn.DFCommonElectronsECIDSResult",
    "AnalysisElectronsAuxDyn.neflowisol20",
    "AnalysisMuonsAuxDyn.ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt500",
    "AnalysisMuonsAuxDyn.ptcone40",
    "AnalysisMuonsAuxDyn.ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt1000_CloseByCorr",
    "AnalysisMuonsAuxDyn.ptvarcone30_Nonprompt_All_MaxWeightTTVA_pt1000",
    "AnalysisMuonsAuxDyn.ptvarcone40",
    "AnalysisElectronsAuxDyn.f1",
    "AnalysisMuonsAuxDyn.ptcone20_Nonprompt_All_MaxWeightTTVA_pt500",
    "PrimaryVerticesAuxDyn.vertexType",
    "AnalysisMuonsAuxDyn.ptvarcone30",
    "AnalysisMuonsAuxDyn.ptcone30",
    "AnalysisMuonsAuxDyn.ptcone20_Nonprompt_All_MaxWeightTTVA_pt1000",
    "AnalysisElectronsAuxDyn.ptvarcone30_Nonprompt_All_MaxWeightTTVALooseCone_pt500",
    "AnalysisMuonsAuxDyn.CaloLRLikelihood",
]


def materialize_branches(events):
    num_events = ak.num(events, axis=0)  # track number of events

    _counter = 0
    # see https://github.com/dask-contrib/dask-awkward/issues/499 for context
    for branch in BRANCH_LIST:
        _counter_to_add = ak.count_nonzero(events[branch], axis=-1)  # reduce innermost

        # reduce >2-dimensional (per event) branches further
        for _ in range(_counter_to_add.ndim - 1):
            _counter_to_add = ak.count_nonzero(_counter_to_add, axis=-1)

        _counter = _counter + _counter_to_add  # sum 1-dim array built from new branch
        # gc.collect()  # does nothing?

    _counter = ak.count_nonzero(_counter, axis=0)  # reduce to int

    return {"nevts": num_events, "_counter": _counter}


if __name__ == "__main__":
    filter_name = lambda b: b in BRANCH_LIST

    data_dir = Path("/tmp") / "data"
    if not data_dir.exists():
        data_dir.mkdir()

    example_file = data_dir / "DAOD_PHYSLITE.37233417._000052.pool.root.1"

    if not (example_file).exists():
        import urllib.request

        urllib.request.urlretrieve(
            "https://cernbox.cern.ch/remote.php/dav/public-files/BPIO76iUaeYuhaF/DAOD_PHYSLITE.37233417._000052.pool.root.1",
            example_file,
        )

    events = uproot.dask({example_file: "CollectionTree"}, filter_name=filter_name)
    task = materialize_branches(events)
    task["_counter"].compute()
