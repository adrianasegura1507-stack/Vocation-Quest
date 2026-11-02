-- =====================================================================
-- Vocation Quest: carreras, instituciones y programas (primera version)
--
-- COMO USARLO: en phpMyAdmin, seleccionar la base vocation_quest2,
-- pestana "Importar", elegir este archivo. Ejecutarlo UNA sola vez
-- (las tablas deben estar vacias; si no, dara error de clave repetida).
--
-- QUE TRAE: solo programas cuya existencia se pudo respaldar en fuentes
-- consultadas (SENA y Universidad de Antioquia). Los enlaces apuntan al
-- SITIO OFICIAL de cada institucion; NO se incluyeron duraciones, cupos
-- ni costos porque no se pudieron comprobar. Antes de presentar, abrir
-- cada enlace y, si se desea, reemplazar sitio_web por la pagina exacta
-- del programa y completar la duracion.
--
-- AREAS: 1 Tecnología, 2 Salud, 3 Arte y Diseño, 4 Administración,
--        5 Ciencias Sociales, 6 Educación, 7 Ciencias.
-- PENDIENTE: Educación (6) no tiene datos; Ciencias Sociales (5) solo Economía.
-- =====================================================================

SET NAMES utf8mb4;

-- ---------------------------------------------------------------------
-- INSTITUCIONES
-- ---------------------------------------------------------------------
INSERT INTO instituciones (id_institucion, nombre, tipo, descripcion, sitio_web, estado) VALUES
(1, 'SENA - Servicio Nacional de Aprendizaje', 'Formación técnica y tecnológica',
 'Entidad pública que ofrece formación titulada (técnica y tecnológica) en todo el país.',
 'https://www.sena.edu.co', 1),
(2, 'Universidad de Antioquia', 'Universidad pública',
 'Universidad pública con sede principal en Medellín y programas de pregrado y posgrado.',
 'https://www.udea.edu.co', 1);

-- ---------------------------------------------------------------------
-- CARRERAS
-- ---------------------------------------------------------------------
INSERT INTO carreras (id_carrera, nombre, descripcion, perfil_profesional, campo_laboral, estado) VALUES
(1, 'Ingeniería de Sistemas y Software',
 'Diseña, desarrolla y mantiene programas, aplicaciones y sistemas de información.',
 NULL,
 'Empresas de tecnología, desarrollo de software, bancos, comercio electrónico y entidades públicas.', 1),
(2, 'Telecomunicaciones y Electrónica',
 'Estudia las redes de comunicación, los circuitos y los sistemas electrónicos.',
 NULL,
 'Empresas de telecomunicaciones, industria electrónica, automatización y redes de datos.', 1),
(3, 'Medicina',
 'Forma profesionales que previenen, diagnostican y tratan enfermedades de las personas.',
 NULL,
 'Hospitales, clínicas, salud pública, investigación en salud y consulta privada.', 1),
(4, 'Enfermería',
 'Se centra en el cuidado de las personas y las comunidades en todas las etapas de la vida.',
 NULL,
 'Hospitales, clínicas, centros de salud, atención domiciliaria y salud comunitaria.', 1),
(5, 'Diseño digital, multimedia y animación',
 'Combina diseño, tecnología y creatividad para producir piezas digitales, páginas web y animaciones.',
 NULL,
 'Estudios de animación, agencias digitales, producción audiovisual y desarrollo de sitios web.', 1),
(6, 'Publicidad',
 'Crea y comunica mensajes para dar a conocer marcas, productos y servicios.',
 NULL,
 'Agencias de publicidad, áreas de mercadeo, medios digitales y producción de contenidos.', 1),
(7, 'Administración de Empresas',
 'Estudia cómo planear, organizar y dirigir los recursos de una organización.',
 NULL,
 'Empresas de todos los sectores, emprendimiento, entidades públicas y consultoría.', 1),
(8, 'Contaduría y gestión financiera',
 'Se ocupa de registrar, analizar y controlar la información contable y financiera.',
 NULL,
 'Empresas, firmas contables, entidades financieras, auditoría y entidades públicas.', 1),
(9, 'Economía',
 'Analiza como se producen, distribuyen y consumen los recursos en la sociedad.',
 NULL,
 'Entidades públicas, banca, consultoría, investigación y análisis de datos económicos.', 1),
(10, 'Biología',
 'Estudia los seres vivos, su funcionamiento y su relación con el ambiente.',
 NULL,
 'Investigación, conservación ambiental, laboratorios y educación.', 1),
(11, 'Matemáticas',
 'Desarrolla el razonamiento lógico y las herramientas para modelar y resolver problemas.',
 NULL,
 'Investigación, análisis de datos, finanzas, tecnología y docencia.', 1),
(12, 'Química',
 'Estudia la composición, las propiedades y las transformaciones de la materia.',
 NULL,
 'Laboratorios, industria, control de calidad e investigación.', 1),
(13, 'Física',
 'Estudia las leyes que explican la materia, la energía y el universo.',
 NULL,
 'Investigación, tecnología, industria, docencia y análisis de datos.', 1);

-- ---------------------------------------------------------------------
-- RELACION CARRERA - AREA
-- ---------------------------------------------------------------------
INSERT INTO carrera_area (id_carrera, id_area) VALUES
(1, 1), (2, 1),
(3, 2), (4, 2),
(5, 3), (6, 3),
(7, 4), (8, 4),
(9, 5),
(10, 7), (11, 7), (12, 7), (13, 7);

-- ---------------------------------------------------------------------
-- PROGRAMAS (sin duracion ni enlace propio: se muestra el sitio oficial
-- de la institucion). tipo: universitario / tecnico / tecnologico / curso
-- ---------------------------------------------------------------------
INSERT INTO programas (id_programa, id_institucion, nombre, tipo, descripcion, duracion, sitio_web, estado) VALUES
(1,  1, 'Tecnólogo en Análisis y Desarrollo de Software', 'tecnologico', NULL, NULL, NULL, 1),
(2,  2, 'Ingeniería de Sistemas', 'universitario', 'Se ofrece en modalidad presencial y virtual.', NULL, NULL, 1),
(3,  2, 'Ingeniería de Telecomunicaciones', 'universitario', NULL, NULL, NULL, 1),
(4,  2, 'Ingeniería Electrónica', 'universitario', NULL, NULL, NULL, 1),
(5,  2, 'Medicina', 'universitario', NULL, NULL, NULL, 1),
(6,  2, 'Enfermería', 'universitario', NULL, NULL, NULL, 1),
(7,  1, 'Tecnólogo en Desarrollo Multimedia y Web', 'tecnologico', NULL, NULL, NULL, 1),
(8,  1, 'Tecnólogo en Animación 3D', 'tecnologico', NULL, NULL, NULL, 1),
(9,  1, 'Tecnólogo en Desarrollo Publicitario', 'tecnologico', NULL, NULL, NULL, 1),
(10, 2, 'Administración de Empresas', 'universitario', NULL, NULL, NULL, 1),
(11, 1, 'Tecnólogo en Gestión Empresarial', 'tecnologico', NULL, NULL, NULL, 1),
(12, 1, 'Tecnólogo en Gestión Administrativa', 'tecnologico', NULL, NULL, NULL, 1),
(13, 2, 'Contaduría Pública', 'universitario', NULL, NULL, NULL, 1),
(14, 1, 'Tecnólogo en Gestión Contable y de Información Financiera', 'tecnologico', NULL, NULL, NULL, 1),
(15, 2, 'Economía', 'universitario', NULL, NULL, NULL, 1),
(16, 2, 'Biología', 'universitario', NULL, NULL, NULL, 1),
(17, 2, 'Matemáticas', 'universitario', NULL, NULL, NULL, 1),
(18, 2, 'Química', 'universitario', NULL, NULL, NULL, 1),
(19, 2, 'Física', 'universitario', NULL, NULL, NULL, 1);

-- ---------------------------------------------------------------------
-- RELACION PROGRAMA - CARRERA
-- ---------------------------------------------------------------------
INSERT INTO programa_carrera (id_programa, id_carrera) VALUES
(1, 1), (2, 1),
(3, 2), (4, 2),
(5, 3),
(6, 4),
(7, 5), (8, 5),
(9, 6),
(10, 7), (11, 7), (12, 7),
(13, 8), (14, 8),
(15, 9),
(16, 10),
(17, 11),
(18, 12),
(19, 13);