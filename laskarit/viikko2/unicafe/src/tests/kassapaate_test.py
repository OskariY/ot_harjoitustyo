import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassaPaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()

    def test_rahaa_1000_euroa(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_lounaita_ei_myyty(self):
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_kateinen_syo_edullisesti_maksu_riittava(self):
        output = self.kassapaate.syo_edullisesti_kateisella(500)
        self.assertEqual(output, 260)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 240)
        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_kateinen_syo_edullisesti_maksu_ei_riittava(self):
        output = self.kassapaate.syo_edullisesti_kateisella(5)
        self.assertEqual(output, 5)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kateinen_syo_maukkaasti_maksu_riittava(self):
        output = self.kassapaate.syo_maukkaasti_kateisella(500)
        self.assertEqual(output, 100)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 400)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_kateinen_syo_maukkaasti_maksu_ei_riittava(self):
        output = self.kassapaate.syo_maukkaasti_kateisella(5)
        self.assertEqual(output, 5)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_syo_edullisesti_kortilla_vahentaa_rahaa(self):
        maksukortti = Maksukortti(500)
        output = self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(output, True)
        self.assertEqual(maksukortti.saldo, 260)

    def test_syo_maukkaasti_kortilla_vahentaa_rahaa(self):
        maksukortti = Maksukortti(500)
        output = self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(output, True)
        self.assertEqual(maksukortti.saldo, 100)

    def test_myytyjen_lounaiden_maara_kasvaa(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_syo_edullisesti_kortilla_ei_tarpeeksi_rahaa(self):
        maksukortti = Maksukortti(10)
        output = self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(output, False)
        self.assertEqual(maksukortti.saldo, 10)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_syo_maukkaasti_kortilla_ei_tarpeeksi_rahaa(self):
        maksukortti = Maksukortti(10)
        output = self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.assertEqual(output, False)
        self.assertEqual(maksukortti.saldo, 10)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_korttimaksut_ei_vaikuta_kassaan(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.syo_maukkaasti_kortilla(maksukortti)
        self.kassapaate.syo_edullisesti_kortilla(maksukortti)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_lataa_rahaa_kortille_toimii(self):
        maksukortti = Maksukortti(1000)
        self.kassapaate.lataa_rahaa_kortille(maksukortti, 500)
        self.assertEqual(maksukortti.saldo, 1500)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000 + 500)

    def test_lataa_rahaa_kortille_ei_toimi_negatiivisella(self):
        maksukortti = Maksukortti(1000)
        output = self.kassapaate.lataa_rahaa_kortille(maksukortti, -500)
        self.assertEqual(output, None)
        self.assertEqual(maksukortti.saldo, 1000)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
