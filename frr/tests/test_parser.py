from frr import parser as pr
from frr import monad
###############################################################################
#                                    Test
###############################################################################
class TestClass:

    def test_create_GcRow(self):
        gc = pr.GcRow(r"GC      GC-JLP  -F      Hilary Readhead         EVOLUTION - EVOLUTION - LETOUR  8       121w @1.80wkg   01:31:02.265")
        assert gc is not None
        assert gc.effort == "121w @1.80wkg"
        assert gc.time ==  "01:31:02.265000"
        assert gc.watt == 121
        assert gc.wkg == 1.80

        gc = pr.GcRow(r"GC      GC-CRP  -M      Eric Brandhorst         TEAMCLS - Équipe Orange         1       276w @4.00wkg   00:48:08.726")
        assert gc is not None
        assert gc.table == "GC"
        assert gc.frhc == "GC-CRP"
        assert gc.gender == "-M"
        assert gc.name ==  "Eric Brandhorst"
        assert gc.team ==  "TEAMCLS - Équipe Orange"
        assert gc.stage == 1
        assert gc.effort == "276w @4.00wkg"
        assert gc.watt == 276
        assert gc.wkg == 4.00
        assert gc.time ==  "00:48:08.726000"

    def test_pipe_line_row(self):

        def fake_db_insert(gc):
            assert gc.table == "GC"
            assert gc.name == "Eric Brandhorst"


        pr.pipe_line_insert_row_db(r"""GC      GC-CRP  -M      Eric Brandhorst         TEAMCLS - Équipe Orange         1       276w @4.00wkg   00:48:08.726""",fake_db_insert)

    # def test_read_file(self):
    #     """

    #     """

    #     gcs = open_txt_file("/home/calle/git/frr_gc/season_1.txt")
    #     assert len(gcs) > 100
    #     print(gcs[190].name)
