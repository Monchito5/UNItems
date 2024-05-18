-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-05-2024 a las 06:42:50
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `unitems`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `articles`
--

CREATE TABLE `articles` (
  `ida` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `idc` int(11) NOT NULL,
  `title` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `content` text COLLATE utf8_spanish_ci NOT NULL,
  `pdate` date NOT NULL,
  `learningchannel` varchar(20) COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comments`
--

CREATE TABLE `comments` (
  `idc` int(11) NOT NULL,
  `date` date NOT NULL,
  `contents` text COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `email` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `password` char(102) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fullname` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  `age` varchar(5) COLLATE utf8_spanish_ci DEFAULT NULL,
  `schoolgrade` varchar(20) COLLATE utf8_spanish_ci DEFAULT NULL,
  `auth` char(1) COLLATE utf8_spanish_ci DEFAULT 'U',
  `imgprofile` varchar(5000) COLLATE utf8_spanish_ci DEFAULT NULL,
  `user_resume` varchar(120) COLLATE utf8_spanish_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci COMMENT='Tabla de usuario';

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `fullname`, `age`, `schoolgrade`, `auth`, `imgprofile`, `user_resume`) VALUES
(1, 'Monchonetreitor', 'guille2807lol@gmail.com', 'pbkdf2:sha256:260000$BFFHjvkFCqVYnpUD$37275b500b1a32af81d6c47eda631d942c90ca31085d297febc9d70175e2df4d', 'GUILLERMO DANIEL ZARAGOZA CASTRO', '20', 'preparatoria', 'A', '2022133352ESCORPION_INOSUKE.jpg', 'La trakalosa de MTY'),
(2, 'Pancho', 'panchito5@gmail.com', 'pbkdf2:sha256:260000$qylavDl4SkA2cu3n$e9bc8aa4f8d8c583159dd75c18f7059416fdbb08b22f939ee02b22ee133f7c58', 'Francisco Valle', '54', 'primaria', 'U', '2022012044inosuke.jpg', NULL),
(3, 'Eric Aitor García', 'eric007garcia@gmail.com', 'pbkdf2:sha256:260000$bWjYTV1FURrRFpH8$f343f9f1c3074f8423ba903b1e12be4c8f25e94310fbb85b518be6155da2b0d6', 'Eric Fernando García Y Ramos', '37', 'Licenciatura', 'U', '2022012113perfil_tulipanes.jpg', NULL),
(4, 'RouSan', 'sandyros.16.09@gmail.com', 'pbkdf2:sha256:260000$uzmpjPnpnz8wIbyI$2839948e48ee38520465eefa88d0d55b5e3a2db5e9620afbd7166a20bf5e2ced', 'Sandra Yessica Del Rocío Zaragoza Castro', '21', 'Licenciatura', 'U', '2022011855profile5.jpg', NULL),
(5, 'Oscarín Shark', 'learntoapplication@gmail.com', 'pbkdf2:sha256:260000$XRwrijcJMmaIBzmu$0ab98942af421ede92da3b0afa19114ea14453309eb7a0fd5f8d72970348fa51', 'Óscar Maya', '25', 'Ingenieria', 'U', '2022005926learn.png', NULL),
(6, 'Lili', 'betzabeth0921@gmail.com', 'pbkdf2:sha256:260000$J0JH46qGhdAplUWO$8b822afc71cd1ed006ced75af214f4b2372f3f988e3562c86e928a74823a6a9b', 'Liliana Perez', '17', 'Preparatoria', 'A', '2022172410belleza.png', NULL),
(7, 'RousCast', 'reyna.rosy.26.09@gmail.com', 'pbkdf2:sha256:260000$u2c1qey0tajLDa5R$76610a69508575918c5a62b0d5196557b3788defe5860ab2f95d50074c763e78', 'Rocío Castro', '39', 'Licenciatura', 'U', '2022211351profile1.jpg', NULL),
(12, 'Juanito', 'kakowo9231@ociun.com', 'pbkdf2:sha256:260000$iSyU8hUTI55YGrbh$64190f9fb215eff8ffa8f76ab496afd99a6f32f55cc30e77be510e6f4c777a73', 'Juan Perez', '', '', 'U', '', NULL),
(14, 'Danny', 'danny.2807.32@gmail.com', 'pbkdf2:sha256:260000$ZDZupj7rt9k57zS5$6488aa808651c504b10ed7a772e814737eaf710cb4576661a8cd4233e5c35581', 'Daniel Castro', '0', 'Primaria', 'U', 'Dragonn_sea.PNG', '');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`ida`),
  ADD KEY `id` (`id`),
  ADD KEY `idc` (`idc`);

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`idc`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `articles`
--
ALTER TABLE `articles`
  MODIFY `ida` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `comments`
--
ALTER TABLE `comments`
  MODIFY `idc` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `articles`
--
ALTER TABLE `articles`
  ADD CONSTRAINT `articles_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`idc`) REFERENCES `articles` (`idc`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
