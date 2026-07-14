function getApiBase() {
  if (window.location.hostname.endsWith(".app.github.dev")) {
    return "";
  }

  return "http://127.0.0.1:8000";
}

const API_BASE = getApiBase();

async function fetchApi(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `El backend respondió con ${res.status}`);
  }
  return res;
}

// Paleta de colores para las zonas (opcional para futuras visualizaciones)
const ZONE_COLORS = [
  "#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231",
  "#911eb4", "#46f0f0", "#f032e6", "#bcf60c", "#00ca83",
];

function getZoneColor(zoneId) {
  const text = String(zoneId ?? "");
  let hash = 0;

  for (let i = 0; i < text.length; i += 1) {
    hash = (hash * 31 + text.charCodeAt(i)) >>> 0;
  }

  return ZONE_COLORS[hash % ZONE_COLORS.length];
}

// Límites de Kamppi, Helsinki (aprox.)
const KAMPPI_BOUNDS = [
  [60.1600, 24.9180], // suroeste
  [60.1725, 24.9450]  // noreste
];

const map = L.map("map", {
  maxBounds: KAMPPI_BOUNDS,
  maxBoundsViscosity: 2.0,
}).setView([60.1665, 24.9300], 16);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution: "&copy; OpenStreetMap contributors",
  maxZoom: 20,
  minZoom: 16,
}).addTo(map);

// Datos
let depots = [];          // { name, lat, lng, type: "depot" }
let deliveries = [];      // { name, lat, lng, type: "deploy" }
let isCtrlPressed = false;

// Capas
let markersLayer = L.layerGroup().addTo(map);
let depotCirclesLayer = L.layerGroup().addTo(map);
let hullsLayer = L.layerGroup().addTo(map);
let routesLayer = L.layerGroup().addTo(map);

// --- Funciones de ayuda para nombres ---
function getNextDepotLetter() {
  if (depots.length === 0) return "A";
  const letters = depots.map(d => d.name).filter(n => /^[A-Z]$/.test(n));
  const maxCode = letters.reduce((max, l) => Math.max(max, l.charCodeAt(0)), 64);
  return String.fromCharCode(maxCode + 1);
}

function getNextDeliveryNumber() {
  if (deliveries.length === 0) return "1";
  const nums = deliveries.map(d => parseInt(d.name, 10)).filter(n => !isNaN(n));
  const maxNum = nums.length ? Math.max(...nums) : 0;
  return (maxNum + 1).toString();
}

// --- Distancia Haversine (en metros) ---
function haversineDistance(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const toRad = deg => deg * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat / 2) ** 2 +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) ** 2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

// --- Validación de depot (200 m de separación) ---
function isDepotTooClose(lat, lng) {
  return depots.some(d => haversineDistance(lat, lng, d.lat, d.lng) < 200);
}

// --- Redibujar puntos y círculos de depots ---
function redrawPoints() {
  markersLayer.clearLayers();
  depotCirclesLayer.clearLayers();

  // Dibujar depots
  depots.forEach(dep => {
    const icon = L.divIcon({
      className: 'depot-icon',
      html: `<div style="background:#2563eb;color:white;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-weight:bold;">${dep.name}</div>`,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });
    const marker = L.marker([dep.lat, dep.lng], { icon, customData: dep })
      .bindPopup(`Depot ${dep.name}`)
      .addTo(markersLayer);
    marker.on('contextmenu', (e) => {
      L.DomEvent.preventDefault(e);
      deleteNode(dep);
    });

    if (isCtrlPressed) {
      L.circle([dep.lat, dep.lng], {
        radius: 200,
        color: '#5fbbd9',
        fillColor: '#5fbbd9',
        fillOpacity: 0.15,
        weight: 1
      }).addTo(depotCirclesLayer);
    }
  });

  // Dibujar entregas
  deliveries.forEach(del => {
    const icon = L.divIcon({
      className: 'delivery-icon',
      html: `<div style="background:#e6194b;color:white;border-radius:50%;width:20px;height:20px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:bold;">${del.name}</div>`,
      iconSize: [20, 20],
      iconAnchor: [10, 10]
    });
    const marker = L.marker([del.lat, del.lng], { icon, customData: del })
      .bindPopup(`Entrega ${del.name}`)
      .addTo(markersLayer);
    marker.on('contextmenu', (e) => {
      L.DomEvent.preventDefault(e);
      deleteNode(del);
    });
  });
}

function updateCtrlState(isPressed) {
  isCtrlPressed = isPressed;
  redrawPoints();
}

function deleteNode(node) {
  if (node.type === "depot") {
    depots = depots.filter(d => d.name !== node.name);
  } else {
    deliveries = deliveries.filter(d => d.name !== node.name);
  }
  redrawPoints();
  // Limpiar resultados previos al eliminar nodos
  hullsLayer.clearLayers();
  routesLayer.clearLayers();
  setResults("Nodo eliminado.");
}

// --- Eventos del mapa ---
document.addEventListener("keydown", (e) => {
  if (e.ctrlKey || e.metaKey) {
    updateCtrlState(true);
  }
});

document.addEventListener("keyup", (e) => {
  if (!e.ctrlKey && !e.metaKey) {
    updateCtrlState(false);
  }
});

map.on("click", (e) => {
  const isCtrl = e.originalEvent.ctrlKey || e.originalEvent.metaKey;
  // Solo ignoramos el clic sobre un marcador si NO es para agregar depot
  if (!isCtrl && e.originalEvent.target.closest('.leaflet-marker-icon')) return;

  const { lat, lng } = e.latlng;

  if (isCtrl) {
    if (isDepotTooClose(lat, lng)) {
      alert("No se puede agregar depot: hay otro a menos de 200 m.");
      return;
    }
    const name = getNextDepotLetter();
    depots.push({ name, lat, lng, type: "depot" });
  } else {
    const name = getNextDeliveryNumber();
    deliveries.push({ name, lat, lng, type: "deploy" });
  }
  redrawPoints();
});

map.on("contextmenu", (e) => {
  // Previene el menú contextual del navegador en el mapa vacío
  L.DomEvent.preventDefault(e);
});

// --- Botón de procesamiento ---
document.getElementById("process-btn").addEventListener("click", async () => {
  if (depots.length === 0) return alert("Agrega al menos un depot.");
  if (deliveries.length === 0) return alert("Agrega al menos un punto de entrega.");

  const maxNodes = parseInt(document.getElementById("max-nodes-input").value, 10) || 5;

  const nodesPayload = [
    ...depots.map(d => ({ name: d.name, type: "depot", longitude: d.lng, latitude: d.lat })),
    ...deliveries.map(d => ({ name: d.name, type: "deploy", longitude: d.lng, latitude: d.lat }))
  ];

  setResults("Procesando...");

  try {
    const res = await fetchApi("/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ nodes: nodesPayload, max_nodos_por_zona: maxNodes })
    });
    const data = await res.json();

    hullsLayer.clearLayers();
    routesLayer.clearLayers();

    drawConvexHulls(data);
    drawRoutes(data);

    const regionCount = Object.keys(data || {}).length;
    setResults(`Procesamiento completado. Se dibujaron ${regionCount} zonas.`);

  } catch (err) {
    setResults(`Error: ${err.message}`);
  }
});

function drawConvexHulls(regions) {
  Object.entries(regions).forEach(([regionId, regionData]) => {
    const points = Array.isArray(regionData?.frontera) ? regionData.frontera : [];
    const coords = points
      .map(point => {
        if (point && typeof point === "object") {
          if (typeof point.latitud === "number" && typeof point.longitud === "number") {
            return [point.latitud, point.longitud];
          }
        }
        return null;
      })
      .filter(Boolean);

    if (coords.length > 2) {
      L.polygon(coords, {
        color: getZoneColor(regionId),
        fillColor: getZoneColor(regionId),
        opacity: 0.4,
        fillOpacity: 0.1,
        weight: 3
      }).addTo(hullsLayer).bindPopup(`Región ${regionId}`);
    }
  });
}

function drawRoutes(regions) {
  Object.entries(regions).forEach(([routeId, regionData]) => {
    const routePoints = Array.isArray(regionData?.ruta) ? regionData.ruta : [];
    const latlngs = routePoints
      .map(point => {
        if (point && typeof point === "object") {
          if (typeof point.latitud === "number" && typeof point.longitud === "number") {
            return [point.latitud, point.longitud];
          }
        }
        return null;
      })
      .filter(Boolean);

    if (latlngs.length > 1) {
      const zoneColor = getZoneColor(routeId);

      const routeLine = L.polyline(latlngs, {
        color: zoneColor,
        weight: 2,
        opacity: 0.8,
        dashArray: 10
      }).addTo(routesLayer).bindPopup(`Ruta ${routeId}`);

      L.polylineDecorator(routeLine, {
        patterns: [
          {
            offset: '5%',
            repeat: '10%',
            symbol: L.Symbol.arrowHead({
              pixelSize: 10,
              polygon: false,
              pathOptions: { stroke: true, color: zoneColor, weight: 2 }
            })
          }
        ]
      }).addTo(routesLayer);
    }
  });
}

function setResults(html) {
  document.getElementById("results-content").innerHTML = html;
}

// Inicializar dibujo
redrawPoints();