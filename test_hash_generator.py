import datetime
import unittest
from licencia import generar_hash_licencia


class TestLicenciaHash(unittest.TestCase):
    def test_generar_hash_licencia_vector_conocido(self):
        fecha = datetime.date(2025, 1, 1)
        clave = "testkey"
        resultado = generar_hash_licencia(fecha, clave)
        self.assertEqual(len(resultado), 12)
        # Determinismo
        self.assertEqual(resultado, generar_hash_licencia(fecha, clave))

    def test_generar_hash_licencia_clave_vacia(self):
        fecha = datetime.date(2025, 1, 1)
        with self.assertRaises(ValueError):
            generar_hash_licencia(fecha, "")
        with self.assertRaises(ValueError):
            generar_hash_licencia(fecha, "   ")

    def test_generar_hash_licencia_bisiesto(self):
        fecha_bisiesto = datetime.date(2024, 2, 29)
        resultado = generar_hash_licencia(fecha_bisiesto, "secreto123")
        self.assertEqual(len(resultado), 12)


if __name__ == "__main__":
    unittest.main()
