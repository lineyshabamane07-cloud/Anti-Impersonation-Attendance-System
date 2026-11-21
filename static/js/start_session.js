
const latEl = document.getElementById("lat");
const lngEl = document.getElementById("lng");
const msgEl = document.getElementById("loc-msg");
const errEl = document.getElementById("form-error");

document.getElementById("btn-loc").addEventListener("click", () => {
 msgEl.textContent = "Getting your location...";
 navigator.geolocation.getCurrentPosition(
   (pos) => {
    latEl.value = pos.coords.latitude.toFixed(6);
    lngEl.value = pos.coords.longitude.toFixed(6);
    msgEl.textContent = "Location captured (accuracy about " + Math.round(pos.coords.accuracy)
+ " m).";
   },
   (err) => {
    msgEl.textContent = "Could not get location (" + err.message + "). Type the numbers in by
hand.";
   },
   { enableHighAccuracy: true, timeout: 15000 }
 );
});

document.getElementById("session-form").addEventListener("submit", async (event) => {
 event.preventDefault();
 errEl.textContent = "";
 const body = {
  lat: latEl.value,
  lng: lngEl.value,
  radius_m: document.getElementById("radius").value,
  refresh_s: document.getElementById("refresh").value,
  duration_min: document.getElementById("duration").value,
 };
 const res = await fetch("/faculty/session/start", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(body),
 });
 const data = await res.json();
 if (!res.ok) {
   errEl.textContent = data.error || "Could not start the session.";
   return;
 }
 window.location.href = "/faculty/session/" + data.session_id;
});
