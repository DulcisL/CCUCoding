<?php include "commheader.php"; ?>
<main>
	<section class="parking-intro">
		<h2>Parking Status</h2>
		<p>
			Below you can see an interactive map showing the current status of each CCU parking lot.
			Bus routes appear when that information is available.
		</p>
	</section>

	<section class="parking-map-wrapper" aria-label="Interactive parking availability map">
		<div id="map"></div>
		<p class="parking-map-note">
			Lot colors shift from green (available) toward red as they fill. Planned events force a solid red overlay.
		</p>
	</section>

	<section class="parking-selector">
		<h2>Select A Parking Lot</h2>
		<p>
			Use the dropdown menu to explore a specific lot. Need the full campus layout?
			<a href="https://www.coastal.edu/map/" target="_blank" rel="noopener">Open the campus map</a>.
		</p>
		<?php include "dropdown.php"; ?>
	</section>
</main>
<script
	src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
	crossorigin=""
></script>
<script>
	window.ccuParkingApiBase = <?php echo json_encode(getenv('PARKING_API_BASE') ?: 'http://127.0.0.1:3000'); ?>;
</script>
<script>
<?php include __DIR__ . '/../src/parkingStatus.js'; ?>
</script>
<?php include "commfooter.php"; ?>
