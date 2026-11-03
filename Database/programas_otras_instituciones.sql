-- =========================================
-- Otras instituciones: carreras y programas
-- Fuente: folletos institucionales
-- Requiere haber ejecutado antes programas_ut.sql
-- Áreas: 1 Tecnología, 2 Salud, 3 Arte y Diseño, 4 Administración,
--        5 Ciencias Sociales, 6 Educación, 7 Ciencias
-- =========================================

-- 1. Instituciones
INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Instituto de Educación para el Trabajo y el Desarrollo Humano Comfenalco Tolima', 'privada', 'https://institutocomfenalco.edu.co', 1);
SET @comfenalco = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Universidad Nacional de Colombia - Sede Manizales', 'publica', 'http://admisiones.unal.edu.co/pregrado', 1);
SET @unal = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Institución Universitaria Visión de las Américas', 'privada', 'https://www.uam.edu.co', 1);
SET @uam = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Corporación Universitaria Minuto de Dios - UNIMINUTO', 'privada', 'https://www.uniminuto.edu', 1);
SET @uniminuto = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Universidad del Magdalena', 'publica', 'https://www.unimagdalena.edu.co', 1);
SET @magdalena = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Universidad Externado de Colombia', 'privada', 'https://www.uexternado.edu.co', 1);
SET @externado = LAST_INSERT_ID();

INSERT INTO instituciones (nombre, sector, sitio_web, estado) VALUES
('Corporación Universitaria Empresarial Alexander von Humboldt', 'privada', 'https://www.humboldt.edu.co', 1);
SET @humboldt = LAST_INSERT_ID();

-- 2. Carreras nuevas
INSERT INTO carreras (nombre, descripcion, campo_laboral, estado) VALUES
('Odontología', 'Cuidado de la salud de la boca y los dientes.', 'Consultorios y clínicas odontológicas, hospitales y práctica independiente.', 1),
('Terapia respiratoria', 'Atención y rehabilitación de pacientes con problemas respiratorios.', 'Hospitales, clínicas, unidades de cuidados intensivos y atención domiciliaria.', 1),
('Ingeniería biomédica', 'Tecnología aplicada a equipos y procesos de la salud.', 'Hospitales, empresas de equipos médicos, investigación y mantenimiento biomédico.', 1),
('Psicología', 'Estudio del comportamiento, las emociones y los procesos mentales.', 'Consulta, colegios, empresas, entidades de salud y proyectos sociales.', 1),
('Trabajo social', 'Acompañamiento a personas y comunidades para mejorar su bienestar.', 'Entidades públicas, fundaciones, colegios, salud y proyectos comunitarios.', 1),
('Mercadeo', 'Estudio del mercado y de cómo dar a conocer productos y servicios.', 'Empresas de todos los sectores, agencias y emprendimiento propio.', 1),
('Ingeniería industrial', 'Mejora de procesos para que las empresas produzcan mejor.', 'Industria, logística, servicios, consultoría y gestión de calidad.', 1),
('Ingeniería civil', 'Diseño y construcción de obras como vías, puentes y edificios.', 'Constructoras, entidades de infraestructura, consultoría y diseño.', 1),
('Ingeniería eléctrica', 'Generación, distribución y uso de la energía eléctrica.', 'Empresas de energía, industria, construcción y consultoría.', 1),
('Ingeniería química', 'Transformación de materias primas en productos mediante procesos químicos.', 'Industria química, alimentos, petróleo, ambiental e investigación.', 1),
('Gestión cultural', 'Planeación y desarrollo de proyectos culturales y creativos.', 'Entidades culturales, museos, medios, fundaciones y emprendimientos creativos.', 1),
('Administración pública', 'Gestión de entidades y servicios del Estado.', 'Alcaldías, gobernaciones, entidades nacionales y organizaciones sociales.', 1),
('Antropología', 'Estudio de las culturas y de la diversidad humana.', 'Investigación, entidades públicas, museos y organizaciones sociales.', 1),
('Arqueología', 'Estudio del pasado a partir de restos materiales.', 'Investigación, museos, patrimonio y proyectos de construcción.', 1),
('Ciencia de datos', 'Análisis de grandes cantidades de datos para tomar decisiones.', 'Empresas de tecnología, finanzas, salud, comercio e investigación.', 1),
('Geografía', 'Estudio del territorio y de cómo las personas lo usan y lo transforman.', 'Planeación territorial, entidades ambientales, cartografía e investigación.', 1),
('Relaciones internacionales', 'Estudio de las relaciones entre países y organismos internacionales.', 'Cancillería, organismos internacionales, comercio exterior y consultoría.', 1),
('Filosofía', 'Reflexión sobre el conocimiento, la ética y la sociedad.', 'Docencia, investigación, edición, cultura y consultoría.', 1),
('Conservación y restauración del patrimonio', 'Cuidado y recuperación de obras y objetos de valor cultural.', 'Museos, archivos, bibliotecas, galerías y entidades de patrimonio.', 1),
('Cocina y gastronomía', 'Preparación de alimentos y manejo de cocinas.', 'Restaurantes, hoteles, catering y emprendimiento propio.', 1),
('Logística y distribución', 'Organización del almacenamiento y transporte de productos.', 'Bodegas, empresas de transporte, comercio y distribuidoras.', 1),
('Idiomas y comunicación en inglés', 'Aprendizaje del inglés para estudiar, trabajar y comunicarse.', 'Atención al cliente, turismo, comercio, educación y empresas con clientes extranjeros.', 1);

-- 3. Áreas de las carreras nuevas
INSERT INTO carrera_area (id_carrera, id_area) VALUES
((SELECT id_carrera FROM carreras WHERE nombre = 'Odontología' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Terapia respiratoria' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería biomédica' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería biomédica' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Psicología' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Psicología' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Trabajo social' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Mercadeo' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería industrial' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería industrial' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería civil' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería eléctrica' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería química' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería química' LIMIT 1), 7),
((SELECT id_carrera FROM carreras WHERE nombre = 'Gestión cultural' LIMIT 1), 3),
((SELECT id_carrera FROM carreras WHERE nombre = 'Gestión cultural' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Administración pública' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Administración pública' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Antropología' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Arqueología' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ciencia de datos' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Geografía' LIMIT 1), 7),
((SELECT id_carrera FROM carreras WHERE nombre = 'Geografía' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Relaciones internacionales' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Filosofía' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Conservación y restauración del patrimonio' LIMIT 1), 3),
((SELECT id_carrera FROM carreras WHERE nombre = 'Conservación y restauración del patrimonio' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Cocina y gastronomía' LIMIT 1), 3),
((SELECT id_carrera FROM carreras WHERE nombre = 'Cocina y gastronomía' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Logística y distribución' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Idiomas y comunicación en inglés' LIMIT 1), 5);

-- 4. Tabla temporal con todos los programas
-- inst: 1 Comfenalco, 2 UNAL, 3 Visión de las Américas, 4 Uniminuto,
--       5 Magdalena, 6 Externado, 7 Humboldt
CREATE TEMPORARY TABLE tmp_prog (
    inst        TINYINT,
    nombre      VARCHAR(150),
    tipo        VARCHAR(20),
    modalidad   VARCHAR(20),
    ciudad      VARCHAR(60),
    duracion    VARCHAR(60),
    descripcion VARCHAR(255),
    carrera     VARCHAR(150)
);

INSERT INTO tmp_prog (inst, nombre, tipo, modalidad, ciudad, duracion, descripcion, carrera) VALUES
-- Comfenalco Tolima (Ibagué)
(1, 'Técnico laboral en Asistencia Administrativa y Atención al Usuario', 'tecnico', NULL, 'Ibagué', '630 horas (2 niveles)', 'Incluye uso de herramientas de IA. Requisitos: 15 años y 9.º grado.', 'Administración de Empresas'),
(1, 'Técnico laboral en Auxiliar Contable y Financiero', 'tecnico', NULL, 'Ibagué', '630 horas (2 niveles)', 'Requisitos: 15 años y 9.º grado.', 'Contaduría y gestión financiera'),
(1, 'Técnico laboral en Cocina', 'tecnico', NULL, 'Ibagué', '720 horas (3 niveles)', 'Requisitos: 15 años y 9.º grado.', 'Cocina y gastronomía'),
(1, 'Técnico laboral en Seguridad Ocupacional y Laboral', 'tecnico', NULL, 'Ibagué', '720 horas (3 niveles)', 'Requisitos: 15 años y 9.º grado.', 'Seguridad y salud en el trabajo'),
(1, 'Técnico laboral en Auxiliar de Logística y Distribución', 'tecnico', NULL, 'Ibagué', '720 horas (3 niveles)', 'Requisitos: 15 años y 9.º grado.', 'Logística y distribución'),
(1, 'Inglés Marco Común Europeo de Referencia', 'curso', NULL, 'Ibagué', '16 niveles de 40 horas', 'Edad mínima 7 años, con habilidades de lectoescritura.', 'Idiomas y comunicación en inglés'),
(1, 'Inglés Conversacional', 'curso', NULL, 'Ibagué', '4 niveles de 20 horas', 'Edad mínima 7 años, con habilidades de lectoescritura.', 'Idiomas y comunicación en inglés'),
-- Universidad Nacional, sede Manizales
(2, 'Administración de Empresas', 'universitario', NULL, 'Manizales', NULL, 'Se ofrece en jornada diurna y nocturna.', 'Administración de Empresas'),
(2, 'Administración de Sistemas Informáticos', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería de Sistemas y Software'),
(2, 'Ingeniería Física', 'universitario', NULL, 'Manizales', NULL, NULL, 'Física'),
(2, 'Matemáticas', 'universitario', NULL, 'Manizales', NULL, NULL, 'Matemáticas'),
(2, 'Ingeniería Biológica', 'universitario', NULL, 'Manizales', NULL, NULL, 'Biología'),
(2, 'Estadística', 'universitario', NULL, 'Manizales', NULL, NULL, 'Matemáticas'),
(2, 'Ciencias de la Computación', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería de Sistemas y Software'),
(2, 'Gestión Cultural y Comunicativa', 'universitario', NULL, 'Manizales', NULL, NULL, 'Gestión cultural'),
(2, 'Ciencia Política', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ciencia política'),
(2, 'Licenciatura en Filología e Idiomas - Inglés', 'universitario', NULL, 'Manizales', NULL, NULL, 'Docencia en lenguas y literatura'),
(2, 'Arquitectura', 'universitario', NULL, 'Manizales', NULL, NULL, 'Arquitectura'),
(2, 'Ingeniería Civil', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería civil'),
(2, 'Ingeniería Eléctrica', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería eléctrica'),
(2, 'Ingeniería Electrónica', 'universitario', NULL, 'Manizales', NULL, NULL, 'Telecomunicaciones y Electrónica'),
(2, 'Ingeniería Industrial', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería industrial'),
(2, 'Ingeniería Química', 'universitario', NULL, 'Manizales', NULL, NULL, 'Ingeniería química'),
-- Institución Universitaria Visión de las Américas
(3, 'Odontología', 'universitario', NULL, 'Medellín', NULL, NULL, 'Odontología'),
(3, 'Medicina Veterinaria y Zootecnia', 'universitario', NULL, 'Medellín', NULL, NULL, 'Medicina veterinaria y zootecnia'),
(3, 'Terapia Respiratoria', 'universitario', NULL, 'Medellín', NULL, NULL, 'Terapia respiratoria'),
(3, 'Tecnología en Laboratorio de Prótesis Dental', 'tecnologico', NULL, 'Medellín', NULL, NULL, 'Odontología'),
(3, 'Medicina', 'universitario', NULL, 'Pereira', NULL, NULL, 'Medicina'),
(3, 'Odontología', 'universitario', NULL, 'Pereira', NULL, NULL, 'Odontología'),
(3, 'Medicina Veterinaria y Zootecnia', 'universitario', NULL, 'Pereira', NULL, NULL, 'Medicina veterinaria y zootecnia'),
(3, 'Ingeniería de Software', 'universitario', NULL, 'Pereira', NULL, NULL, 'Ingeniería de Sistemas y Software'),
(3, 'Ingeniería Biomédica', 'universitario', NULL, 'Pereira', NULL, NULL, 'Ingeniería biomédica'),
-- Uniminuto
(4, 'Mercadeo', 'universitario', 'presencial', 'Ibagué', '8 semestres', NULL, 'Mercadeo'),
(4, 'Ingeniería de Sistemas', 'universitario', 'presencial', 'Ibagué', '10 semestres', NULL, 'Ingeniería de Sistemas y Software'),
(4, 'Psicología', 'universitario', 'presencial', 'Ibagué', '10 semestres', NULL, 'Psicología'),
(4, 'Comunicación Social', 'universitario', 'distancia', NULL, '9 semestres', NULL, 'Comunicación y periodismo'),
(4, 'Licenciatura en Educación Infantil', 'universitario', 'distancia', NULL, '10 semestres', NULL, 'Educación infantil y artística'),
(4, 'Contaduría Pública', 'universitario', 'distancia', NULL, '9 semestres', NULL, 'Contaduría y gestión financiera'),
(4, 'Administración Financiera', 'universitario', 'distancia', NULL, '9 semestres', NULL, 'Contaduría y gestión financiera'),
(4, 'Administración de Empresas', 'universitario', 'distancia', NULL, '9 semestres', NULL, 'Administración de Empresas'),
(4, 'Administración en Seguridad y Salud en el Trabajo', 'universitario', 'distancia', NULL, '9 semestres', NULL, 'Seguridad y salud en el trabajo'),
(4, 'Trabajo Social', 'universitario', 'distancia', NULL, '9 semestres', 'Programa nuevo.', 'Trabajo social'),
(4, 'Ingeniería Industrial', 'universitario', 'distancia', NULL, '9 semestres', 'Programa nuevo.', 'Ingeniería industrial'),
(4, 'Derecho', 'universitario', 'distancia', NULL, '10 semestres', 'Programa nuevo.', 'Derecho'),
(4, 'Licenciatura en Educación Física, Recreación y Deporte', 'universitario', 'distancia', NULL, '10 semestres', 'Programa nuevo.', 'Educación física y deporte'),
-- Universidad del Magdalena / CEDEIT
(5, 'Profesional en Deportes', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Educación física y deporte'),
(5, 'Administración Pública', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Administración pública'),
(5, 'Administración de Seguridad en el Trabajo', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Seguridad y salud en el trabajo'),
(5, 'Licenciatura en Matemáticas', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Docencia en matemáticas y ciencias'),
(5, 'Licenciatura en Literatura y Lengua Castellana', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Docencia en lenguas y literatura'),
(5, 'Tecnología en Atención Integral a la Primera Infancia', 'tecnologico', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Educación infantil y artística'),
(5, 'Profesional en Gestión Cultural e Industrias Creativas', 'universitario', NULL, NULL, NULL, 'Presentado en la Expo Universidades de Ibagué. El folleto no indica modalidad ni sede: confírmalo en el sitio oficial.', 'Gestión cultural'),
-- Universidad Externado de Colombia (Bogotá)
(6, 'Administración de Empresas', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Administración de Empresas'),
(6, 'Administración de Empresas Turísticas y Hoteleras', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Turismo y hotelería'),
(6, 'Antropología', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Antropología'),
(6, 'Arqueología', 'universitario', NULL, 'Bogotá', '8 semestres', NULL, 'Arqueología'),
(6, 'Ciencia de Datos', 'universitario', NULL, 'Bogotá', '8 semestres', NULL, 'Ciencia de datos'),
(6, 'Comunicación Social-Periodismo', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Comunicación y periodismo'),
(6, 'Geografía', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Geografía'),
(6, 'Gobierno y Relaciones Internacionales', 'universitario', NULL, 'Bogotá', '8 semestres', NULL, 'Relaciones internacionales'),
(6, 'Historia', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Historia'),
(6, 'Psicología', 'universitario', NULL, 'Bogotá', '10 semestres', NULL, 'Psicología'),
(6, 'Sociología', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Sociología'),
(6, 'Trabajo Social', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Trabajo social'),
(6, 'Conservación y Restauración de Patrimonio Cultural Mueble', 'universitario', NULL, 'Bogotá', '8 semestres', NULL, 'Conservación y restauración del patrimonio'),
(6, 'Contaduría Pública', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Contaduría y gestión financiera'),
(6, 'Derecho', 'universitario', NULL, 'Bogotá', '10 semestres', NULL, 'Derecho'),
(6, 'Economía', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Economía'),
(6, 'Filosofía', 'universitario', NULL, 'Bogotá', '9 semestres', NULL, 'Filosofía'),
(6, 'Finanzas y Relaciones Internacionales', 'universitario', NULL, 'Bogotá', '8 semestres', NULL, 'Negocios internacionales'),
-- Humboldt (el folleto no indica sede)
(7, 'Administración de Empresas Dual', 'universitario', NULL, NULL, '7 semestres', 'Modelo dual: prácticas en empresas reales desde los primeros semestres.', 'Administración de Empresas'),
(7, 'Ingeniería de Software Dual', 'universitario', NULL, NULL, '8 semestres', 'Modelo dual: prácticas en empresas reales desde los primeros semestres.', 'Ingeniería de Sistemas y Software'),
(7, 'Ingeniería Industrial Dual', 'universitario', NULL, NULL, '8 semestres', 'Modelo dual: prácticas en empresas reales desde los primeros semestres.', 'Ingeniería industrial'),
(7, 'Medicina', 'universitario', NULL, NULL, '12 semestres', NULL, 'Medicina'),
(7, 'Enfermería', 'universitario', NULL, NULL, '9 semestres', NULL, 'Enfermería'),
(7, 'Psicología', 'universitario', NULL, NULL, '8 semestres', NULL, 'Psicología'),
(7, 'Medicina Veterinaria y Zootecnia', 'universitario', NULL, NULL, '10 semestres', NULL, 'Medicina veterinaria y zootecnia'),
(7, 'Derecho', 'universitario', NULL, NULL, '8 semestres', NULL, 'Derecho'),
(7, 'Marketing Digital y Comunicación Estratégica', 'universitario', NULL, NULL, '9 semestres', NULL, 'Publicidad');

-- 5. Programas
INSERT INTO programas
    (id_institucion, nombre, tipo, descripcion, duracion, ciudad, modalidad, sitio_web, estado)
SELECT
    CASE t.inst
        WHEN 1 THEN @comfenalco
        WHEN 2 THEN @unal
        WHEN 3 THEN @uam
        WHEN 4 THEN @uniminuto
        WHEN 5 THEN @magdalena
        WHEN 6 THEN @externado
        WHEN 7 THEN @humboldt
    END,
    t.nombre, t.tipo, t.descripcion, t.duracion, t.ciudad, t.modalidad, NULL, 1
FROM tmp_prog t;

-- 6. Enlazar cada programa con su carrera
INSERT INTO programa_carrera (id_programa, id_carrera)
SELECT p.id_programa, c.id_carrera
FROM tmp_prog t
INNER JOIN programas p
    ON p.nombre = t.nombre
   AND p.modalidad <=> t.modalidad
   AND p.ciudad <=> t.ciudad
   AND p.id_institucion = CASE t.inst
        WHEN 1 THEN @comfenalco
        WHEN 2 THEN @unal
        WHEN 3 THEN @uam
        WHEN 4 THEN @uniminuto
        WHEN 5 THEN @magdalena
        WHEN 6 THEN @externado
        WHEN 7 THEN @humboldt
    END
INNER JOIN carreras c
    ON c.nombre = t.carrera;

DROP TEMPORARY TABLE tmp_prog;