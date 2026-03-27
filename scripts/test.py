

import unittest

from dinamico import resolver_dinamico
from voraz import voraz

class TestCorteVarilla(unittest.TestCase):
	# ──────────────── Casos Básicos ────────────────
	def test_01_voraz_no_siempre_optimo(self):
		"""Voraz NO garantiza óptimo global."""
		precios = {1: 1, 2: 5, 3: 8, 4: 10}
		n = 4
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 9)
		self.assertEqual(ganancia_pd, 10)

	def test_02_corte_uniforme(self):
		"""Todos los segmentos tienen el mismo rendimiento."""
		precios = {1: 2, 2: 4, 3: 6}
		n = 6
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 12)
		self.assertEqual(ganancia_pd, 12)

	def test_03_mejor_segmento_pequeno(self):
		"""El segmento más pequeño tiene mejor rendimiento."""
		precios = {1: 3, 2: 4, 3: 5}
		n = 6
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 18)
		self.assertEqual(ganancia_pd, 18)

	def test_04_varilla_longitud_uno(self):
		"""Varilla de longitud 1: solo puede tomar el segmento de longitud 1."""
		precios = {1: 5, 2: 9, 3: 13}
		n = 1
		ganancia_voraz, segs_voraz = voraz(n, precios)
		ganancia_pd, segs_pd = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 5)
		self.assertEqual(ganancia_pd, 5)
		self.assertEqual(len(segs_voraz), 1)
		self.assertEqual(len(segs_pd), 1)

	def test_05_un_solo_segmento_disponible(self):
		"""Solo hay un tipo de segmento posible."""
		precios = {3: 9}
		n = 9
		ganancia_voraz, segs_voraz = voraz(n, precios)
		ganancia_pd, segs_pd = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 27)
		self.assertEqual(ganancia_pd, 27)
		self.assertEqual(len(segs_voraz), 3)
		self.assertEqual(len(segs_pd), 3)

	# ──────────────── Casos Límite ────────────────
	def test_06_varilla_longitud_cero(self):
		"""Varilla de longitud 0: no se puede cortar nada."""
		precios = {1: 2, 2: 5}
		n = 0
		ganancia_voraz, segs_voraz = voraz(n, precios)
		ganancia_pd, segs_pd = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 0)
		self.assertEqual(ganancia_pd, 0)
		self.assertEqual(segs_voraz, [])
		self.assertEqual(segs_pd, [])

	def test_07_ningun_segmento_cabe(self):
		"""Todos los segmentos son más grandes que la varilla."""
		precios = {5: 10, 10: 20}
		n = 3
		ganancia_voraz, segs_voraz = voraz(n, precios)
		ganancia_pd, segs_pd = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 0)
		self.assertEqual(ganancia_pd, 0)
		self.assertEqual(segs_voraz, [])
		self.assertEqual(segs_pd, [])

	def test_08_varilla_igual_a_segmento(self):
		"""La varilla tiene exactamente la longitud del mejor segmento."""
		precios = {1: 1, 2: 6, 4: 9}
		n = 2
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 6)
		self.assertEqual(ganancia_pd, 6)

	def test_09_precio_muy_alto_segmento_grande(self):
		"""Segmento grande con precio muy alto domina."""
		precios = {1: 1, 2: 2, 10: 100}
		n = 10
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 100)
		self.assertEqual(ganancia_pd, 100)

	def test_10_resto_no_cubierto(self):
		"""La varilla tiene un resto que no puede ser cubierto por ningún segmento."""
		precios = {2: 5, 3: 8}
		n = 5
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 13)
		self.assertEqual(ganancia_pd, 13)

	# ──────────────── Casos Comparativos y Estrés ────────────────
	def test_11_voraz_suboptimo_documentado(self):
		"""Caso donde voraz NO alcanza el óptimo global."""
		precios = {1: 1, 2: 5, 3: 8}
		n = 4
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 9)
		self.assertEqual(ganancia_pd, 10)

	def test_12_voraz_suboptimo_caso2(self):
		"""Voraz toma 5+3=$16, PD toma 3+5=$18. PD supera al voraz por 2."""
		precios = {1: 1, 3: 7, 5: 11}
		n = 8
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 16)
		self.assertEqual(ganancia_pd, 18)

	def test_13_pd_supera_voraz_segmentos_impares(self):
		"""PD supera al voraz con segmentos impares."""
		precios = {1: 1, 3: 7, 5: 11}
		n = 8
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 16)
		self.assertEqual(ganancia_pd, 18)

	def test_14_pd_supera_voraz_n_mediano(self):
		"""PD supera al voraz en n mediano."""
		precios = {1: 1, 2: 5, 3: 8}
		n = 100
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 265)
		self.assertEqual(ganancia_pd, 266)

	def test_15_pd_supera_voraz_cuatro_segmentos(self):
		"""PD supera al voraz con cuatro segmentos."""
		precios = {1: 1, 4: 9, 5: 10, 6: 13}
		n = 10
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 20)
		self.assertEqual(ganancia_pd, 22)

	def test_16_pd_supera_voraz_n_100_mixto(self):
		"""PD supera al voraz en n=100 mixto."""
		precios = {3: 4, 5: 7, 6: 9, 7: 11}
		n = 100
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 154)
		self.assertEqual(ganancia_pd, 156)

	def test_17_pd_supera_voraz_n_1000(self):
		"""PD supera al voraz en n=1000."""
		precios = {1: 1, 2: 5, 3: 8}
		n = 10000
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 26665)
		self.assertEqual(ganancia_pd, 26666)

	# ──────────────── Robustez y Estrés ────────────────
	def test_21_varilla_grande(self):
		"""Varilla de longitud 100 con segmento dominante reutilizado muchas veces."""
		precios = {1: 3, 2: 5}
		n = 100
		ganancia_voraz, _ = voraz(n, precios)
		ganancia_pd, _ = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 300)
		self.assertEqual(ganancia_pd, 300)

	def test_22_muchos_tipos_de_segmentos(self):
		"""15 tipos distintos de segmentos, todos con el mismo rendimiento."""
		precios = {
			1: 2, 2: 4, 3: 6, 4: 8, 5: 10,
			6: 12, 7: 14, 8: 16, 9: 18, 10: 20,
			11: 22, 12: 24, 13: 26, 14: 28, 15: 30
		}
		n = 30
		ganancia_voraz , _= voraz(n, precios)
		ganancia_pd , _= resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 60)
		self.assertEqual(ganancia_pd, 60)


	def test_23_rendimiento_identico_desempate(self):
		"""Dos segmentos con rendimiento idéntico, el algoritmo debe ser estable."""
		precios = {2: 4, 4: 8}
		n = 8
		ganancia_voraz, segs_voraz = voraz(n, precios)
		ganancia_pd, segs_pd = resolver_dinamico(precios, n)
		self.assertEqual(ganancia_voraz, 16)
		self.assertEqual(ganancia_pd, 16)
		self.assertLessEqual(sum(s["longitud"] for s in segs_voraz), n)
		self.assertLessEqual(sum(s["longitud"] for s in segs_pd), n)


if __name__ == "__main__":
	unittest.main()


