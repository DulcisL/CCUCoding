<?php
	// allows me to see all the errors so they can be fixed
	// will be turned off in a prouction environment
	error_reporting(E_ALL);
	ini_set('display_errors', "1");
	
	$currentFile = basename($_SERVER['SCRIPT_FILENAME']);
	$needsMapAssets = ($currentFile === 'parking.php');
?>
<!DOCTYPE html>
<html lang="en-us">
	<head>
		<meta charset="utf-8">
		<meta name="author" content="Lucas Wedge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title><?php echo ucfirst($currentFile), PHP_EOL; ?></title>
		<?php if ($needsMapAssets): ?>
		<link
			rel="stylesheet"
			href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
			crossorigin=""
		>
		<style>
			#map {
				height: 70vh;
				min-height: 420px;
				width: 100%;
				border-radius: 12px;
				box-shadow: 0 2px 14px rgba(0, 0, 0, 0.12);
				overflow: hidden;
			}
			.parking-map-wrapper {
				position: relative;
				margin-block: 1.5rem;
			}
			.parking-map-note {
				margin-top: 0.5rem;
				font-size: 0.95rem;
				color: #444;
			}
		</style>
		<?php endif; ?>
	</head>
	<body>
		<header>
			<h1>CCU Commuting</h1>
			<nav>
				<?php 
			echo ($currentFile == "parking.php") ? "Parking" : '<a href="parking.php">Parking</a>';
			echo ($currentFile == "stats.php") ? "Stats" : '<a href="stats.php">Stats</a>';
		?>
			</nav>
		</header>
