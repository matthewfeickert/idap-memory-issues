from pathlib import Path

import uproot

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
    "AnalysisMuonsAuxDyn.muonSegmentLinks",
    "AnalysisMuonsAuxDyn.msOnlyExtrapolatedMuonSpectrometerTrackParticleLink",
    "AnalysisMuonsAuxDyn.extrapolatedMuonSpectrometerTrackParticleLink",
    "AnalysisMuonsAuxDyn.inDetTrackParticleLink",
    "AnalysisMuonsAuxDyn.muonSpectrometerTrackParticleLink",
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
    "AnalysisMuonsAuxDyn.combinedTrackParticleLink",
    "AnalysisMuonsAuxDyn.InnerDetectorPt",
    "AnalysisMuonsAuxDyn.MuonSpectrometerPt",
    "AnalysisMuonsAuxDyn.clusterLink",
    "AnalysisMuonsAuxDyn.spectrometerFieldIntegral",
    "AnalysisElectronsAuxDyn.ambiguityLink",
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


if __name__ == "__main__":
    data_dir = Path("/tmp") / "data"
    if not data_dir.exists():
        data_dir.mkdir()

    example_file = data_dir / "DAOD_PHYSLITE.37233417._000052.pool.root.1"

    if not (example_file).exists():
        import urllib.request

        # download input file (~1.1 GB):
        urllib.request.urlretrieve(
            "https://cernbox.cern.ch/remote.php/dav/public-files/BPIO76iUaeYuhaF/DAOD_PHYSLITE.37233417._000052.pool.root.1",
            example_file,
        )

    all_files = [example_file]

    filter_name = lambda branch: branch in BRANCH_LIST  # noqa: E731

    with uproot.open(all_files[0], filter_name=filter_name) as read_file:
        for branch in BRANCH_LIST:
            print(branch)
            arr = read_file["CollectionTree"][branch].array()

        print(
            f"\n# total read: {read_file.file.source.num_requested_bytes / 1000**2:.2f} MB"
        )
