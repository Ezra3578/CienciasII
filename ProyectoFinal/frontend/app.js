const API_BASE = "http://127.0.0.1:8000";

// Paleta fija de colores para las zonas (evita colores random poco distinguibles).
const ZONE_COLORS = [
  "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
  "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#fabebe",
];

const map = L.map("map").setView([4.60971, -74.08175], 13); // Bogotá por defecto

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 19,
}).addTo(map);

let depot = null; // {lat, lng}
let deliveries = []; // [{lat, lng}, ...]
let markersLayer = L.layerGroup().addTo(map);
let zonesLayer = L.layerGroup().addTo(map);
let routesLayer = L.layerGroup().addTo(map);

function redrawPoints() {
  markersLayer.clearLayers();

  if (depot) {
    L.marker([depot.lat, depot.lng], { title: "Depot" })
      .bindPopup("Depot")
      .addTo(markersLayer);
  }

  deliveries.forEach((p, i) => {
    L.circleMarker([p.lat, p.lng], {
      radius: 6,
      color: "#333",
      fillColor: "#333",
      fillOpacity: 0.8,
    })
      .bindPopup(`Entrega #${i + 1}`)
      .addTo(markersLayer);
  });
}

map.on("click", (e) => {
  const { lat, lng } = e.latlng;
  if (!depot) {
    depot = { lat, lng };
  } else {
    deliveries.push({ lat, lng });
  }
  redrawPoints();
});

document.getElementById("clear-points-btn").addEventListener("click", () => {
  depot = null;
  deliveries = [];
  zonesLayer.clearLayers();
  routesLayer.clearLayers();
  redrawPoints();
  setResults("Puntos limpiados.");
});

function setResults(html) {
  document.getElementById("results-content").innerHTML = html;
}

// --- Etapa 1: construir grafo ---
document.getElementById("build-graph-btn").addEventListener("click", async () => {
  const place = document.getElementById("place-input").value.trim();
  if (!place) return alert("Escribe un lugar, ej: 'Chía, Cundinamarca, Colombia'");

  setResults("Construyendo grafo... (puede tardar según el tamaño de la ciudad)");

  try {
    const res = await fetch(`${API_BASE}/graph/build`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ place_name: place, network_type: "drive" }),
    });
    if (!res.ok) throw new Error(await res.text());
    setResults(`Grafo construido para: <b>${place}</b>. Ahora haz clic en el mapa.`);
  } catch (err) {
    setResults(`Error construyendo el grafo: ${err.message}`);
  }
});

// --- Etapa 2: coloreado / zonas ---
document.getElementById("build-zones-btn").addEventListener("click", async () => {
  if (!depot || deliveries.length === 0) {
    return alert("Marca un depot y al menos un punto de entrega en el mapa.");
  }

  const conflictRadius = parseFloat(document.getElementById("conflict-radius").value);

  setResults("Calculando zonas (coloreado de grafos)...");

  try {
    const res = await fetch(`${API_BASE}/zones/build`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        depot,
        deliveries,
        n_colors: null,
        balance: true,
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    drawZones(data.zones);
    setResults(`Zonas creadas: ${Object.keys(data.zones).length}`);
  } catch (err) {
    setResults(`Error creando zonas: ${err.message}`);
  }
});

function drawZones(zones) {
  zonesLayer.clearLayers();

  Object.entries(zones).forEach(([color, points], idx) => {
    const zoneColor = ZONE_COLORS[idx % ZONE_COLORS.length];
    points.forEach((p) => {
      L.circleMarker([p.lat, p.lng], {
        radius: 8,
        color: zoneColor,
        fillColor: zoneColor,
        fillOpacity: 0.9,
      })
        .bindPopup(`Zona ${color}`)
        .addTo(zonesLayer);
    });
  });
}

// --- Etapa 3: planificar rutas por zona ---
document.getElementById("plan-routes-btn").addEventListener("click", async () => {
  if (!depot || deliveries.length === 0) {
    return alert("Marca un depot y al menos un punto de entrega en el mapa.");
  }

  setResults("Planificando rutas por zona (TSP heurístico)...");

  try {
    const res = await fetch(`${API_BASE}/zones/plan-routes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        depot,
        deliveries,
        n_colors: null,
        balance: true,
        tsp_method: "nn_2opt",
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();

    drawRoutes(data.zones);
    renderResultsTable(data.zones);
  } catch (err) {
    setResults(`Error planificando rutas: ${err.message}`);
  }
});

function drawRoutes(zones) {
  routesLayer.clearLayers();

  Object.entries(zones).forEach(([color, info], idx) => {
    const zoneColor = ZONE_COLORS[idx % ZONE_COLORS.length];
    const latlngs = info.ordered_points.map((p) => [p.lat, p.lng]);

    L.polyline(latlngs, { color: zoneColor, weight: 4, opacity: 0.8 }).addTo(routesLayer);
  });
}

function renderResultsTable(zones) {
  let html = "";
  Object.entries(zones).forEach(([color, info]) => {
    html += `
      <div class="zone-card">
        <b>Zona ${color}</b><br/>
        Distancia total: ${(info.total_distance_meters / 1000).toFixed(2)} km<br/>
        Tiempo de cómputo: ${(info.compute_time_seconds * 1000).toFixed(1)} ms<br/>
        Método: ${info.method}
      </div>
    `;
  });
  setResults(html || "Sin zonas.");
}

redrawPoints();
