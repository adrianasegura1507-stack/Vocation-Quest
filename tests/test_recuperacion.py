import os
import sys
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath("Backend"))

from recuperacion import (
    generar_codigo_recuperacion,
    calcular_vencimiento_codigo,
    guardar_codigo_recuperacion,
    registrar_intento_fallido
)

from werkzeug.security import check_password_hash


class PruebasRecuperacion(unittest.TestCase):

    def test_generar_codigo_seguro(self):
        codigo, codigo_hash = generar_codigo_recuperacion()

        self.assertEqual(len(codigo), 6)
        self.assertTrue(codigo.isdigit())
        self.assertTrue(100000 <= int(codigo) <= 999999)
        self.assertNotEqual(codigo, codigo_hash)
        self.assertTrue(check_password_hash(codigo_hash, codigo))

    def test_vencimiento_diez_minutos(self):
        inicio = datetime.now()
        vencimiento = calcular_vencimiento_codigo()
        final = datetime.now()

        self.assertGreaterEqual(
            vencimiento,
            inicio + timedelta(minutes=10)
        )
        self.assertLessEqual(
            vencimiento,
            final + timedelta(minutes=10)
        )

    @patch("recuperacion.obtener_conexion")
    def test_guardar_codigo_exitosamente(self, conexion_mock):
        conexion = MagicMock()
        cursor = MagicMock()

        conexion_mock.return_value = conexion
        conexion.cursor.return_value = cursor
        cursor.lastrowid = 17

        resultado = guardar_codigo_recuperacion(
            5,
            "hash_de_prueba"
        )

        self.assertEqual(resultado, 17)
        conexion.commit.assert_called_once()
        cursor.execute.assert_called_once()
        cursor.close.assert_called_once()
        conexion.close.assert_called_once()

    @patch("recuperacion.obtener_conexion")
    def test_error_al_guardar_codigo(self, conexion_mock):
        conexion = MagicMock()
        cursor = MagicMock()

        conexion_mock.return_value = conexion
        conexion.cursor.return_value = cursor
        cursor.execute.side_effect = Exception("Error de prueba")

        resultado = guardar_codigo_recuperacion(
            5,
            "hash_de_prueba"
        )

        self.assertIsNone(resultado)
        conexion.rollback.assert_called_once()
        cursor.close.assert_called_once()
        conexion.close.assert_called_once()

    @patch("recuperacion.obtener_conexion")
    def test_registrar_intento_fallido(self, conexion_mock):
        conexion = MagicMock()
        cursor = MagicMock()

        conexion_mock.return_value = conexion
        conexion.cursor.return_value = cursor
        cursor.rowcount = 1

        resultado = registrar_intento_fallido(17)

        self.assertTrue(resultado)
        cursor.execute.assert_called_once()
        conexion.commit.assert_called_once()
        cursor.close.assert_called_once()
        conexion.close.assert_called_once()

    @patch("recuperacion.obtener_conexion")
    def test_intento_no_registrado(self, conexion_mock):
        conexion = MagicMock()
        cursor = MagicMock()

        conexion_mock.return_value = conexion
        conexion.cursor.return_value = cursor
        cursor.rowcount = 0

        resultado = registrar_intento_fallido(17)

        self.assertFalse(resultado)
        conexion.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
