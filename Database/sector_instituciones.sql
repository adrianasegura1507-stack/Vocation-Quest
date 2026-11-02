-- =====================================================
-- VOCATION QUEST: sector de las instituciones (pública o privada)
--
-- Agrega la columna "sector" a la tabla "instituciones":
--   sector -> publica o privada (NULL = sin dato)
--
-- No borra ni cambia nada de lo que ya existe: las instituciones
-- actuales quedan con el sector vacío hasta que lo completes
-- desde el panel de administración.
--
-- IMPORTANTE: ejecutar UNA sola vez.
-- =====================================================

ALTER TABLE instituciones
  ADD COLUMN sector ENUM('publica','privada') NULL AFTER tipo;
