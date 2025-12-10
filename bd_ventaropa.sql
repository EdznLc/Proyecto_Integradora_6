-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 10-12-2025 a las 03:31:09
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
  `id_cliente` smallint(3) UNSIGNED NOT NULL,
  `id_usuario_registro` smallint(2) UNSIGNED NOT NULL,
  `nombre` tinytext NOT NULL,
  `apellido_paterno` tinytext NOT NULL,
  `apellido_materno` tinytext DEFAULT NULL,
  `telefono` char(10) DEFAULT NULL,
  `direccion` tinytext DEFAULT NULL,
  `correo` varchar(50) DEFAULT NULL,
  `edad` tinyint(2) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `id_usuario_registro`, `nombre`, `apellido_paterno`, `apellido_materno`, `telefono`, `direccion`, `correo`, `edad`) VALUES
(1, 3, 'Lety', 'Estrada', 'Alvarado', '6183657892', 'Calle Encino #245, Col. Valle del Guadiana, Durango, Dgo.', 'lety_estrada@gmail.com', 52),
(2, 3, 'Nancy', 'Rios', 'Delgado', '6183622244', 'Privada Nogal #112, Col. Ampliación PRI, Durango, Dgo.', 'riosnancy420@gmail.com', 43),
(3, 3, 'Guadalupe', 'Hernandez', 'Garcia', '6187273415', 'Avenida Constitución #1875, Col. Santa María, Durango, Dgo.', 'lupislupis@gmail.com', 62),
(6, 3, 'Alicia', 'Perez', 'Cruz', '6186641812', 'Calle Río Coatzacoalcos #58, Fracc. Río Dorado, Durango, Dgo.', 'alicia_maravilla@gmail.com', 38),
(7, 3, 'Coco', 'Aguilar', 'Castillo', '6182774911', 'Calle 5 de Febrero #321, Col. Madero, Durango, Dgo.', 'cocoaguilar11@hotmail.com', 46),
(8, 3, 'Nancy', 'Morales', 'Rivera', '6181234665', 'Boulevard Durango #1402, Col. Esperanza, Durango, Dgo.', 'nancymr@gmail.com', 47),
(9, 3, 'Maria Angeles', 'Dominguez', 'Medina', '6183352456', 'Calle Fresno #67, Col. Nuevo Durango, Durango, Dgo.', 'maangeles65@gmail.com', 53),
(10, 4, 'Paty', 'Lomas', 'Hernandez', '6181170606', 'Avenida Magallanes #903, Col. Las Alamedas, Durango, Dgo.', 'nana11@gmail.com', 59),
(11, 4, 'Paola', 'Hernandez', 'Vazquez', '6182987831', 'Calle Abedul #44, Fracc. Real del Prado, Durango, Dgo.', 'paola51hv@gmail.com', 30),
(12, 3, 'Lili', 'Bautista', 'Rojas', '6182672506', 'Calle Ciprés #780, Col. El Refugio, Durango, Dgo.', 'lililili345@gmail.com', 45),
(13, 3, 'Janeth', 'Carrillo', 'Solis', '6182168573', 'Calle Ópalo #129, Fracc. Joyas del Valle, Durango, Dgo.', 'betsi677@hotmail.com', 36),
(14, 4, 'Luisa', 'Camacho', 'Ibarra', '6183309547', 'Calle Cedro Rojo #311, Col. San Ignacio, Durango, Dgo.', 'ciluisa90@gmail.com', 38),
(15, 3, 'Nahive', 'Hernandez', 'Martinez', '6183330729', 'Privada Azucena #54, Fracc. Florencia, Durango, Dgo.', 'martmarmon@gmail.com', 30),
(16, 4, 'Fany', 'Gonzalez', 'Diaz', '6183245391', 'Avenida Hidalgo #2048, Col. Centro, Durango, Dgo.', 'fgdanyyzz@gmail.com', 26),
(17, 3, 'Rosa', 'Jimenez', 'Flores', '6181091869', 'Calle Galeana #77, Col. El Calvario, Durango, Dgo.', 'rosyfloji12@gmail.com', 41),
(18, 3, 'Maritza', 'Diaz', 'Alvarado', '6183089191', 'Privada Roble Blanco #19, Fracc. Los Encinos, Durango, Dgo.', 'Martiza2634@gmail.com', 35),
(19, 3, 'Marissa', 'Montes', 'Galvan', '6182126201', 'Calle Sierra Madre #880, Col. Domingo Arrieta, Durango, Dgo.', 'marigal45@hotmail.com', 51),
(20, 3, 'Claudia', 'Lopez', 'Barraza', '6181600290', 'Boulevard Guadiana #1021, Col. Las Brisas, Durango, Dgo.', 'claulopezb78@gmail.com', 62),
(21, 3, 'Mayra', 'Guerra', 'Saucedo', '6182802326', 'Calle Tulipanes #36, Fracc. Jardines del Real, Durango, Dgo.', 'saucedomg363@gmail.com', 47);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` smallint(2) UNSIGNED NOT NULL,
  `username` tinytext NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` char(64) NOT NULL,
  `es_admin` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `username`, `correo`, `password`, `es_admin`) VALUES
(1, 'Admin', 'admin@sistema.com', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 1),
(2, 'Edson', 'edson@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 1),
(3, 'Mireya', 'ayerim_1981@gmail.com', 'a5c3ca0c0ee32e8bfab8b69f06d55990545b82c52ca553389000cfb5186c5a4c', 1),
(4, 'Naila', 'naila2009@gmail.com', 'bda50c44c700c94bf75f3fb911f3d664e6ad891590c0defbfed10d8e12ab4a61', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` smallint(4) UNSIGNED NOT NULL,
  `id_usuario` smallint(2) UNSIGNED NOT NULL,
  `id_cliente` smallint(3) UNSIGNED NOT NULL,
  `metodo_pago` tinyint(1) UNSIGNED NOT NULL,
  `monto` decimal(6,2) NOT NULL,
  `num_prendas` tinyint(2) UNSIGNED NOT NULL,
  `fecha` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `id_usuario`, `id_cliente`, `metodo_pago`, `monto`, `num_prendas`, `fecha`) VALUES
(1, 2, 1, 2, 120.01, 2, '2025-11-25 20:51:41'),
(3, 1, 3, 3, 305.00, 6, '2025-11-25 21:29:13'),
(6, 3, 18, 3, 415.00, 5, '2024-12-14 17:33:05'),
(7, 4, 10, 1, 695.00, 8, '2024-12-15 18:48:17'),
(8, 3, 19, 2, 120.00, 1, '2024-12-16 19:13:29'),
(9, 4, 11, 3, 445.00, 5, '2024-12-17 20:39:41'),
(10, 3, 20, 1, 775.00, 9, '2024-12-18 17:04:53'),
(11, 4, 14, 2, 200.00, 2, '2024-12-19 18:19:05'),
(12, 3, 13, 3, 535.00, 6, '2024-12-20 19:45:17'),
(13, 4, 16, 1, 855.00, 11, '2024-12-21 20:10:29'),
(14, 3, 1, 2, 360.00, 4, '2024-12-22 17:36:42'),
(15, 4, 10, 3, 635.00, 8, '2024-12-23 18:51:54'),
(16, 3, 2, 1, 145.00, 2, '2024-12-24 19:27:06'),
(17, 4, 11, 2, 475.00, 5, '2024-12-25 20:53:18'),
(18, 3, 3, 3, 725.00, 9, '2024-12-26 17:18:30'),
(19, 4, 14, 1, 295.00, 3, '2024-12-27 18:43:42'),
(20, 3, 6, 2, 585.00, 7, '2024-12-28 19:08:54'),
(21, 4, 16, 3, 815.00, 10, '2024-12-29 20:34:06'),
(22, 3, 7, 1, 170.00, 2, '2024-12-30 17:59:19'),
(23, 4, 10, 2, 400.00, 4, '2024-12-31 18:24:31'),
(24, 3, 8, 3, 755.00, 9, '2025-01-01 19:50:43'),
(25, 4, 11, 1, 225.00, 3, '2025-01-02 20:15:55'),
(26, 3, 9, 2, 555.00, 6, '2025-01-03 17:41:08'),
(27, 4, 14, 3, 885.00, 11, '2025-01-04 18:56:20'),
(28, 3, 12, 1, 395.00, 4, '2025-01-05 19:21:32'),
(29, 4, 16, 2, 665.00, 8, '2025-01-06 20:47:44'),
(30, 3, 18, 3, 115.00, 1, '2025-01-07 17:12:56'),
(31, 4, 10, 1, 435.00, 5, '2025-01-08 18:38:09'),
(32, 3, 19, 2, 785.00, 10, '2025-01-09 19:03:21'),
(33, 4, 11, 3, 270.00, 3, '2025-01-10 20:29:33'),
(34, 3, 20, 1, 600.00, 7, '2025-01-11 17:54:46'),
(35, 4, 14, 2, 150.00, 2, '2025-01-12 18:19:58'),
(36, 3, 13, 3, 480.00, 5, '2025-01-13 19:46:10'),
(37, 4, 16, 1, 730.00, 9, '2025-01-14 20:11:22'),
(38, 3, 1, 2, 240.00, 3, '2025-01-15 17:37:34'),
(39, 4, 10, 3, 560.00, 6, '2025-01-16 18:02:46'),
(40, 3, 2, 1, 890.00, 12, '2025-01-17 19:28:59'),
(41, 4, 11, 2, 330.00, 4, '2025-01-18 20:55:11'),
(42, 3, 3, 3, 670.00, 8, '2025-01-19 17:20:23'),
(43, 4, 14, 1, 100.00, 1, '2025-01-20 18:45:35'),
(44, 3, 6, 2, 420.00, 5, '2025-01-21 19:10:47'),
(45, 4, 16, 3, 750.00, 9, '2025-01-22 20:36:59'),
(46, 3, 7, 1, 265.00, 3, '2025-01-23 17:02:12'),
(47, 4, 10, 2, 595.00, 7, '2025-01-24 18:27:24'),
(48, 3, 8, 3, 880.00, 11, '2025-01-25 19:53:36'),
(49, 4, 11, 1, 305.00, 4, '2025-01-26 20:18:48'),
(50, 3, 9, 2, 625.00, 8, '2025-01-27 17:44:01'),
(51, 4, 14, 3, 155.00, 2, '2025-01-28 18:09:13'),
(52, 3, 12, 1, 475.00, 5, '2025-01-29 19:35:25'),
(53, 4, 16, 2, 705.00, 9, '2025-01-30 20:00:37'),
(54, 3, 18, 3, 235.00, 3, '2025-01-31 17:26:49'),
(55, 4, 10, 1, 565.00, 7, '2025-02-01 18:51:01'),
(56, 3, 19, 2, 815.00, 10, '2025-02-02 19:16:13'),
(57, 4, 11, 3, 345.00, 4, '2025-02-03 20:42:25'),
(58, 3, 20, 1, 695.00, 8, '2025-02-04 17:07:38'),
(59, 4, 14, 2, 125.00, 1, '2025-02-05 18:32:50'),
(60, 3, 13, 3, 455.00, 5, '2025-02-06 19:58:02'),
(61, 4, 16, 1, 785.00, 10, '2025-02-07 20:23:14'),
(62, 3, 1, 2, 205.00, 2, '2025-02-08 17:49:26'),
(63, 4, 10, 3, 535.00, 6, '2025-02-09 18:14:38'),
(64, 3, 2, 1, 865.00, 11, '2025-02-10 19:40:51'),
(65, 4, 11, 2, 395.00, 4, '2025-02-11 20:06:03'),
(66, 3, 3, 3, 625.00, 8, '2025-02-12 17:31:15'),
(67, 4, 14, 1, 140.00, 1, '2025-02-13 18:56:27'),
(68, 3, 6, 2, 470.00, 5, '2025-02-14 19:21:39'),
(69, 4, 16, 3, 720.00, 9, '2025-02-15 20:47:51'),
(70, 3, 7, 1, 250.00, 3, '2025-02-16 17:13:04'),
(71, 4, 10, 2, 580.00, 7, '2025-02-17 18:38:16'),
(72, 3, 8, 3, 830.00, 10, '2025-02-18 20:04:28'),
(73, 4, 11, 1, 350.00, 4, '2025-02-19 20:29:40'),
(74, 3, 9, 2, 680.00, 8, '2025-02-20 17:54:53'),
(75, 4, 14, 3, 170.00, 2, '2025-02-21 18:19:05'),
(76, 3, 12, 1, 500.00, 6, '2025-02-22 19:45:17'),
(77, 4, 16, 2, 850.00, 11, '2025-02-23 20:10:29'),
(78, 3, 18, 3, 300.00, 4, '2025-02-24 17:36:42'),
(79, 4, 10, 1, 630.00, 8, '2025-02-25 18:51:54'),
(80, 3, 19, 2, 120.00, 1, '2025-02-26 19:27:06'),
(81, 4, 11, 3, 450.00, 5, '2025-02-27 20:53:18'),
(82, 3, 20, 1, 780.00, 9, '2025-02-28 17:18:30'),
(83, 4, 14, 2, 210.00, 2, '2025-03-01 18:43:42'),
(84, 3, 13, 3, 540.00, 6, '2025-03-02 19:08:54'),
(85, 4, 16, 1, 870.00, 12, '2025-03-03 20:34:06'),
(86, 3, 1, 2, 390.00, 4, '2025-03-04 17:59:19'),
(87, 4, 10, 3, 620.00, 8, '2025-03-05 18:24:31'),
(88, 3, 2, 1, 110.00, 1, '2025-03-06 19:50:43'),
(89, 4, 11, 2, 440.00, 5, '2025-03-07 20:15:55'),
(90, 3, 3, 3, 770.00, 9, '2025-03-08 17:41:08'),
(91, 4, 14, 1, 200.00, 2, '2025-03-09 18:56:20'),
(92, 3, 6, 2, 530.00, 6, '2025-03-10 19:21:32'),
(93, 4, 16, 3, 860.00, 11, '2025-03-11 20:47:44'),
(94, 3, 7, 1, 370.00, 4, '2025-03-12 17:12:56');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_usuario_registro` (`id_usuario_registro`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD UNIQUE KEY `username` (`username`) USING HASH;

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` smallint(3) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` smallint(2) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` smallint(4) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=95;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario_registro`) REFERENCES `usuarios` (`id_usuario`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
