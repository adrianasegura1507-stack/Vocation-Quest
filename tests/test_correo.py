import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath("Backend"))

from correo import enviar_correo_bienvenida


class PruebasCorreoBienvenida(unittest.TestCase):

    @patch.dict(os.environ, {
        "MAIL_SERVER": "smtp.gmail.com",
        "MAIL_PORT": "587",
        "MAIL_USERNAME": "prueba@gmail.com",
        "MAIL_PASSWORD": "contrasena_prueba",
        "MAIL_DEFAULT_SENDER": "prueba@gmail.com"
    })
    @patch("correo.smtplib.SMTP")
    def test_envio_correo_bienvenida_exitoso(self, smtp_mock):
        servidor = MagicMock()
        smtp_mock.return_value.__enter__.return_value = servidor

        resultado = enviar_correo_bienvenida(
            "Estudiante de prueba",
            "destinatario@gmail.com"
        )

        self.assertTrue(resultado)
        servidor.starttls.assert_called_once()
        servidor.login.assert_called_once()
        servidor.send_message.assert_called_once()

    @patch.dict(os.environ, {}, clear=True)
    def test_falla_si_falta_configuracion(self):
        resultado = enviar_correo_bienvenida(
            "Estudiante de prueba",
            "destinatario@gmail.com"
        )

        self.assertFalse(resultado)


if __name__ == "__main__":
    unittest.main()
