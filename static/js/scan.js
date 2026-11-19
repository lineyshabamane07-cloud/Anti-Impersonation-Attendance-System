
const statusEl = document.getElementById("status-msg");
const locEl = document.getElementById("loc-status");
const scanView = document.getElementById("scan-view");
const resultView = document.getElementById("result-view");

let position = null; // latest GPS reading: {lat, lng}
let scanner = null;
let busy = false;   // true while waiting for the server (stops double submits)

// A random id saved in this browser the first time. It identifies this phone.
function getDeviceId() {
  let id = localStorage.getItem("aias_device_id");
  if (!id) {
    id = window.crypto && crypto.randomUUID
     ? crypto.randomUUID()
     : "dev-" + Date.now() + "-" + Math.random().toString(16).slice(2);
    localStorage.setItem("aias_device_id", id);
  }
  return id;
}

function watchLocation() {
  if (!navigator.geolocation) {
    locEl.textContent = "Location is not supported on this browser.";
    return;
  }
  navigator.geolocation.watchPosition(
    (pos) => {
     position = { lat: pos.coords.latitude, lng: pos.coords.longitude };
     locEl.textContent = "Location: OK (accuracy about " + Math.round(pos.coords.accuracy) + " m)";
    },
    (err) => {
     position = null;
     locEl.textContent = "Location blocked (" + err.message + "). Allow location for this site, then reload.";
    },
    { enableHighAccuracy: true, maximumAge: 5000, timeout: 20000 }
  );
}

async function startScanner() {
 scanner = new Html5Qrcode("reader");
    try {
      await scanner.start(
        { facingMode: "environment" },
        { fps: 10, qrbox: { width: 250, height: 250 } },
        (decodedText) => submitToken(decodedText),
        () => {}                    // called for frames with no QR code: ignore
      );
      statusEl.textContent = "Point the camera at the QR code on the screen.";
    } catch (err) {
      statusEl.textContent = "Camera not available (" + err + "). Use the box below.";
    }
}

const LOOKS = {
 present: { icon: "   ✔", title: "Attendance marked", cls: "status-ok" },
 flagged: { icon: "   ⚠", title: "Under review", cls: "status-warn" },
 rejected: { icon: "  ✖", title: "Not marked", cls: "status-bad" },
};

function showResult(data) {
  const look = LOOKS[data.status] || LOOKS.rejected;
  const icon = document.getElementById("result-icon");
  icon.textContent = look.icon;
  icon.className = look.cls;
  document.getElementById("result-title").textContent = look.title;
  document.getElementById("result-reason").textContent = data.reason;
  document.getElementById("result-distance").textContent =
   data.distance_m !== null && data.distance_m !== undefined
    ? "Distance from classroom: " + Math.round(data.distance_m) + " m"
    : "";
  scanView.classList.add("d-none");
  resultView.classList.remove("d-none");
}

async function submitToken(token) {
 if (busy) return;
 busy = true;
 statusEl.textContent = "Checking...";
 try { if (scanner) await scanner.stop(); } catch (e) { /* camera was not running */ }

    const body = {
     token: token.trim(),
     lat: position ? position.lat : null,
     lng: position ? position.lng : null,
     device_id: getDeviceId(),
    };
    let data;

  try {
    const res = await fetch("/student/mark", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    data = await res.json();
    if (!res.ok) data = { status: "rejected", reason: data.error || "Server error", distance_m: null };
  } catch (e) {
    data = { status: "rejected", reason: "Something went wrong. Check your internet and that you are still logged in.", distance_m: null };
  }

  showResult(data);
  busy = false;
}

document.getElementById("btn-manual").addEventListener("click", () => {
 const value = document.getElementById("manual-token").value;
 if (value.trim()) submitToken(value);
});

document.getElementById("btn-again").addEventListener("click", () => {
 resultView.classList.add("d-none");
 scanView.classList.remove("d-none");
 statusEl.textContent = "Starting camera...";
 startScanner();
});

watchLocation();
startScanner();
