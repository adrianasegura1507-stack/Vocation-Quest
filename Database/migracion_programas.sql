-- =====================================================
-- VOCATION QUEST: nuevas columnas para los programas
--
-- Agrega dos datos a la tabla "programas":
--   ciudad     -> sede donde se ofrece (NULL = sin dato)
--   modalidad  -> presencial, distancia, virtual o mixta (NULL = sin dato)
--
-- No borra ni cambia nada de lo que ya existe: los programas
-- actuales quedan con ciudad y modalidad vacías.
--
-- (En el mundo del software, a un script que cambia la estructura
--  de la base de datos de una versión a otra se le llama
--  "migración". El nombre del archivo no afecta nada.)
--
-- IMPORTANTE: ejecutar UNA sola vez. Si lo ejecutas de nuevo,
-- MySQL dirá que las columnas ya existen.
-- =====================================================

ALTER TABLE programas
  ADD COLUMN ciudad VARCHAR(100) NULL AFTER duracion,
  ADD COLUMN modalidad ENUM('presencial','distancia','virtual','mixta') NULL AFTER ciudad;