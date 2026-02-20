 document.getElementById("cropForm").addEventListener("submit", async (event) => {
  event.preventDefault();

  // Get input values from form
  const N = document.getElementById("nitrogen").value;
  const P = document.getElementById("phosphorus").value;
  const K = document.getElementById("potassium").value;
  const pH = document.getElementById("ph") ? document.getElementById("ph").value : 6.5; // default if no input

  // Get user's current location
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      try {
        // Send POST request to backend
        const response = await fetch("/recommend", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ N, P, K, pH, Latitude: lat, Longitude: lon })
        });

        const data = await response.json();

        // Display recommendation and weather
        const resultDiv = document.getElementById("result");
        resultDiv.innerHTML = `
          <div class="card">
            <h2>Recommended Crop 🌱</h2>
            <p class="crop">${data.recommendation}</p>

            <h3>📍 Location Weather: ${data.location}</h3>
            <ul>
              <li>🌡️ Temperature: ${data.weather.temperature} °C</li>
              <li>💧 Humidity: ${data.weather.humidity}%</li>
              <li>🌧️ Rainfall: ${data.weather.rainfall} mm</li>
            </ul>
          </div>
        `;
      } catch (err) {
        console.error("Error:", err);
        alert("Failed to fetch recommendation. Try again.");
      }
    });
  } else {
    alert("Geolocation is not supported by this browser.");
  }
});
