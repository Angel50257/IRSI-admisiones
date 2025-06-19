-- Crear la base de datos
CREATE DATABASE Admisiones;
GO

USE Admisiones;
GO

-- Tabla: Usuarios
CREATE TABLE usuarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_usuario NVARCHAR(50) UNIQUE NOT NULL,
    contrasena_hash NVARCHAR(255) NOT NULL,
    rol NVARCHAR(20) CHECK (rol IN ('ADMINISTRADOR', 'ASISTENTE', 'DIRECTOR', 'CONSULTA')) NOT NULL,
    fecha_creacion DATETIME DEFAULT GETDATE()
);
GO

-- Tabla: Aplicantes
CREATE TABLE aplicantes (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_completo NVARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    documento NVARCHAR(50) UNIQUE NOT NULL,
    pais NVARCHAR(50) NOT NULL,
    universidad NVARCHAR(100),
    carrera NVARCHAR(100),
	ultimo_grado_academico NVARCHAR(100),
    estado NVARCHAR(20) CHECK (estado IN ('Aceptado', 'Rechazado', 'Retirado', 'En curso')) DEFAULT 'En curso',
    email NVARCHAR(100),
    telefono NVARCHAR(20),
    anio_aplicacion INT NOT NULL,
    observaciones NVARCHAR(MAX),
    fecha_registro DATETIME DEFAULT GETDATE()
);
GO

-- Tabla: Historial
CREATE TABLE historial (
    id INT IDENTITY(1,1) PRIMARY KEY,
    aplicante_id INT NOT NULL,
    fecha_evento DATETIME NOT NULL,
    motivo NVARCHAR(255) NOT NULL,
    duracion_meses INT,
    observaciones NVARCHAR(MAX),
    FOREIGN KEY (aplicante_id) REFERENCES aplicantes(id)
);
GO

-- Tabla: Eventos del sistema (auditoría)
CREATE TABLE historial_eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento NVARCHAR(100),
    aplicante_id INT,
    fecha DATETIME DEFAULT GETDATE()
);
GO

DROP PROCEDURE IF EXISTS InsertarAplicante;
GO

-- Insertar un aplicante con validación de documento único
CREATE PROCEDURE InsertarAplicante
    @NombreCompleto NVARCHAR(100),
    @FechaNacimiento DATE,
    @Documento NVARCHAR(50),
    @Pais NVARCHAR(50),
    @Universidad NVARCHAR(100),
    @Carrera NVARCHAR(100),
	@UltimoGradoAcademico NVARCHAR(100), 
    @Estado NVARCHAR(20),
    @Email NVARCHAR(100),
    @Telefono NVARCHAR(20),
    @AnioAplicacion INT,
    @Observaciones NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (SELECT 1 FROM aplicantes WHERE documento = @Documento)
    BEGIN
        RAISERROR ('Ya existe un aplicante con este documento.', 16, 1);
        RETURN;
    END

    INSERT INTO aplicantes (
        nombre_completo, fecha_nacimiento, documento, pais, universidad, carrera, 
		ultimo_grado_academico, estado, email, telefono, anio_aplicacion, observaciones
    ) VALUES (
        @NombreCompleto, @FechaNacimiento, @Documento, @Pais, @Universidad, @Carrera,
        @UltimoGradoAcademico, @Estado, @Email, @Telefono, @AnioAplicacion, @Observaciones
    );
END;
GO

-- Agregar evento al historial de un aplicante
CREATE PROCEDURE RegistrarHistorial
    @AplicanteId INT,
    @FechaEvento DATETIME,
    @Motivo NVARCHAR(255),
    @DuracionMeses INT,
    @Observaciones NVARCHAR(MAX)
AS
BEGIN
    SET NOCOUNT ON;

    IF NOT EXISTS (SELECT 1 FROM aplicantes WHERE id = @AplicanteId)
    BEGIN
        RAISERROR ('Aplicante no encontrado.', 16, 1);
        RETURN;
    END

    INSERT INTO historial (
        aplicante_id, fecha_evento, motivo, duracion_meses, observaciones
    ) VALUES (
        @AplicanteId, @FechaEvento, @Motivo, @DuracionMeses, @Observaciones
    );
END;
GO


-- Auditoría al eliminar un aplicante
CREATE TRIGGER trg_Aplicante_Eliminado
ON aplicantes
AFTER DELETE
AS
BEGIN
    INSERT INTO historial_eventos (evento, aplicante_id, fecha)
    SELECT 'Aplicante eliminado', id, GETDATE()
    FROM deleted;
END;
GO

SELECT * FROM USUARIOS
SELECT * FROM APLICANTES
SELECT * FROM HISTORIAL
SELECT * FROM HISTORIAL_EVENTOS


