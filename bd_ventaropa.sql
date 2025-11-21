-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-11-2025 a las 17:05:51
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
-- Base de datos: `bd_ventaropa`
--
CREATE DATABASE IF NOT EXISTS `bd_ventaropa` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `bd_ventaropa`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(60) NOT NULL,
  `telefono` bigint(11) NOT NULL,
  `direccion` mediumtext NOT NULL,
  `correo` varchar(100) NOT NULL,
  `edad` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id`, `id_usuario`, `nombre`, `telefono`, `direccion`, `correo`, `edad`) VALUES
(1, 4, 'Maria Lopez', 5512345678, 'Av. Reforma 105', 'maria@mail.com', 25),
(4, 4, 'Juan Porras', 5587654321, 'Calle 5 de Mayo', 'juan@mail.com', 35),
(5, 5, 'Pedro Sanchez', 5511223344, 'Insurgentes Sur', 'pedro@mail.com', 42),
(6, 4, 'Sofia Ramirez', 5599887766, 'Colonia Centro', 'sofia@mail.com', 22),
(7, 5, 'Jorge Torres', 5544332211, 'Lomas Verdes', 'jorge@mail.com', 35),
(8, 1, 'Gilberto Lomas Hdz', 6181875561, 'Su casa', 'gil@gmail.com', 59);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id` int(11) NOT NULL,
  `nombre` varchar(40) NOT NULL,
  `apellidos` varchar(40) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `rol` varchar(20) DEFAULT 'usuario'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id`, `nombre`, `apellidos`, `correo`, `password`, `rol`) VALUES
(1, 'Luis', 'Admin', 'admin@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'admin'),
(2, 'Ana', 'Gomez', 'ana@gmail.com', '5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5', 'usuario'),
(3, 'Carlos', 'Vendedor', 'carlos@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'usuario'),
(4, 'ERIK', 'BUENO CAO ROMERO', 'erik@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'usuario'),
(5, 'Fernando', 'Sida', 'fer@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'usuario');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `monto` double NOT NULL,
  `num_prendas` int(3) NOT NULL,
  `metodo_pago` varchar(20) NOT NULL,
  `fecha` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id`, `id_usuario`, `id_cliente`, `monto`, `num_prendas`, `metodo_pago`, `fecha`) VALUES
(5, 4, 1, 1500.5, 3, 'Efectivo', '2025-10-15'),
(6, 5, 4, 500, 1, 'Tarjeta', '2025-10-20'),
(7, 1, 5, 2300, 5, 'Transferencia', '2025-10-25'),
(8, 1, 1, 850, 2, 'Efectivo', '2025-11-01'),
(9, 4, 4, 120, 1, 'Efectivo', '2025-11-02'),
(10, 5, 5, 3500, 8, 'Tarjeta', '2025-11-05'),
(11, 4, 1, 450, 1, 'Tarjeta', '2025-11-10'),
(12, 1, 4, 999.9, 2, 'Transferencia', '2025-11-12'),
(13, 5, 5, 150, 1, 'Efectivo', '2025-11-15'),
(14, 4, 1, 2000, 4, 'Tarjeta', '2025-11-18'),
(15, 1, 5, 750.5, 2, 'Efectivo', '2025-11-19'),
(16, 5, 4, 3200, 6, 'Transferencia', '2025-11-20');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `telefono` (`telefono`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `correo` (`correo`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_usuario` (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
