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

-- Tabla: Eventos del sistema (auditor�a)
CREATE TABLE historial_eventos (
    id INT IDENTITY(1,1) PRIMARY KEY,
    evento NVARCHAR(100),
    aplicante_id INT,
    fecha DATETIME DEFAULT GETDATE()
);
GO

DROP PROCEDURE IF EXISTS InsertarAplicante;
GO

-- Insertar un aplicante con validaci�n de documento �nico
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


-- Auditor�a al eliminar un aplicante
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


INSERT INTO aplicantes (nombre_completo, fecha_nacimiento, documento, pais, universidad, carrera, ultimo_grado_academico, estado, email, telefono, anio_aplicacion, observaciones)
VALUES 
('Ana L�pez Morales', '2000-03-15', 'GT-1001', 'Guatemala', 'USAC', 'Ingenier�a Civil', 'Diversificado', 'Aceptado', 'ana.lopez@example.com', '50123456', 2025, 'Aplicaci�n exitosa'),

('Carlos M�ndez R�os', '1999-07-20', 'SV-1002', 'El Salvador', 'UES', 'Derecho', 'Bachillerato General', 'Rechazado', 'carlos.mendez@correo.com', '77451236', 2025, 'No cumpli� requisitos acad�micos'),

('Mar�a Fernanda Aguilar', '2001-01-09', 'HN-1003', 'Honduras', 'UNAH', 'Enfermer�a', 'Bachiller T�cnico', 'Aceptado', 'm.fernanda@correo.hn', '32999887', 2025, 'Gran potencial'),

('Jos� Ram�rez Castillo', '2000-05-22', 'NI-1004', 'Nicaragua', 'UNAN-Managua', 'Arquitectura', 'Secundaria completa', 'Retirado', 'jose.ramirez@nicaragua.com', '88993311', 2023, 'Se retir� por motivos personales'),

('Laura Ch�vez L�pez', '1999-10-05', 'CR-1005', 'Costa Rica', 'UCR', 'Psicolog�a', 'Bachiller en Educaci�n', 'En curso', 'laura.chavez@ucr.cr', '71234567', 2024, 'Buen desempe�o'),

('Andr�s Soto Jim�nez', '2001-04-30', 'PA-1006', 'Panam�', 'Universidad de Panam�', 'Sociolog�a', 'Diversificado', 'Aceptado', 'andres.soto@up.pa', '64412345', 2025, 'Recomendado por catedr�tico'),

('Isabel Herrera', '2000-08-12', 'GT-1007', 'Guatemala', 'UVG', 'Ingenier�a Industrial', 'Diversificado', 'En curso', 'isabel.herrera@uvg.edu.gt', '50112233', 2025, 'Interesada en gesti�n de proyectos'),

('David Morales', '1998-11-01', 'HN-1008', 'Honduras', 'UNAH', 'Administraci�n', 'Perito Mercantil', 'Rechazado', 'd.morales@unah.hn', '33445566', 2025, 'Documentos incompletos'),

('Marcela G�mez', '2002-02-18', 'SV-1009', 'El Salvador', 'UCA', 'Econom�a', 'Bachillerato General', 'Aceptado', 'marcela.gomez@uca.edu.sv', '77889900', 2025, 'Aplicaci�n destacada'),

('Fernando Rodr�guez', '2000-06-25', 'CR-1010', 'Costa Rica', 'TEC', 'Ingenier�a en Sistemas', 'Bachiller en Ciencias', 'En curso', 'fernando.rodriguez@tec.cr', '71112233', 2025, 'Avanzado en programaci�n'),

('Daniela Lima', '1999-12-19', 'NI-1011', 'Nicaragua', 'UNAN-Le�n', 'Medicina', 'Secundaria', 'Retirado', 'daniela.lima@unan.edu.ni', '88994477', 2022, 'Abandono por salud'),

('Mario Ju�rez', '2000-09-10', 'PA-1012', 'Panam�', 'UDELAS', 'Educaci�n Primaria', 'Diversificado', 'Aceptado', 'mario.juarez@udelas.pa', '60001122', 2025, 'Buen perfil acad�mico'),

('Andrea Figueroa', '2001-03-03', 'GT-1013', 'Guatemala', 'Land�var', 'Comunicaci�n', 'Diversificado', 'En curso', 'a.figueroa@landivar.gt', '50123499', 2025, 'Buen nivel de expresi�n oral'),

('Kevin Torres', '2000-07-07', 'SV-1014', 'El Salvador', 'UES', 'Matem�tica', 'Bachiller T�cnico', 'Aceptado', 'kevin.torres@ues.edu.sv', '77334455', 2025, 'Particip� en olimpiadas'),

('Luc�a Men�ndez', '2001-05-21', 'HN-1015', 'Honduras', 'UNITEC', 'Finanzas', 'Perito Contador', 'Rechazado', 'lucia.menendez@unitec.hn', '33445577', 2025, 'No present� carta de recomendaci�n'),

('Brandon Ruiz', '1999-11-15', 'CR-1016', 'Costa Rica', 'UNED', 'Inform�tica Educativa', 'Bachiller en Educaci�n', 'Aceptado', 'brandon.ruiz@uned.cr', '79993322', 2025, 'Apoya en centros comunitarios'),

('Patricia S�nchez', '2002-01-02', 'NI-1017', 'Nicaragua', 'UNAN-Managua', 'Biolog�a', 'Diversificado', 'En curso', 'patricia.sanchez@bio.edu.ni', '88991100', 2025, 'Apasionada por la ciencia'),

('Luis Herrera', '1998-04-14', 'PA-1018', 'Panam�', 'USMA', 'Contadur�a', 'Perito Contador', 'Retirado', 'luis.herrera@usma.pa', '63332211', 2021, 'Motivos laborales'),

('Camila Reyes', '2000-03-20', 'GT-1019', 'Guatemala', 'USAC', 'Ingenier�a Qu�mica', 'Diversificado', 'Aceptado', 'camila.reyes@usac.gt', '50128900', 2025, 'Excelente promedio acad�mico'),

('Esteban Sol�s', '2001-10-30', 'CR-1020', 'Costa Rica', 'UCR', 'Derecho', 'Bachiller en Ciencias Sociales', 'En curso', 'esteban.solis@ucr.cr', '71234501', 2025, 'Activo en proyectos legales');
