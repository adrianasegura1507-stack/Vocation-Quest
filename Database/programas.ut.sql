-- =========================================
-- Universidad del Tolima: carreras y programas
-- Fuente: folleto institucional (pregrados presenciales y a distancia)
-- =========================================

-- 1. Institución
INSERT INTO instituciones (nombre, sector, sitio_web, estado)
VALUES ('Universidad del Tolima', 'publica', 'https://www.ut.edu.co', 1);

SET @ut = LAST_INSERT_ID();

-- 2. Carreras nuevas
INSERT INTO carreras (nombre, descripcion, campo_laboral, estado) VALUES
('Arquitectura', 'Diseño de espacios, edificios y ciudades, combinando creatividad y técnica.', 'Estudios de arquitectura, constructoras, entidades de planeación y diseño de interiores.', 1),
('Artes plásticas y visuales', 'Creación artística con pintura, escultura, dibujo, fotografía y otros medios.', 'Producción artística, galerías, museos, docencia y proyectos culturales.', 1),
('Comunicación y periodismo', 'Investigar, contar y difundir información en medios y plataformas digitales.', 'Medios de comunicación, comunicación corporativa, producción de contenidos y agencias.', 1),
('Historia', 'Estudio del pasado para entender las sociedades de hoy.', 'Investigación, docencia, archivos, museos y gestión cultural.', 1),
('Sociología', 'Análisis de cómo se organizan y cambian los grupos y las sociedades.', 'Investigación social, entidades públicas, organizaciones sociales y consultoría.', 1),
('Ciencia política', 'Estudio del poder, el Estado y las políticas públicas.', 'Entidades públicas, análisis político, organizaciones y consultoría.', 1),
('Derecho', 'Estudio de las leyes y la forma de resolver conflictos y defender derechos.', 'Firmas jurídicas, entidades públicas, rama judicial y empresas.', 1),
('Negocios internacionales', 'Gestión del comercio y de los negocios entre países.', 'Empresas exportadoras e importadoras, comercio exterior y logística.', 1),
('Turismo y hotelería', 'Administración de servicios y empresas turísticas y hoteleras.', 'Hoteles, agencias de viajes, entidades de turismo y emprendimiento propio.', 1),
('Ingeniería agronómica y agroindustrial', 'Producción agrícola y transformación de productos del campo.', 'Empresas agrícolas, agroindustria, asistencia técnica y proyectos rurales.', 1),
('Ingeniería forestal y ecosistemas', 'Manejo, protección y recuperación de bosques y ecosistemas.', 'Entidades ambientales, proyectos de conservación y empresas forestales.', 1),
('Medicina veterinaria y zootecnia', 'Salud, cuidado y producción de los animales.', 'Clínicas veterinarias, fincas, empresas pecuarias e investigación.', 1),
('Topografía y modelación de proyectos de ingeniería', 'Medición del terreno y modelado de proyectos de construcción.', 'Constructoras, firmas de ingeniería, catastro y entidades de infraestructura.', 1),
('Seguridad y salud en el trabajo', 'Prevención de accidentes y cuidado de la salud en las empresas.', 'Empresas de todos los sectores, aseguradoras y consultoría.', 1),
('Regencia de farmacia', 'Manejo y dispensación de medicamentos y atención en farmacias.', 'Farmacias, droguerías, hospitales y distribuidoras.', 1),
('Docencia en matemáticas y ciencias', 'Enseñanza de las matemáticas y las ciencias naturales.', 'Colegios, instituciones educativas y proyectos pedagógicos.', 1),
('Docencia en lenguas y literatura', 'Enseñanza de la lengua, la literatura y los idiomas extranjeros.', 'Colegios, institutos de idiomas y proyectos educativos.', 1),
('Docencia en ciencias sociales', 'Enseñanza de las ciencias sociales en la educación escolar.', 'Colegios, instituciones educativas y proyectos pedagógicos.', 1),
('Educación física y deporte', 'Enseñanza del deporte, la recreación y la actividad física.', 'Colegios, clubes deportivos, recreación y entrenamiento.', 1),
('Educación infantil y artística', 'Formación y acompañamiento de niños y enseñanza de las artes.', 'Jardines infantiles, colegios y proyectos culturales.', 1);

-- 3. Áreas de cada carrera nueva
-- Áreas: 1 Tecnología, 2 Salud, 3 Arte y Diseño, 4 Administración,
--        5 Ciencias Sociales, 6 Educación, 7 Ciencias
INSERT INTO carrera_area (id_carrera, id_area) VALUES
((SELECT id_carrera FROM carreras WHERE nombre = 'Arquitectura' LIMIT 1), 3),
((SELECT id_carrera FROM carreras WHERE nombre = 'Artes plásticas y visuales' LIMIT 1), 3),
((SELECT id_carrera FROM carreras WHERE nombre = 'Comunicación y periodismo' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Historia' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Sociología' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ciencia política' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Derecho' LIMIT 1), 5),
((SELECT id_carrera FROM carreras WHERE nombre = 'Negocios internacionales' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Turismo y hotelería' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería agronómica y agroindustrial' LIMIT 1), 7),
((SELECT id_carrera FROM carreras WHERE nombre = 'Ingeniería forestal y ecosistemas' LIMIT 1), 7),
((SELECT id_carrera FROM carreras WHERE nombre = 'Medicina veterinaria y zootecnia' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Medicina veterinaria y zootecnia' LIMIT 1), 7),
((SELECT id_carrera FROM carreras WHERE nombre = 'Topografía y modelación de proyectos de ingeniería' LIMIT 1), 1),
((SELECT id_carrera FROM carreras WHERE nombre = 'Seguridad y salud en el trabajo' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Seguridad y salud en el trabajo' LIMIT 1), 4),
((SELECT id_carrera FROM carreras WHERE nombre = 'Regencia de farmacia' LIMIT 1), 2),
((SELECT id_carrera FROM carreras WHERE nombre = 'Docencia en matemáticas y ciencias' LIMIT 1), 6),
((SELECT id_carrera FROM carreras WHERE nombre = 'Docencia en lenguas y literatura' LIMIT 1), 6),
((SELECT id_carrera FROM carreras WHERE nombre = 'Docencia en ciencias sociales' LIMIT 1), 6),
((SELECT id_carrera FROM carreras WHERE nombre = 'Educación física y deporte' LIMIT 1), 6),
((SELECT id_carrera FROM carreras WHERE nombre = 'Educación infantil y artística' LIMIT 1), 6);

-- 4. Tabla temporal con los programas del folleto
CREATE TEMPORARY TABLE tmp_prog (
    nombre      VARCHAR(150),
    tipo        VARCHAR(20),
    modalidad   VARCHAR(20),
    descripcion VARCHAR(255),
    carrera     VARCHAR(150)
);

INSERT INTO tmp_prog (nombre, tipo, modalidad, descripcion, carrera) VALUES
-- Presenciales
('Enfermería', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Enfermería'),
('Medicina', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Medicina'),
('Historia', 'universitario', 'presencial', NULL, 'Historia'),
('Sociología', 'universitario', 'presencial', NULL, 'Sociología'),
('Derecho', 'universitario', 'presencial', NULL, 'Derecho'),
('Economía', 'universitario', 'presencial', NULL, 'Economía'),
('Arquitectura', 'universitario', 'presencial', NULL, 'Arquitectura'),
('Biología', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Biología'),
('Química', 'universitario', 'presencial', 'Se ofrece solo en el semestre A.', 'Química'),
('Física', 'universitario', 'presencial', 'Se ofrece solo en el semestre A.', 'Física'),
('Ciencia Política', 'universitario', 'presencial', NULL, 'Ciencia política'),
('Diseño Interactivo y Multimedia', 'universitario', 'presencial', NULL, 'Diseño digital, multimedia y animación'),
('Ingeniería Forestal', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Ingeniería forestal y ecosistemas'),
('Ingeniería Agronómica', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Ingeniería agronómica y agroindustrial'),
('Ingeniería Agroindustrial', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Ingeniería agronómica y agroindustrial'),
('Administración de Empresas', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Administración de Empresas'),
('Comunicación Social - Periodismo', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Comunicación y periodismo'),
('Negocios Internacionales', 'universitario', 'presencial', NULL, 'Negocios internacionales'),
('Licenciatura en Ciencias Sociales', 'universitario', 'presencial', NULL, 'Docencia en ciencias sociales'),
('Artes Plásticas y Visuales', 'universitario', 'presencial', NULL, 'Artes plásticas y visuales'),
('Medicina Veterinaria y Zootecnia', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Medicina veterinaria y zootecnia'),
('Matemáticas con Énfasis en Estadística', 'universitario', 'presencial', NULL, 'Matemáticas'),
('Tecnología en Levantamientos Topográficos', 'tecnologico', 'presencial', NULL, 'Topografía y modelación de proyectos de ingeniería'),
('Tecnología en Modelación de Proyectos de Arquitectura e Ingeniería', 'tecnologico', 'presencial', NULL, 'Topografía y modelación de proyectos de ingeniería'),
('Licenciatura en Matemáticas', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Docencia en matemáticas y ciencias'),
('Licenciatura en Ciencias Naturales y Educación Ambiental', 'universitario', 'presencial', NULL, 'Docencia en matemáticas y ciencias'),
('Licenciatura en Educación Física, Recreación y Deportes', 'universitario', 'presencial', 'Programa acreditado de alta calidad.', 'Educación física y deporte'),
('Licenciatura en Literatura y Lengua Castellana', 'universitario', 'presencial', NULL, 'Docencia en lenguas y literatura'),
('Licenciatura en Lenguas Extranjeras con Énfasis en Inglés', 'universitario', 'presencial', NULL, 'Docencia en lenguas y literatura'),
-- A distancia
('Licenciatura en Literatura y Lengua Castellana', 'universitario', 'distancia', 'Programa acreditado de alta calidad.', 'Docencia en lenguas y literatura'),
('Seguridad y Salud en el Trabajo', 'universitario', 'distancia', NULL, 'Seguridad y salud en el trabajo'),
('Ingeniería de Sistemas', 'universitario', 'distancia', NULL, 'Ingeniería de Sistemas y Software'),
('Licenciatura en Educación Infantil', 'universitario', 'distancia', NULL, 'Educación infantil y artística'),
('Licenciatura en Educación Artística', 'universitario', 'distancia', NULL, 'Educación infantil y artística'),
('Licenciatura en Ciencias Naturales y Educación Ambiental', 'universitario', 'distancia', 'Programa acreditado de alta calidad.', 'Docencia en matemáticas y ciencias'),
('Ingeniería en Agroecología', 'universitario', 'distancia', NULL, 'Ingeniería agronómica y agroindustrial'),
('Administración Financiera', 'universitario', 'distancia', NULL, 'Contaduría y gestión financiera'),
('Tecnología en Regencia de Farmacia', 'tecnologico', 'distancia', NULL, 'Regencia de farmacia'),
('Tecnología en Protección y Recuperación de Ecosistemas Forestales', 'tecnologico', 'distancia', NULL, 'Ingeniería forestal y ecosistemas'),
('Administración de Empresas Turísticas y Hoteleras', 'universitario', 'distancia', NULL, 'Turismo y hotelería'),
('Contaduría Pública', 'universitario', 'distancia', NULL, 'Contaduría y gestión financiera');

-- 5. Programas (la duración queda vacía: el folleto no la trae)
INSERT INTO programas
    (id_institucion, nombre, tipo, descripcion, ciudad, modalidad, sitio_web, estado)
SELECT @ut, nombre, tipo, descripcion, 'Ibagué', modalidad, NULL, 1
FROM tmp_prog;

-- 6. Enlazar cada programa con su carrera
INSERT INTO programa_carrera (id_programa, id_carrera)
SELECT p.id_programa, c.id_carrera
FROM tmp_prog t
INNER JOIN programas p
    ON p.nombre = t.nombre
   AND p.modalidad = t.modalidad
   AND p.id_institucion = @ut
INNER JOIN carreras c
    ON c.nombre = t.carrera;

DROP TEMPORARY TABLE tmp_prog;