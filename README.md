# Vocation Quest

Aplicación web de **orientación vocacional gamificada** para estudiantes. Se completa un recorrido por niveles, estilo juego, y al final se muestran las áreas profesionales con las que más afinidad hay, junto con carreras y programas relacionados.

> Los resultados son una guía para explorar intereses. **No reemplazan la orientación de un psicorientador.**

Proyecto académico del **Técnico en Programación de Software (SENA)**.

## Equipo

- Adriana Segura Ceballos
- Maylle Andrea Quesada Enciso
- Karol Juliana Varajas Castro

## Enlaces

- Página publicada: disponible solo en local. Para demostraciones se usa una URL temporal con Cloudflare Tunnel.
- Repositorio: https://github.com/adrianasegura1507-stack/Vocation-Quest

## ¿Qué hace?

- **Registro e inicio de sesión** con fecha de nacimiento (la edad se calcula sola) y contraseñas guardadas con hash.
- **Mapa de aventura** con 5 niveles: del 1 al 4 son pruebas con preguntas; el nivel 5 son los resultados y se desbloquea al terminar los anteriores.
- **Prueba vocacional**: 28 preguntas (4 niveles de 7), con barra de progreso y progreso guardado.
- **Resultados**: porcentaje por área (siete áreas), área principal y avisos de empate, y carreras y programas relacionados con sus tres áreas principales.
- **Misión actual y logros** que se desbloquean según el avance.
- **Perfil del estudiante**: ver, editar datos, cambiar contraseña y eliminar la cuenta.
- **Panel de administración**: estadísticas, y crear, editar, buscar, activar o desactivar y eliminar estudiantes.

## Tecnologías

Python, Flask, Jinja, HTML, CSS, MySQL (XAMPP), Git y GitHub.

## Cómo ejecutarlo en tu computador

Requisitos: Python 3, XAMPP (para MySQL) y Git.

1. Clona el repositorio y entra a la carpeta:

   ```powershell
   git clone https://github.com/adrianasegura1507-stack/Vocation-Quest.git
   cd Vocation-Quest
   ```

2. Cambia a la rama de trabajo:

   ```powershell
   git switch pruebas-vocacionales
   ```

3. Crea el entorno virtual e instala las librerías:

   ```powershell
   py -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

4. Enciende **MySQL** desde el panel de XAMPP. En `http://localhost/phpmyadmin` crea una base llamada `vocation_quest2` e importa el archivo `Database/vocation_quest_aiven.sql` (trae las tablas, las preguntas, las áreas, los logros, las carreras y las instituciones, sin usuarios).

5. Ejecuta la aplicación y abre `http://127.0.0.1:5000`:

   ```powershell
   python Backend/app.py
   ```

La conexión a la base de datos está en `Backend/database.py`. Por defecto usa XAMPP (`localhost`, usuario `root`, sin contraseña) y se puede cambiar con las variables de entorno `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` y `DB_SSL_CA`.

## Estructura

```text
Backend/
  app.py            Aplicación principal y página del estudiante
  database.py       Conexión con MySQL
  routes/           auth, pruebas, perfil y admin
  templates/        Páginas HTML (Jinja)
  static/           Estilos (CSS)
Database/           Archivos SQL
requirements.txt    Librerías de Python
```

## Cuentas de prueba

Las cuentas de demostración (estudiante y administrador) se entregan en el documento de entrega, no en este repositorio, porque es público.

## Limitaciones conocidas

- Las 28 preguntas son una propuesta de diseño balanceada (cada área aparece el mismo número de veces).
- La edad mínima (14) y la máxima (30) del registro son valores provisionales, pendientes de confirmar con la persona interesada del proyecto.
- Los datos de carreras e instituciones son limitados: hoy incluyen el SENA y la Universidad de Antioquia. Los enlaces llevan al sitio oficial de cada institución; los cupos, costos y fechas deben consultarse allí.