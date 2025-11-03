<?php
// index.php — lightweight front controller + map page

// Optional: pull in your app config if you have one
if (file_exists(__DIR__ . '/config.php')) {
  require_once __DIR__ . '/config.php';
}

// Simple page selection (defaults to "map")
$page = isset($_GET['page']) ? preg_replace('/[^a-z0-9_\-]/i', '', $_GET['page']) : 'map';

// Convenience helper for safe includes
function try_include($path) {
  if (file_exists($path)) { include $path; return true; }
  return false;
}
?><!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta
    name="viewport"
    content="width=device-width, initial-scale=1, viewport-fit=cover"
  />
  <title><?php echo htmlspecialchars(ucfirst($page)); ?></title>

  <!-- Leaflet CSS (required for the interactive map) -->
  <link
    rel="stylesheet"
    href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
    crossorigin=""
  />

  <!-- Any site-wide CSS you already have -->
  <?php try_include(__DIR__ . '/components/head-styles.php'); ?>
  <?php try_include(__DIR__ . '/components/head-scripts.php'); ?>

  <style>
    /* Keep the map visible without touching your existing CSS */
    #map { height: 70vh; min-height: 420px; width: 100%; }
    .legend {
      background: #fff; padding: 8px 10px; border-radius: 8px;
      box-shadow: 0 1px 4px rgba(0,0,0,0.2); font: 14px/1.2 system-ui, sans-serif;
    }
  </style>
</head>
<body>
  <?php
    // Optional shared header / nav you might already have
    try_include(__DIR__ . '/components/header.php');
    try_include(__DIR__ . '/components/navbar.php');
  ?>

  <main>
    <?php if ($page === 'map'): ?>
      <!-- The interactive map lives here -->
      <div id="map"></div>
      <!-- Optional legend container (parkingStatus.js already handles tooltips/colors) -->
      <div id="legend" class="legend" style="position:absolute; right:16px; bottom:16px; z-index:999;"></div>
    <?php else: ?>
      <?php
        // Include any other page without changing it (e.g., pages/about.php -> ?page=about)
        $candidate = __DIR__ . '/pages/' . $page . '.php';
        if (!try_include($candidate)) {
          http_response_code(404);
          echo '<div style="padding:1rem;">Page not found.</div>';
        }
      ?>
    <?php endif; ?>
  </main>

  <?php
    // Optional shared footer you might already have
    try_include(__DIR__ . '/components/footer.php');
  ?>

  <!-- Leaflet JS (required) -->
  <script
    src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"
    crossorigin=""
  ></script>

  <!-- Your existing map logic (the updated file you shared) -->
  <!-- Adjust the src path to where parkingStatus.js actually lives in your project -->
  <script src="/js/parkingStatus.js"></script>

  <!-- If you have any site-wide scripts, they can remain as-is -->
  <?php try_include(__DIR__ . '/components/foot-scripts.php'); ?>
</body>
</html>
