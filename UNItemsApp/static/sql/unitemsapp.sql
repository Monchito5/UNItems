-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 02-12-2022 a las 20:36:10
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
-- Base de datos: `unitemsapp`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `comments`
--

CREATE TABLE `comments` (
  `idc` int(11) NOT NULL,
  `idu` int(11) NOT NULL,
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
  `password` char(102) COLLATE utf8_spanish_ci NOT NULL,
  `auth` char(1) COLLATE utf8_spanish_ci NOT NULL DEFAULT 'U',
  `imgprofile` varchar(5000) COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `user`
--

INSERT INTO `user` (`id`, `username`, `email`, `password`, `auth`, `imgprofile`) VALUES
(1, 'MrSylar', 'secrethawkwood@gmail.com', 'pbkdf2:sha256:260000$sXwGyQPplVuepnLG$c1f35e7dcf4a7777adfd74928e045372da28c5ceece9353eeb115fdf787fd05a', 'A', 'jinx.jpg'),
(2, 'Gerardo', 'numbersixapplication@gmail.com', 'pbkdf2:sha256:260000$sy7Fho1Dff7b2RdR$f560cb0114dd9113b1053c58044de6170150868c3c62fed134f5f816bf3dda55', 'A', '2022130647ghost.png'),
(3, 'Monchonetreitor', 'guille2807lol@gmail.com', 'pbkdf2:sha256:260000$uQxJi1eyxmzhBVUk$a9e70f0aa4dd2e8fbbb094fdbc517d315e370805e84e1ce8f0202fb0598955d2', 'A', '2022133352ESCORPION INOSUKE.jpg'),
(4, 'RouSan', 'reyna.rosy.26.09@gmail.com', 'pbkdf2:sha256:260000$wWFlaDWD0dDWxUFp$1935a6d527f6ecf670ed884775c705348ab8a4a742e905e4f24a7ee73e669b71', 'U', '2022133424bonito azul.jpg');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`idc`),
  ADD KEY `idu` (`idu`);

--
-- Indices de la tabla `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `comments`
--
ALTER TABLE `comments`
  MODIFY `idc` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`idu`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
