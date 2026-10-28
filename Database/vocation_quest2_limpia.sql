-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 28-10-2026 a las 06:26:58
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `vocation_quest2`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `administradores`
--

CREATE TABLE `administradores` (
  `id_administrador` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `administradores`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `areas`
--

CREATE TABLE `areas` (
  `id_area` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `areas`
--

INSERT INTO `areas` (`id_area`, `nombre`, `descripcion`) VALUES
(1, 'Tecnología', 'Área relacionada con tecnología, programación e innovación.'),
(2, 'Salud', 'Área relacionada con el cuidado y bienestar de las personas.'),
(3, 'Arte y Diseño', 'Área relacionada con creatividad, expresión y diseño.'),
(4, 'Administración', 'Área relacionada con organización, gestión y negocios.'),
(5, 'Ciencias Sociales', 'Área relacionada con sociedad, comunicación y comportamiento humano.'),
(6, 'Educación', 'Área relacionada con enseñanza, aprendizaje y formación.'),
(7, 'Ciencias', 'Área relacionada con investigación, análisis y conocimiento científico.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carreras`
--

CREATE TABLE `carreras` (
  `id_carrera` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `perfil_profesional` text DEFAULT NULL,
  `campo_laboral` text DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrera_area`
--

CREATE TABLE `carrera_area` (
  `id_carrera` int(11) NOT NULL,
  `id_area` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiantes`
--

CREATE TABLE `estudiantes` (
  `id_estudiante` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `edad` int(11) NOT NULL,
  `grado` varchar(20) DEFAULT NULL,
  `fecha_nacimiento` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `estudiantes`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_logro`
--

CREATE TABLE `estudiante_logro` (
  `id_estudiante` int(11) NOT NULL,
  `id_logro` int(11) NOT NULL,
  `fecha_obtencion` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instituciones`
--

CREATE TABLE `instituciones` (
  `id_institucion` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `tipo` varchar(100) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `sitio_web` varchar(255) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `intentos_prueba`
--

CREATE TABLE `intentos_prueba` (
  `id_intento` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `id_prueba` int(11) NOT NULL,
  `fecha_inicio` datetime DEFAULT current_timestamp(),
  `fecha_fin` datetime DEFAULT NULL,
  `completado` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `intentos_prueba`
--


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logros`
--

CREATE TABLE `logros` (
  `id_logro` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `puntos` int(11) NOT NULL DEFAULT 0,
  `tipo` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `logros`
--

INSERT INTO `logros` (`id_logro`, `nombre`, `descripcion`, `puntos`, `tipo`) VALUES
(1, 'En marcha', 'Responde tu primera pregunta.', 5, 'preguntas_1'),
(2, 'Primer paso', 'Completa tu primer nivel.', 10, 'niveles_1'),
(3, 'Curioso', 'Responde 10 preguntas.', 15, 'preguntas_10'),
(4, 'Explorador', 'Completa 3 niveles.', 20, 'niveles_3'),
(5, 'Constante', 'Responde 20 preguntas.', 30, 'preguntas_20'),
(6, 'Gran descubrimiento', 'Finaliza tu proceso vocacional.', 50, 'niveles_5');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opciones_respuesta`
--

CREATE TABLE `opciones_respuesta` (
  `id_opcion` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `texto` text NOT NULL,
  `orden` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `opciones_respuesta`
--

INSERT INTO `opciones_respuesta` (`id_opcion`, `id_pregunta`, `texto`, `orden`) VALUES
(1, 1, 'Crear algo usando un computador o una herramienta tecnológica.', 1),
(2, 1, 'Ayudar a alguien que necesita apoyo o acompañamiento.', 2),
(3, 1, 'Dibujar, diseñar o crear algo visualmente llamativo.', 3),
(4, 1, 'Investigar cómo funciona algo y descubrir por qué sucede.', 4),
(5, 2, 'Encontrar una solución para un problema usando lógica y tecnología.', 1),
(6, 2, 'Buscar una solución que ayude a mejorar la vida de otras personas.', 2),
(7, 2, 'Crear una idea original que nadie haya hecho antes.', 3),
(8, 2, 'Analizar información hasta encontrar una explicación.', 4),
(9, 3, 'Organizar las tareas y asegurarme de que todo avance.', 1),
(10, 3, 'Escuchar las ideas de todos y ayudar a que el grupo se entienda.', 2),
(11, 3, 'Proponer ideas creativas para el proyecto.', 3),
(12, 3, 'Investigar información y aportar datos para tomar decisiones.', 4),
(13, 4, 'Aprender a utilizar una herramienta, programa o dispositivo nuevo.', 1),
(14, 4, 'Explicar algo que sabes para ayudar a otra persona a aprenderlo.', 2),
(15, 4, 'Crear diseños, imágenes, videos u otros contenidos.', 3),
(16, 4, 'Hacer experimentos y comprobar qué sucede.', 4),
(17, 5, 'Crear una aplicación o solución tecnológica.', 1),
(18, 5, 'Participar en un proyecto para ayudar a una comunidad.', 2),
(19, 5, 'Diseñar la imagen y presentación de un proyecto.', 3),
(20, 5, 'Investigar un problema y analizar posibles soluciones.', 4),
(21, 6, 'Practicar directamente hasta aprender cómo funciona.', 1),
(22, 6, 'Leer información y analizarla con atención.', 2),
(23, 6, 'Crear ejemplos, dibujos o formas diferentes de entenderlo.', 3),
(24, 6, 'Explicárselo a otra persona para comprobar que lo entendí.', 4),
(25, 7, 'Busco diferentes formas de solucionarlo usando herramientas o tecnología.', 1),
(26, 7, 'Investigo información hasta encontrar una explicación.', 2),
(27, 7, 'Pienso en una solución diferente o creativa.', 3),
(28, 7, 'Pregunto a otras personas y escucho sus ideas.', 4),
(29, 8, 'Resolver problemas utilizando lógica.', 1),
(30, 8, 'Comprender y analizar información.', 2),
(31, 8, 'Crear diseños, ideas o contenidos originales.', 3),
(32, 8, 'Comunicarme mejor y trabajar con otras personas.', 4),
(33, 9, 'Organizar las tareas y buscar la manera de hacerlas más eficientes.', 1),
(34, 9, 'Investigar información y sacar conclusiones.', 2),
(35, 9, 'Crear la presentación, diseño o parte visual.', 3),
(36, 9, 'Explicar el proyecto y ayudar a coordinar al equipo.', 4),
(37, 10, 'Haber encontrado una solución que funciona.', 1),
(38, 10, 'Haber descubierto algo que antes no entendía.', 2),
(39, 10, 'Haber creado algo original.', 3),
(40, 10, 'Haber ayudado o trabajado bien con otras personas.', 4),
(41, 11, 'Me gusta planear todo antes de comenzar.', 1),
(42, 11, 'Prefiero analizar las diferentes posibilidades primero.', 2),
(43, 11, 'Me gusta dejar espacio para cambiar y probar ideas nuevas.', 3),
(44, 11, 'Prefiero organizarme con otras personas y repartir las tareas.', 4),
(45, 12, 'Analizo las ventajas y desventajas de cada opción.', 1),
(46, 12, 'Pienso en cómo puede afectar mi decisión a otras personas.', 2),
(47, 12, 'Confío en mi intuición y en lo que siento que es mejor.', 3),
(48, 12, 'Busco información y diferentes opiniones antes de decidir.', 4),
(49, 13, 'Me gusta asumir responsabilidades y ayudar a organizar el grupo.', 1),
(50, 13, 'Prefiero escuchar a los demás y buscar acuerdos.', 2),
(51, 13, 'Me gusta aportar ideas y mantener un ambiente agradable.', 3),
(52, 13, 'Prefiero trabajar de manera independiente y concentrarme en mi tarea.', 4),
(53, 14, 'Intento encontrar rápidamente una solución al problema.', 1),
(54, 14, 'Analizo qué salió mal antes de actuar.', 2),
(55, 14, 'Busco una forma diferente de hacer las cosas.', 3),
(56, 14, 'Pido ayuda o consejo para encontrar una solución.', 4),
(57, 15, 'Un ambiente organizado donde pueda concentrarme.', 1),
(58, 15, 'Un ambiente donde pueda investigar y aprender constantemente.', 2),
(59, 15, 'Un ambiente creativo donde pueda expresar mis ideas.', 3),
(60, 15, 'Un ambiente donde pueda colaborar y relacionarme con otras personas.', 4),
(61, 16, 'Resolver problemas y encontrar soluciones.', 1),
(62, 16, 'Ayudar y trabajar directamente con otras personas.', 2),
(63, 16, 'Crear, diseñar o expresar ideas.', 3),
(64, 16, 'Investigar, analizar y descubrir cosas nuevas.', 4),
(65, 17, 'Tener oportunidades para aprender y desarrollar mis habilidades.', 1),
(66, 17, 'Poder ayudar a otras personas o aportar a la sociedad.', 2),
(67, 17, 'Tener libertad para crear y desarrollar mis propias ideas.', 3),
(68, 17, 'Tener retos que me permitan analizar y resolver problemas.', 4),
(69, 18, 'Una aplicación, herramienta o solución tecnológica.', 1),
(70, 18, 'Un proyecto para mejorar la vida de una comunidad.', 2),
(71, 18, 'Una campaña, diseño o proyecto creativo.', 3),
(72, 18, 'Una investigación para comprender un problema.', 4),
(73, 19, 'Crear soluciones útiles y eficientes.', 1),
(74, 19, 'Ayudar a las personas y generar un impacto positivo.', 2),
(75, 19, 'Expresar mi creatividad y hacer realidad mis ideas.', 3),
(76, 19, 'Aprender constantemente y descubrir nuevos conocimientos.', 4),
(77, 20, 'Un lugar donde pueda utilizar tecnología y resolver problemas.', 1),
(78, 20, 'Un lugar donde pueda trabajar con personas y ayudarlas.', 2),
(79, 20, 'Un lugar creativo donde pueda desarrollar nuevas ideas.', 3),
(80, 20, 'Un lugar donde pueda investigar, analizar y aprender.', 4),
(81, 21, 'Tecnología, programación y creación de soluciones digitales.', 1),
(82, 21, 'Salud, bienestar y ayuda a las personas.', 2),
(83, 21, 'Arte, diseño y creación de contenidos.', 3),
(84, 21, 'Ciencia, investigación y análisis.', 4),
(85, 22, 'Diseñar o desarrollar una solución usando tecnología.', 1),
(86, 22, 'Trabajar directamente con personas y apoyarlas.', 2),
(87, 22, 'Crear ideas, diseños o proyectos originales.', 3),
(88, 22, 'Investigar, analizar información y encontrar respuestas.', 4),
(89, 23, 'Crear una aplicación, página web o herramienta tecnológica.', 1),
(90, 23, 'Desarrollar un proyecto para ayudar a una comunidad.', 2),
(91, 23, 'Crear la imagen, diseño o contenido de un proyecto.', 3),
(92, 23, 'Investigar un problema y proponer posibles soluciones.', 4),
(93, 24, 'Que me permita resolver problemas y aprender nuevas tecnologías.', 1),
(94, 24, 'Que me permita ayudar a otras personas y generar un impacto positivo.', 2),
(95, 24, 'Que me permita expresar mi creatividad y desarrollar ideas.', 3),
(96, 24, 'Que me permita investigar, aprender y descubrir cosas nuevas.', 4),
(97, 25, 'Quiero crear soluciones y trabajar con tecnología.', 1),
(98, 25, 'Quiero ayudar a las personas y contribuir a la sociedad.', 2),
(99, 25, 'Quiero crear, diseñar y expresar mis ideas.', 3),
(100, 25, 'Quiero investigar, analizar y comprender cómo funcionan las cosas.', 4),
(1001, 101, 'Probar una app, un juego o un aparato y averiguar cómo funciona por dentro.', 1),
(1002, 101, 'Dibujar, grabar un video o crear algo con tu propio estilo.', 2),
(1003, 101, 'Ver un documental o conversar sobre por qué las personas pensamos tan distinto.', 3),
(1004, 101, 'Hacerte una pregunta rara, como por qué cambia el color del cielo, y buscar la respuesta.', 4),
(1005, 102, 'Ser monitor de niños más pequeños y enseñarles algo nuevo.', 1),
(1006, 102, 'Montar un negocio pequeño: precios, ventas y cuentas.', 2),
(1007, 102, 'Periodismo y debate: investigar un tema y presentarlo ante el público.', 3),
(1008, 102, 'Laboratorio: hacer experimentos y anotar qué pasa en cada uno.', 4),
(1009, 103, 'Arreglar computadores viejos para donarlos a escuelas.', 1),
(1010, 103, 'Recoger las historias de vida de gente de tu comunidad.', 2),
(1011, 103, 'Acompañar a personas mayores en un hogar de cuidado.', 3),
(1012, 103, 'Dar refuerzo escolar a niños de tu barrio.', 4),
(1013, 104, 'Presentar el evento, hablar con la gente y lograr que todos se integren.', 1),
(1014, 104, 'Diseñar la decoración, el afiche y el ambiente del lugar.', 2),
(1015, 104, 'Coordinar al equipo: tareas, presupuesto y horarios.', 3),
(1016, 104, 'Encargarte de los primeros auxilios y de que todos estén cómodos.', 4),
(1017, 105, 'Nutrición y ejercicio: cómo cuidar el cuerpo.', 1),
(1018, 105, 'Cómo se programa un videojuego o una página web.', 2),
(1019, 105, 'Astronomía, biología o química para entender cómo funciona el mundo.', 3),
(1020, 105, 'Cómo crear un emprendimiento desde cero.', 4),
(1021, 106, 'El de arte: pintura en vivo, música y fotografía.', 1),
(1022, 106, 'El de experimentos: reacciones químicas y fenómenos físicos.', 2),
(1023, 106, 'El de enseñanza: juegos para aprender de forma divertida.', 3),
(1024, 106, 'El de bienestar: pruebas de reflejos, pulso y consejos para cuidarse.', 4),
(1025, 107, 'Organizar una venta de comida para recoger fondos.', 1),
(1026, 107, 'Diseñar el logo, el uniforme o los letreros del colegio.', 2),
(1027, 107, 'Crear la página web o la aplicación del colegio.', 3),
(1028, 107, 'Armar un programa de tutorías entre compañeros.', 4),
(1029, 108, 'Armar un plan: quién hace qué y en qué orden.', 1),
(1030, 108, 'Plantear una explicación posible y comprobarla con una prueba.', 2),
(1031, 108, 'Revisar paso a paso hasta encontrar la falla y probar una solución.', 3),
(1032, 108, 'Ver si alguien salió afectado y atenderlo primero; lo demás viene después.', 4),
(1033, 109, 'Preguntarles cómo se sienten y cuidar que descansen y se sientan bien.', 1),
(1034, 109, 'Dividir el trabajo en metas pequeñas para que vean avances.', 2),
(1035, 109, 'Reunirlos a hablar para entender qué está pasando entre ellos.', 3),
(1036, 109, 'Proponer una actividad creativa que cambie el ambiente.', 4),
(1037, 110, 'Entender el punto de vista de personas muy diferentes a ti.', 1),
(1038, 110, 'Explicar un tema difícil hasta que la otra persona lo entienda.', 2),
(1039, 110, 'Analizar datos o pistas para llegar a una conclusión sólida.', 3),
(1040, 110, 'Convencer a otros de apoyar una idea y conseguir lo necesario para hacerla.', 4),
(1041, 111, 'Busco un tutorial, una app o una simulación que se lo muestre en pantalla.', 1),
(1042, 111, 'Se lo explico con ejemplos y dibujos hasta que le quede claro.', 2),
(1043, 111, 'Primero lo tranquilizo, porque con estrés nadie aprende.', 3),
(1044, 111, 'Le pregunto cómo piensa y en qué punto se confunde.', 4),
(1045, 112, 'Imaginación: ver posibilidades donde otros ven un espacio vacío.', 1),
(1046, 112, 'Rigor: dudar, comprobar y no quedarme con la primera respuesta.', 2),
(1047, 112, 'Lógica: encontrar patrones y armar sistemas que funcionen.', 3),
(1048, 112, 'Observación: notar el ambiente y lo que la gente no dice.', 4),
(1049, 113, 'Preparar y dar una clase corta sobre algo que dominas.', 1),
(1050, 113, 'Medir algo de tu entorno, como el agua o el ruido, y sacar conclusiones.', 2),
(1051, 113, 'Diseñar una rutina de bienestar para tus compañeros y ver si les sirve.', 3),
(1052, 113, 'Crear una pieza de arte o música que cuente una idea importante.', 4),
(1053, 114, 'El diseño: que se vea claro, atractivo y con identidad.', 1),
(1054, 114, 'Las herramientas digitales: la presentación, el video y que todo funcione.', 2),
(1055, 114, 'Enseñar al grupo a exponer y ayudar a quien le dé nervios.', 3),
(1056, 114, 'La logística: tiempos, ensayos y que todos sepan su parte.', 4),
(1057, 115, 'Alguien con ideas originales y un estilo propio.', 1),
(1058, 115, 'Alguien que cuida a los demás y se da cuenta cuando algo anda mal.', 2),
(1059, 115, 'Alguien paciente que disfruta ayudar a otros a crecer.', 3),
(1060, 115, 'Alguien curioso que siempre pregunta el porqué de las cosas.', 4),
(1061, 116, 'El de quien organiza, toma decisiones y mantiene el ritmo.', 1),
(1062, 116, 'El de quien apoya a los demás para que todos aprendan y avancen.', 2),
(1063, 116, 'El de quien aporta la idea creativa que cambia el rumbo.', 3),
(1064, 116, 'El de quien resuelve lo técnico y encuentra atajos para ir más rápido.', 4),
(1065, 117, 'Entender bien el problema antes de actuar, aunque tarde un poco más.', 1),
(1066, 117, 'Cuidarme: dormir, comer bien y hacer pausas para rendir mejor.', 2),
(1067, 117, 'Priorizar: lo importante primero y lo demás después.', 3),
(1068, 117, 'Automatizar lo repetitivo para ganar tiempo.', 4),
(1069, 118, 'Haber logrado que algo avanzara y funcionara mejor que ayer.', 1),
(1070, 118, 'Descubrir un dato nuevo que cambia lo que pensaba.', 2),
(1071, 118, 'Haber tenido una conversación que me hizo ver algo desde otro lado.', 3),
(1072, 118, 'Ver que alguien por fin entendió lo que le expliqué.', 4),
(1073, 119, 'Que dé voz a personas que casi nunca son escuchadas.', 1),
(1074, 119, 'Que ayude a las personas a sentirse mejor, en su cuerpo o en su ánimo.', 2),
(1075, 119, 'Que sea sostenible: con presupuesto, equipo y metas claras.', 3),
(1076, 119, 'Que sea hermoso y distinto a todo lo que existe.', 4),
(1077, 120, 'Propongo reglas claras y un sistema sencillo para votar y decidir.', 1),
(1078, 120, 'Les ayudo a escucharse y a explicar su punto sin pelear.', 2),
(1079, 120, 'Bajo el tono, escucho a todos y cuido que nadie se sienta mal.', 3),
(1080, 120, 'Busco entender qué hay detrás: intereses, miedos y diferencias.', 4),
(1081, 121, 'Silencio, un computador y tiempo para concentrarme en problemas complejos.', 1),
(1082, 121, 'Un grupo con el que discutir ideas y mirar el mundo desde varios lados.', 2),
(1083, 121, 'Un laboratorio o una salida de campo, midiendo y observando.', 3),
(1084, 121, 'Un espacio libre, con materiales para crear y probar.', 4),
(1085, 122, 'Ver cómo mejora la salud o el ánimo de personas gracias a lo que haces.', 1),
(1086, 122, 'Participar en decisiones que mejoran la vida de una comunidad.', 2),
(1087, 122, 'Mostrar al mundo algo creado por ti, con tu sello personal.', 3),
(1088, 122, 'Dirigir tu propio proyecto con un equipo que confía en ti.', 4),
(1089, 123, 'En una organización que estudia y trabaja de cerca con comunidades.', 1),
(1090, 123, 'En un salón o espacio de formación, rodeado de personas que aprenden.', 2),
(1091, 123, 'En un equipo que desarrolla productos digitales que usa mucha gente.', 3),
(1092, 123, 'En un lugar donde cada día atiendes a personas que te necesitan.', 4),
(1093, 124, 'Para conocer otras culturas y formas de vivir.', 1),
(1094, 124, 'Para aprender a crear y manejar un negocio propio.', 2),
(1095, 124, 'Para participar en una investigación científica de verdad.', 3),
(1096, 124, 'Para formarte mejor y poder enseñar a otros.', 4),
(1097, 125, 'Entender mejor el clima, la naturaleza o las enfermedades.', 1),
(1098, 125, 'Mejorar el acceso a la salud y al bienestar.', 2),
(1099, 125, 'Conseguir que más ideas se conviertan en empleos y negocios.', 3),
(1100, 125, 'Lograr que la tecnología sea segura y útil para todas las personas.', 4),
(1101, 126, 'Acompañar a jóvenes a descubrir su camino.', 1),
(1102, 126, 'Crear herramientas o programas que hagan la vida más fácil.', 2),
(1103, 126, 'Coordinar proyectos y equipos para que todo salga bien.', 3),
(1104, 126, 'Diseñar productos, espacios o imágenes que la gente recuerde.', 4),
(1105, 127, 'Que aportó un descubrimiento que antes nadie conocía.', 1),
(1106, 127, 'Que su estilo se reconoce a primera vista.', 2),
(1107, 127, 'Que ayudó a entender mejor a las personas y a la sociedad.', 3),
(1108, 127, 'Que gracias a él, algo complejo ahora es sencillo y funciona.', 4),
(1109, 128, 'Cómo cuidar la salud mental y física de los estudiantes.', 1),
(1110, 128, 'Una exposición artística sobre algo que te importa.', 2),
(1111, 128, 'Una investigación sobre un problema ambiental de tu región.', 3),
(1112, 128, 'Un método divertido para que a todos les guste aprender.', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `opcion_area`
--

CREATE TABLE `opcion_area` (
  `id_opcion_area` int(11) NOT NULL,
  `id_opcion` int(11) NOT NULL,
  `id_area` int(11) NOT NULL,
  `puntos` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `opcion_area`
--

INSERT INTO `opcion_area` (`id_opcion_area`, `id_opcion`, `id_area`, `puntos`) VALUES
(1, 1, 1, 3),
(2, 1, 7, 1),
(3, 2, 2, 3),
(4, 2, 5, 2),
(5, 2, 6, 1),
(6, 3, 3, 3),
(7, 4, 7, 3),
(8, 4, 1, 1),
(9, 5, 1, 3),
(10, 5, 7, 2),
(11, 6, 2, 2),
(12, 6, 6, 2),
(13, 6, 5, 1),
(14, 7, 3, 3),
(15, 7, 1, 1),
(16, 8, 7, 3),
(17, 8, 4, 1),
(18, 9, 4, 3),
(19, 9, 1, 1),
(20, 10, 5, 3),
(21, 10, 6, 2),
(22, 11, 3, 3),
(23, 11, 5, 1),
(24, 12, 7, 3),
(25, 12, 1, 1),
(26, 13, 1, 3),
(27, 13, 7, 1),
(28, 14, 6, 3),
(29, 14, 5, 2),
(30, 15, 3, 3),
(31, 15, 1, 1),
(32, 16, 7, 3),
(33, 16, 2, 1),
(34, 17, 1, 3),
(35, 17, 7, 2),
(36, 18, 5, 3),
(37, 18, 6, 2),
(38, 19, 3, 3),
(39, 19, 4, 1),
(40, 20, 7, 3),
(41, 20, 4, 1),
(42, 20, 1, 1),
(43, 21, 1, 3),
(44, 21, 7, 2),
(45, 22, 7, 3),
(46, 22, 1, 1),
(47, 23, 3, 3),
(48, 24, 6, 2),
(49, 24, 5, 3),
(50, 25, 1, 3),
(51, 25, 7, 2),
(52, 26, 7, 3),
(53, 26, 1, 1),
(54, 27, 3, 3),
(55, 28, 5, 2),
(56, 28, 6, 2),
(57, 29, 1, 3),
(58, 29, 7, 1),
(59, 30, 7, 3),
(60, 30, 5, 1),
(61, 31, 3, 3),
(62, 31, 5, 1),
(63, 32, 5, 3),
(64, 32, 6, 2),
(65, 33, 4, 3),
(66, 33, 1, 1),
(67, 34, 5, 3),
(68, 34, 7, 1),
(69, 35, 3, 3),
(70, 36, 6, 3),
(71, 36, 5, 2),
(72, 37, 1, 3),
(73, 37, 7, 1),
(74, 38, 7, 3),
(75, 38, 1, 1),
(76, 39, 3, 3),
(77, 40, 5, 1),
(78, 40, 6, 2),
(106, 21, 1, 3),
(107, 21, 7, 2),
(108, 22, 7, 3),
(109, 22, 1, 1),
(110, 23, 3, 3),
(111, 24, 6, 2),
(112, 24, 5, 3),
(113, 25, 1, 3),
(114, 25, 7, 2),
(115, 26, 7, 3),
(116, 26, 1, 1),
(117, 27, 3, 3),
(118, 28, 5, 2),
(119, 28, 6, 2),
(120, 29, 1, 3),
(121, 29, 7, 1),
(122, 30, 7, 3),
(123, 30, 5, 1),
(124, 31, 3, 3),
(125, 31, 5, 1),
(126, 32, 5, 3),
(127, 32, 6, 2),
(128, 33, 4, 3),
(129, 33, 1, 1),
(130, 34, 5, 3),
(131, 34, 7, 1),
(132, 35, 3, 3),
(133, 36, 6, 3),
(134, 36, 5, 2),
(135, 37, 1, 3),
(136, 37, 7, 1),
(137, 38, 7, 3),
(138, 38, 1, 1),
(139, 39, 3, 3),
(140, 40, 5, 1),
(141, 40, 6, 2),
(169, 41, 4, 3),
(170, 42, 7, 3),
(171, 42, 5, 1),
(172, 43, 3, 3),
(173, 44, 5, 2),
(174, 44, 6, 2),
(175, 45, 7, 3),
(176, 45, 1, 1),
(177, 46, 5, 2),
(178, 46, 6, 2),
(179, 47, 3, 3),
(180, 47, 4, 1),
(181, 48, 7, 3),
(182, 48, 1, 1),
(183, 49, 4, 3),
(184, 49, 1, 1),
(185, 50, 5, 3),
(186, 50, 6, 2),
(187, 51, 3, 3),
(188, 51, 5, 1),
(189, 52, 1, 2),
(190, 52, 5, 2),
(191, 52, 6, 2),
(192, 53, 1, 3),
(193, 53, 4, 1),
(194, 54, 7, 3),
(195, 54, 5, 1),
(196, 55, 3, 3),
(197, 55, 1, 1),
(198, 56, 5, 2),
(199, 56, 6, 2),
(200, 57, 1, 3),
(201, 57, 4, 1),
(202, 58, 7, 3),
(203, 58, 5, 1),
(204, 59, 3, 3),
(205, 59, 4, 1),
(206, 60, 5, 2),
(207, 60, 6, 3),
(208, 61, 1, 3),
(209, 61, 4, 1),
(210, 62, 5, 3),
(211, 62, 6, 2),
(212, 63, 3, 3),
(213, 63, 4, 1),
(214, 64, 7, 3),
(215, 64, 5, 1),
(216, 65, 1, 3),
(217, 65, 7, 1),
(218, 66, 5, 3),
(219, 66, 6, 2),
(220, 67, 3, 3),
(221, 67, 4, 1),
(222, 68, 7, 3),
(223, 68, 1, 1),
(224, 69, 1, 3),
(225, 69, 7, 2),
(226, 70, 5, 3),
(227, 70, 6, 2),
(228, 71, 3, 3),
(229, 71, 4, 1),
(230, 72, 7, 3),
(231, 72, 5, 1),
(232, 73, 1, 3),
(233, 73, 4, 1),
(234, 74, 5, 3),
(235, 74, 6, 2),
(236, 75, 3, 3),
(237, 75, 4, 1),
(238, 76, 7, 3),
(239, 76, 5, 1),
(240, 77, 1, 3),
(241, 77, 7, 1),
(242, 78, 5, 3),
(243, 78, 6, 2),
(244, 79, 3, 3),
(245, 79, 4, 1),
(246, 80, 7, 3),
(247, 80, 1, 1),
(248, 81, 1, 3),
(249, 81, 7, 1),
(250, 82, 2, 3),
(251, 82, 5, 2),
(252, 82, 6, 1),
(253, 83, 3, 3),
(254, 83, 4, 1),
(255, 84, 7, 3),
(256, 84, 5, 1),
(257, 85, 1, 3),
(258, 85, 7, 1),
(259, 86, 2, 3),
(260, 86, 6, 2),
(261, 86, 5, 1),
(262, 87, 3, 3),
(263, 87, 4, 1),
(264, 88, 7, 3),
(265, 88, 1, 1),
(266, 89, 1, 3),
(267, 89, 7, 2),
(268, 90, 5, 3),
(269, 90, 6, 2),
(270, 91, 3, 3),
(271, 91, 4, 1),
(272, 92, 7, 3),
(273, 92, 5, 1),
(274, 93, 1, 3),
(275, 93, 7, 1),
(276, 94, 2, 3),
(277, 94, 5, 2),
(278, 94, 6, 1),
(279, 95, 3, 3),
(280, 95, 4, 1),
(281, 96, 7, 3),
(282, 96, 5, 1),
(283, 97, 1, 3),
(284, 97, 7, 1),
(285, 98, 2, 3),
(286, 98, 5, 2),
(287, 98, 6, 1),
(288, 99, 3, 3),
(289, 99, 4, 1),
(290, 100, 7, 3),
(291, 100, 5, 1),
(292, 1001, 1, 3),
(293, 1001, 7, 1),
(294, 1002, 3, 3),
(295, 1002, 1, 1),
(296, 1003, 5, 3),
(297, 1003, 3, 1),
(298, 1004, 7, 3),
(299, 1004, 2, 1),
(300, 1005, 6, 3),
(301, 1005, 2, 1),
(302, 1006, 4, 3),
(303, 1006, 3, 1),
(304, 1007, 5, 3),
(305, 1007, 3, 1),
(306, 1008, 7, 3),
(307, 1008, 1, 1),
(308, 1009, 1, 3),
(309, 1009, 6, 1),
(310, 1010, 5, 3),
(311, 1010, 3, 1),
(312, 1011, 2, 3),
(313, 1011, 5, 1),
(314, 1012, 6, 3),
(315, 1012, 4, 1),
(316, 1013, 5, 3),
(317, 1013, 4, 1),
(318, 1014, 3, 3),
(319, 1014, 5, 1),
(320, 1015, 4, 3),
(321, 1015, 1, 1),
(322, 1016, 2, 3),
(323, 1016, 4, 1),
(324, 1017, 2, 3),
(325, 1017, 7, 1),
(326, 1018, 1, 3),
(327, 1018, 3, 1),
(328, 1019, 7, 3),
(329, 1019, 2, 1),
(330, 1020, 4, 3),
(331, 1020, 1, 1),
(332, 1021, 3, 3),
(333, 1021, 6, 1),
(334, 1022, 7, 3),
(335, 1022, 1, 1),
(336, 1023, 6, 3),
(337, 1023, 3, 1),
(338, 1024, 2, 3),
(339, 1024, 7, 1),
(340, 1025, 4, 3),
(341, 1025, 6, 1),
(342, 1026, 3, 3),
(343, 1026, 4, 1),
(344, 1027, 1, 3),
(345, 1027, 3, 1),
(346, 1028, 6, 3),
(347, 1028, 4, 1),
(348, 1029, 4, 3),
(349, 1029, 1, 1),
(350, 1030, 7, 3),
(351, 1030, 2, 1),
(352, 1031, 1, 3),
(353, 1031, 7, 1),
(354, 1032, 2, 3),
(355, 1032, 6, 1),
(356, 1033, 2, 3),
(357, 1033, 5, 1),
(358, 1034, 4, 3),
(359, 1034, 1, 1),
(360, 1035, 5, 3),
(361, 1035, 2, 1),
(362, 1036, 3, 3),
(363, 1036, 6, 1),
(364, 1037, 5, 3),
(365, 1037, 6, 1),
(366, 1038, 6, 3),
(367, 1038, 7, 1),
(368, 1039, 7, 3),
(369, 1039, 2, 1),
(370, 1040, 4, 3),
(371, 1040, 3, 1),
(372, 1041, 1, 3),
(373, 1041, 7, 1),
(374, 1042, 6, 3),
(375, 1042, 3, 1),
(376, 1043, 2, 3),
(377, 1043, 5, 1),
(378, 1044, 5, 3),
(379, 1044, 2, 1),
(380, 1045, 3, 3),
(381, 1045, 5, 1),
(382, 1046, 7, 3),
(383, 1046, 5, 1),
(384, 1047, 1, 3),
(385, 1047, 7, 1),
(386, 1048, 5, 3),
(387, 1048, 3, 1),
(388, 1049, 6, 3),
(389, 1049, 3, 1),
(390, 1050, 7, 3),
(391, 1050, 2, 1),
(392, 1051, 2, 3),
(393, 1051, 7, 1),
(394, 1052, 3, 3),
(395, 1052, 6, 1),
(396, 1053, 3, 3),
(397, 1053, 4, 1),
(398, 1054, 1, 3),
(399, 1054, 3, 1),
(400, 1055, 6, 3),
(401, 1055, 4, 1),
(402, 1056, 4, 3),
(403, 1056, 6, 1),
(404, 1057, 3, 3),
(405, 1057, 5, 1),
(406, 1058, 2, 3),
(407, 1058, 6, 1),
(408, 1059, 6, 3),
(409, 1059, 2, 1),
(410, 1060, 7, 3),
(411, 1060, 1, 1),
(412, 1061, 4, 3),
(413, 1061, 6, 1),
(414, 1062, 6, 3),
(415, 1062, 2, 1),
(416, 1063, 3, 3),
(417, 1063, 5, 1),
(418, 1064, 1, 3),
(419, 1064, 7, 1),
(420, 1065, 7, 3),
(421, 1065, 4, 1),
(422, 1066, 2, 3),
(423, 1066, 7, 1),
(424, 1067, 4, 3),
(425, 1067, 1, 1),
(426, 1068, 1, 3),
(427, 1068, 4, 1),
(428, 1069, 4, 3),
(429, 1069, 1, 1),
(430, 1070, 7, 3),
(431, 1070, 2, 1),
(432, 1071, 5, 3),
(433, 1071, 6, 1),
(434, 1072, 6, 3),
(435, 1072, 5, 1),
(436, 1073, 5, 3),
(437, 1073, 3, 1),
(438, 1074, 2, 3),
(439, 1074, 7, 1),
(440, 1075, 4, 3),
(441, 1075, 1, 1),
(442, 1076, 3, 3),
(443, 1076, 4, 1),
(444, 1077, 1, 3),
(445, 1077, 4, 1),
(446, 1078, 6, 3),
(447, 1078, 2, 1),
(448, 1079, 2, 3),
(449, 1079, 5, 1),
(450, 1080, 5, 3),
(451, 1080, 6, 1),
(452, 1081, 1, 3),
(453, 1081, 7, 1),
(454, 1082, 5, 3),
(455, 1082, 6, 1),
(456, 1083, 7, 3),
(457, 1083, 3, 1),
(458, 1084, 3, 3),
(459, 1084, 7, 1),
(460, 1085, 2, 3),
(461, 1085, 7, 1),
(462, 1086, 5, 3),
(463, 1086, 4, 1),
(464, 1087, 3, 3),
(465, 1087, 1, 1),
(466, 1088, 4, 3),
(467, 1088, 5, 1),
(468, 1089, 5, 3),
(469, 1089, 6, 1),
(470, 1090, 6, 3),
(471, 1090, 2, 1),
(472, 1091, 1, 3),
(473, 1091, 4, 1),
(474, 1092, 2, 3),
(475, 1092, 5, 1),
(476, 1093, 5, 3),
(477, 1093, 3, 1),
(478, 1094, 4, 3),
(479, 1094, 1, 1),
(480, 1095, 7, 3),
(481, 1095, 1, 1),
(482, 1096, 6, 3),
(483, 1096, 5, 1),
(484, 1097, 7, 3),
(485, 1097, 2, 1),
(486, 1098, 2, 3),
(487, 1098, 7, 1),
(488, 1099, 4, 3),
(489, 1099, 5, 1),
(490, 1100, 1, 3),
(491, 1100, 4, 1),
(492, 1101, 6, 3),
(493, 1101, 2, 1),
(494, 1102, 1, 3),
(495, 1102, 4, 1),
(496, 1103, 4, 3),
(497, 1103, 6, 1),
(498, 1104, 3, 3),
(499, 1104, 1, 1),
(500, 1105, 7, 3),
(501, 1105, 1, 1),
(502, 1106, 3, 3),
(503, 1106, 5, 1),
(504, 1107, 5, 3),
(505, 1107, 6, 1),
(506, 1108, 1, 3),
(507, 1108, 4, 1),
(508, 1109, 2, 3),
(509, 1109, 7, 1),
(510, 1110, 3, 3),
(511, 1110, 5, 1),
(512, 1111, 7, 3),
(513, 1111, 2, 1),
(514, 1112, 6, 3),
(515, 1112, 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preguntas`
--

CREATE TABLE `preguntas` (
  `id_pregunta` int(11) NOT NULL,
  `id_prueba` int(11) NOT NULL,
  `pregunta` text NOT NULL,
  `orden` int(11) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `preguntas`
--

INSERT INTO `preguntas` (`id_pregunta`, `id_prueba`, `pregunta`, `orden`, `estado`) VALUES
(1, 1, 'Si tuvieras que elegir una actividad para realizar durante una tarde, ¿cuál preferirías?', 1, 0),
(2, 1, '¿Qué tipo de reto te llamaría más la atención?', 2, 0),
(3, 1, 'Cuando trabajas en grupo, ¿qué papel te gustaría asumir?', 3, 0),
(4, 1, '¿Cuál de estas actividades te parece más interesante?', 4, 0),
(5, 1, 'Si pudieras participar en un proyecto, ¿cuál escogerías?', 5, 0),
(6, 2, 'Cuando tienes que aprender algo nuevo, ¿qué forma de aprender prefieres?', 1, 0),
(7, 2, 'Si encuentras un problema que no sabes solucionar, ¿qué haces primero?', 2, 0),
(8, 2, '¿Cuál de estas habilidades te gustaría desarrollar más?', 3, 0),
(9, 2, 'En un proyecto escolar, ¿qué actividad se te facilitaría más?', 4, 0),
(10, 2, 'Cuando terminas una actividad difícil, ¿qué te produce mayor satisfacción?', 5, 0),
(11, 3, 'Cuando trabajas en un proyecto, ¿cómo prefieres organizarte?', 1, 0),
(12, 3, '¿Qué haces normalmente cuando tienes que tomar una decisión importante?', 2, 0),
(13, 3, '¿Cómo te sientes cuando tienes que trabajar con otras personas?', 3, 0),
(14, 3, 'Cuando algo no sale como esperabas, ¿cómo reaccionas?', 4, 0),
(15, 3, '¿Qué ambiente de trabajo te haría sentir más cómodo?', 5, 0),
(16, 4, '¿Qué tipo de actividad te gustaría realizar en un trabajo?', 1, 0),
(17, 4, '¿Qué aspecto valorarías más al elegir una profesión?', 2, 0),
(18, 4, '¿Qué tipo de proyecto te gustaría desarrollar?', 3, 0),
(19, 4, '¿Qué te gustaría lograr principalmente con tu trabajo?', 4, 0),
(20, 4, '¿En qué tipo de entorno profesional te imaginarías trabajando?', 5, 0),
(21, 5, 'Después de conocer mejor tus intereses y habilidades, ¿qué tipo de área te gustaría explorar primero?', 1, 0),
(22, 5, '¿Qué tipo de actividad profesional te imaginas disfrutando más?', 2, 0),
(23, 5, 'Si pudieras participar en un proyecto relacionado con tu futuro, ¿cuál elegirías?', 3, 0),
(24, 5, '¿Qué característica sería más importante para ti en una carrera?', 4, 0),
(25, 5, '¿Cuál de estas opciones representa mejor lo que buscas para tu futuro?', 5, 0),
(101, 1, 'Tienes una tarde libre y nadie te dice qué hacer. ¿Qué te llama más la atención?', 1, 1),
(102, 1, 'Tu colegio abre un taller electivo y puedes elegir uno. ¿Cuál escoges?', 2, 1),
(103, 1, 'Tu colegio abre inscripciones para un voluntariado. ¿En cuál te apuntas?', 3, 1),
(104, 1, 'Tu curso va a organizar una gran celebración. ¿Qué te gustaría hacer?', 4, 1),
(105, 1, 'Te regalan un mes de clases en línea para aprender lo que quieras. ¿Qué eliges?', 5, 1),
(106, 1, 'En una feria de ciencia y cultura, ¿qué puesto te daría más ganas de visitar?', 6, 1),
(107, 1, 'Si pudieras participar en un proyecto del colegio, ¿cuál escogerías?', 7, 1),
(108, 2, 'Algo no funciona y nadie sabe por qué. ¿Cuál es tu primer movimiento?', 1, 1),
(109, 2, 'Un grupo de tu curso está desanimado. ¿Cómo lo ayudas?', 2, 1),
(110, 2, '¿En cuál de estas situaciones te sientes más capaz?', 3, 1),
(111, 2, 'Un amigo no entiende un tema y te pide ayuda. ¿Qué haces?', 4, 1),
(112, 2, '¿Con cuál de estas habilidades te identificas más?', 5, 1),
(113, 2, 'Te dan un reto para cumplir en una semana. ¿Cuál prefieres?', 6, 1),
(114, 2, 'Tu grupo debe presentar un trabajo importante. ¿Qué parte te encargas?', 7, 1),
(115, 3, '¿Cómo te describirían mejor las personas que te conocen?', 1, 1),
(116, 3, 'Trabajando en equipo, ¿qué papel te sale de forma natural?', 2, 1),
(117, 3, 'Cuando tienes presión por una entrega, ¿qué te ayuda más?', 3, 1),
(118, 3, '¿Qué te da más satisfacción al terminar un día?', 4, 1),
(119, 3, 'Si te dieran total libertad para hacer un proyecto, ¿cómo lo harías?', 5, 1),
(120, 3, 'Una discusión se pone tensa en el grupo. ¿Qué haces?', 6, 1),
(121, 3, '¿Qué ambiente de estudio te hace sentir en tu elemento?', 7, 1),
(122, 4, 'Imagina tu vida dentro de diez años. ¿Qué escena te emociona más?', 1, 1),
(123, 4, '¿En qué lugar de trabajo te imaginas?', 2, 1),
(124, 4, 'Te ofrecen una beca de un año. ¿Para qué la usarías?', 3, 1),
(125, 4, '¿Qué problema del mundo te gustaría ayudar a resolver?', 4, 1),
(126, 4, 'Mañana empiezas un trabajo nuevo. ¿Cuál aceptarías con más ganas?', 5, 1),
(127, 4, '¿Qué te gustaría que dijeran de tu trabajo en el futuro?', 6, 1),
(128, 4, 'Para tu último gran proyecto escolar, ¿qué tema te animaría más?', 7, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programas`
--

CREATE TABLE `programas` (
  `id_programa` int(11) NOT NULL,
  `id_institucion` int(11) NOT NULL,
  `nombre` varchar(200) NOT NULL,
  `tipo` enum('universitario','tecnico','tecnologico','curso') NOT NULL,
  `descripcion` text DEFAULT NULL,
  `duracion` varchar(100) DEFAULT NULL,
  `sitio_web` varchar(255) DEFAULT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `programa_carrera`
--

CREATE TABLE `programa_carrera` (
  `id_programa` int(11) NOT NULL,
  `id_carrera` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `progreso`
--

CREATE TABLE `progreso` (
  `id_progreso` int(11) NOT NULL,
  `id_estudiante` int(11) NOT NULL,
  `puntos` int(11) NOT NULL DEFAULT 0,
  `nivel_actual` int(11) NOT NULL DEFAULT 1,
  `porcentaje` decimal(5,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pruebas`
--

CREATE TABLE `pruebas` (
  `id_prueba` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `numero_nivel` int(11) NOT NULL,
  `estado` tinyint(1) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pruebas`
--

INSERT INTO `pruebas` (`id_prueba`, `nombre`, `descripcion`, `numero_nivel`, `estado`) VALUES
(1, 'Nivel 1 - Explora', 'Descubre tus intereses, habilidades y actividades favoritas.', 1, 1),
(2, 'Nivel 2 - Descubre', 'Descubre tus habilidades, fortalezas y la forma en que te gusta resolver diferentes situaciones.', 2, 1),
(3, 'Nivel 3 - Conócete', 'Descubre tu personalidad, tu forma de trabajar y cómo te relacionas con diferentes situaciones.', 3, 1),
(4, 'Nivel 4 - Proyéctate', 'Explora tus preferencias profesionales y descubre qué tipo de actividades y entornos podrían motivarte en el futuro.', 4, 1),
(5, 'Nivel 5 - Decide', 'Relaciona tus intereses, habilidades y preferencias con posibles áreas de estudio y caminos profesionales.', 5, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `respuestas_usuario`
--

CREATE TABLE `respuestas_usuario` (
  `id_respuesta` int(11) NOT NULL,
  `id_intento` int(11) NOT NULL,
  `id_pregunta` int(11) NOT NULL,
  `id_opcion` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultados`
--

CREATE TABLE `resultados` (
  `id_resultado` int(11) NOT NULL,
  `id_intento` int(11) NOT NULL,
  `id_area_principal` int(11) NOT NULL,
  `fecha_resultado` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultado_area`
--

CREATE TABLE `resultado_area` (
  `id_resultado_area` int(11) NOT NULL,
  `id_resultado` int(11) NOT NULL,
  `id_area` int(11) NOT NULL,
  `puntuacion` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(150) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rol` enum('estudiante','administrador') NOT NULL DEFAULT 'estudiante',
  `estado` tinyint(1) NOT NULL DEFAULT 1,
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--


--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD PRIMARY KEY (`id_administrador`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `areas`
--
ALTER TABLE `areas`
  ADD PRIMARY KEY (`id_area`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `carreras`
--
ALTER TABLE `carreras`
  ADD PRIMARY KEY (`id_carrera`);

--
-- Indices de la tabla `carrera_area`
--
ALTER TABLE `carrera_area`
  ADD PRIMARY KEY (`id_carrera`,`id_area`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD PRIMARY KEY (`id_estudiante`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `estudiante_logro`
--
ALTER TABLE `estudiante_logro`
  ADD PRIMARY KEY (`id_estudiante`,`id_logro`),
  ADD KEY `id_logro` (`id_logro`);

--
-- Indices de la tabla `instituciones`
--
ALTER TABLE `instituciones`
  ADD PRIMARY KEY (`id_institucion`);

--
-- Indices de la tabla `intentos_prueba`
--
ALTER TABLE `intentos_prueba`
  ADD PRIMARY KEY (`id_intento`),
  ADD KEY `id_estudiante` (`id_estudiante`),
  ADD KEY `id_prueba` (`id_prueba`);

--
-- Indices de la tabla `logros`
--
ALTER TABLE `logros`
  ADD PRIMARY KEY (`id_logro`);

--
-- Indices de la tabla `opciones_respuesta`
--
ALTER TABLE `opciones_respuesta`
  ADD PRIMARY KEY (`id_opcion`),
  ADD KEY `id_pregunta` (`id_pregunta`);

--
-- Indices de la tabla `opcion_area`
--
ALTER TABLE `opcion_area`
  ADD PRIMARY KEY (`id_opcion_area`),
  ADD KEY `id_opcion` (`id_opcion`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD PRIMARY KEY (`id_pregunta`),
  ADD KEY `id_prueba` (`id_prueba`);

--
-- Indices de la tabla `programas`
--
ALTER TABLE `programas`
  ADD PRIMARY KEY (`id_programa`),
  ADD KEY `id_institucion` (`id_institucion`);

--
-- Indices de la tabla `programa_carrera`
--
ALTER TABLE `programa_carrera`
  ADD PRIMARY KEY (`id_programa`,`id_carrera`),
  ADD KEY `id_carrera` (`id_carrera`);

--
-- Indices de la tabla `progreso`
--
ALTER TABLE `progreso`
  ADD PRIMARY KEY (`id_progreso`),
  ADD UNIQUE KEY `id_estudiante` (`id_estudiante`);

--
-- Indices de la tabla `pruebas`
--
ALTER TABLE `pruebas`
  ADD PRIMARY KEY (`id_prueba`);

--
-- Indices de la tabla `respuestas_usuario`
--
ALTER TABLE `respuestas_usuario`
  ADD PRIMARY KEY (`id_respuesta`),
  ADD KEY `id_intento` (`id_intento`),
  ADD KEY `id_pregunta` (`id_pregunta`),
  ADD KEY `id_opcion` (`id_opcion`);

--
-- Indices de la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD PRIMARY KEY (`id_resultado`),
  ADD UNIQUE KEY `id_intento` (`id_intento`),
  ADD KEY `id_area_principal` (`id_area_principal`);

--
-- Indices de la tabla `resultado_area`
--
ALTER TABLE `resultado_area`
  ADD PRIMARY KEY (`id_resultado_area`),
  ADD KEY `id_resultado` (`id_resultado`),
  ADD KEY `id_area` (`id_area`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `administradores`
--
ALTER TABLE `administradores`
  MODIFY `id_administrador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `areas`
--
ALTER TABLE `areas`
  MODIFY `id_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `carreras`
--
ALTER TABLE `carreras`
  MODIFY `id_carrera` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  MODIFY `id_estudiante` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `instituciones`
--
ALTER TABLE `instituciones`
  MODIFY `id_institucion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `intentos_prueba`
--
ALTER TABLE `intentos_prueba`
  MODIFY `id_intento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `logros`
--
ALTER TABLE `logros`
  MODIFY `id_logro` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `opciones_respuesta`
--
ALTER TABLE `opciones_respuesta`
  MODIFY `id_opcion` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1113;

--
-- AUTO_INCREMENT de la tabla `opcion_area`
--
ALTER TABLE `opcion_area`
  MODIFY `id_opcion_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=516;

--
-- AUTO_INCREMENT de la tabla `preguntas`
--
ALTER TABLE `preguntas`
  MODIFY `id_pregunta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=129;

--
-- AUTO_INCREMENT de la tabla `programas`
--
ALTER TABLE `programas`
  MODIFY `id_programa` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `progreso`
--
ALTER TABLE `progreso`
  MODIFY `id_progreso` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `pruebas`
--
ALTER TABLE `pruebas`
  MODIFY `id_prueba` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `respuestas_usuario`
--
ALTER TABLE `respuestas_usuario`
  MODIFY `id_respuesta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=93;

--
-- AUTO_INCREMENT de la tabla `resultados`
--
ALTER TABLE `resultados`
  MODIFY `id_resultado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `resultado_area`
--
ALTER TABLE `resultado_area`
  MODIFY `id_resultado_area` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `administradores`
--
ALTER TABLE `administradores`
  ADD CONSTRAINT `administradores_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `carrera_area`
--
ALTER TABLE `carrera_area`
  ADD CONSTRAINT `carrera_area_ibfk_1` FOREIGN KEY (`id_carrera`) REFERENCES `carreras` (`id_carrera`) ON DELETE CASCADE,
  ADD CONSTRAINT `carrera_area_ibfk_2` FOREIGN KEY (`id_area`) REFERENCES `areas` (`id_area`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiantes`
--
ALTER TABLE `estudiantes`
  ADD CONSTRAINT `estudiantes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `estudiante_logro`
--
ALTER TABLE `estudiante_logro`
  ADD CONSTRAINT `estudiante_logro_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`) ON DELETE CASCADE,
  ADD CONSTRAINT `estudiante_logro_ibfk_2` FOREIGN KEY (`id_logro`) REFERENCES `logros` (`id_logro`) ON DELETE CASCADE;

--
-- Filtros para la tabla `intentos_prueba`
--
ALTER TABLE `intentos_prueba`
  ADD CONSTRAINT `intentos_prueba_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`) ON DELETE CASCADE,
  ADD CONSTRAINT `intentos_prueba_ibfk_2` FOREIGN KEY (`id_prueba`) REFERENCES `pruebas` (`id_prueba`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opciones_respuesta`
--
ALTER TABLE `opciones_respuesta`
  ADD CONSTRAINT `opciones_respuesta_ibfk_1` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE;

--
-- Filtros para la tabla `opcion_area`
--
ALTER TABLE `opcion_area`
  ADD CONSTRAINT `opcion_area_ibfk_1` FOREIGN KEY (`id_opcion`) REFERENCES `opciones_respuesta` (`id_opcion`) ON DELETE CASCADE,
  ADD CONSTRAINT `opcion_area_ibfk_2` FOREIGN KEY (`id_area`) REFERENCES `areas` (`id_area`) ON DELETE CASCADE;

--
-- Filtros para la tabla `preguntas`
--
ALTER TABLE `preguntas`
  ADD CONSTRAINT `preguntas_ibfk_1` FOREIGN KEY (`id_prueba`) REFERENCES `pruebas` (`id_prueba`) ON DELETE CASCADE;

--
-- Filtros para la tabla `programas`
--
ALTER TABLE `programas`
  ADD CONSTRAINT `programas_ibfk_1` FOREIGN KEY (`id_institucion`) REFERENCES `instituciones` (`id_institucion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `programa_carrera`
--
ALTER TABLE `programa_carrera`
  ADD CONSTRAINT `programa_carrera_ibfk_1` FOREIGN KEY (`id_programa`) REFERENCES `programas` (`id_programa`) ON DELETE CASCADE,
  ADD CONSTRAINT `programa_carrera_ibfk_2` FOREIGN KEY (`id_carrera`) REFERENCES `carreras` (`id_carrera`) ON DELETE CASCADE;

--
-- Filtros para la tabla `progreso`
--
ALTER TABLE `progreso`
  ADD CONSTRAINT `progreso_ibfk_1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`) ON DELETE CASCADE;

--
-- Filtros para la tabla `respuestas_usuario`
--
ALTER TABLE `respuestas_usuario`
  ADD CONSTRAINT `respuestas_usuario_ibfk_1` FOREIGN KEY (`id_intento`) REFERENCES `intentos_prueba` (`id_intento`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_usuario_ibfk_2` FOREIGN KEY (`id_pregunta`) REFERENCES `preguntas` (`id_pregunta`) ON DELETE CASCADE,
  ADD CONSTRAINT `respuestas_usuario_ibfk_3` FOREIGN KEY (`id_opcion`) REFERENCES `opciones_respuesta` (`id_opcion`) ON DELETE CASCADE;

--
-- Filtros para la tabla `resultados`
--
ALTER TABLE `resultados`
  ADD CONSTRAINT `resultados_ibfk_1` FOREIGN KEY (`id_intento`) REFERENCES `intentos_prueba` (`id_intento`) ON DELETE CASCADE,
  ADD CONSTRAINT `resultados_ibfk_2` FOREIGN KEY (`id_area_principal`) REFERENCES `areas` (`id_area`);

--
-- Filtros para la tabla `resultado_area`
--
ALTER TABLE `resultado_area`
  ADD CONSTRAINT `resultado_area_ibfk_1` FOREIGN KEY (`id_resultado`) REFERENCES `resultados` (`id_resultado`) ON DELETE CASCADE,
  ADD CONSTRAINT `resultado_area_ibfk_2` FOREIGN KEY (`id_area`) REFERENCES `areas` (`id_area`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
