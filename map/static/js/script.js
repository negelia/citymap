// Инициализация карты
mapboxgl.accessToken = 'pk.eyJ1IjoibmVnZWxpYSIsImEiOiJjbTlia3dtajkwYnYwMmxzYXhwc2kweHI0In0.DJ_UuwkqthuDDjY2HUQpRg'; 
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v12',
  center: [37.618423, 55.751244],
  zoom: 12
});

let addMode = false;
let clickedLngLat = null;
let toiletMarkers = [];
let toiletCount = JSON.parse(localStorage.getItem("toiletCount") || "0");
let backendMarkers = JSON.parse(localStorage.getItem("backendMarkers") || "[]");

// Функции для работы с аутентификацией
function switchAuthTab(tab) {
  if (tab === 'login') {
    document.getElementById('loginForm').classList.remove('hidden');
    document.getElementById('registerForm').classList.add('hidden');
    document.querySelectorAll('.tab')[0].classList.add('active');
    document.querySelectorAll('.tab')[1].classList.remove('active');
  } else {
    document.getElementById('loginForm').classList.add('hidden');
    document.getElementById('registerForm').classList.remove('hidden');
    document.querySelectorAll('.tab')[0].classList.remove('active');
    document.querySelectorAll('.tab')[1].classList.add('active');
  }
}

function login() {
  alert('Вход выполнен!');
  hideAuthModal();
}

function register() {
  alert('Регистрация успешна!');
  hideAuthModal();
}

function hideAuthModal() {
  document.getElementById('authModal').classList.add('hidden');
}

// Функции для работы с картой
map.on('load', () => {
  loadModeratedMarkers();
});

function enableAddMode() {
  addMode = true;
  alert("Нажмите на карту, чтобы добавить точку.");
}

map.on('click', (e) => {
  if (addMode) {
    clickedLngLat = e.lngLat;
    const modal = new bootstrap.Modal(document.getElementById('addModal'));
    modal.show();
  }
});

function addMarker({id, lng, lat, title, description, photo, rating, category, moderated}) {
  let photoHtml = '';
  if (photo) {
    if (photo.startsWith('data:') || photo.startsWith('http')) {
      photoHtml = `<br><img src="${photo}" style="max-width:100%;">`;
    } else {
      photoHtml = `<br><img src="/media/${photo}" style="max-width:100%;">`;
    }
  }

  const popup = new mapboxgl.Popup()
    .setHTML(`
      <b>${title}</b><br>
      ${description}<br>
      Рейтинг: ${rating}/5<br>
      Категория: ${getCategoryName(category)}
      ${photoHtml}
    `);

  const marker = new mapboxgl.Marker({
    color: getCategoryColor(category)
  })
    .setLngLat([lng, lat])
    .setPopup(popup)
    .addTo(map);
  
  marker.id = id;
  marker.category = category;
  marker.moderated = moderated;
  toiletMarkers.push(marker);
}

function getCategoryName(category) {
  return {
    'toilet': 'Санузел',
    'water': 'Пополнение воды',
    'rest': 'Зона отдыха'
  }[category] || category;
}

function getCategoryColor(category) {
  return {
    'toilet': 'var(--pink)',
    'water': 'var(--water-blue)',
    'rest': 'var(--rest-green)'
  }[category] || '#000000';
}

function filterMarkersByCategory() {
  const selected = document.getElementById("filterSelect").value;
  toiletMarkers.forEach(marker => {
    if (selected === "all" || marker.category === selected) {
      marker.addTo(map);
    } else {
      marker.remove();
    }
  });
}

async function loadModeratedMarkers() {
  try {
    const response = await fetch('/api/markers/');
    if (response.ok) {
      backendMarkers = await response.json();
      backendMarkers.forEach(markerData => addMarker(markerData));
      
      const localMarkers = JSON.parse(localStorage.getItem("backendMarkers") || "[]");
      localMarkers.forEach(markerData => {
        if (!backendMarkers.some(m => m.id === markerData.id)) {
          addMarker(markerData);
        }
      });
      return;
    }
  } catch (error) {
    console.error("Error loading markers from backend:", error);
  }
  
  backendMarkers = JSON.parse(localStorage.getItem("backendMarkers") || "[]");
  backendMarkers
    .filter(m => m.moderated)
    .forEach(markerData => addMarker(markerData));
}

async function saveToBackend(markerData) {
  try {
      const formData = new FormData();
      formData.append('lng', markerData.lng);
      formData.append('lat', markerData.lat);
      formData.append('title', markerData.title);
      formData.append('description', markerData.description || '');
      formData.append('rating', markerData.rating);
      formData.append('category', markerData.category);
      formData.append('moderated', markerData.moderated);
      
      if (markerData.photo && markerData.photo.startsWith('data:')) {
          const blob = await fetch(markerData.photo).then(r => r.blob());
          formData.append('photo', blob, 'photo.jpg');
      }

      const response = await fetch('/api/markers/add/', {
          method: 'POST',
          body: formData,
          headers: {
              'X-CSRFToken': getCookie('csrftoken')
          }
      });

      if (!response.ok) throw new Error('Network response was not ok');
      
      return await response.json();
  } catch (error) {
      console.error('Error saving marker:', error);
      return {
          status: 'error',
          message: error.message
      };
  }
}

function isModerator() {
  return document.getElementById("roleSelect").value === "moderator";
}

document.getElementById("toiletForm").addEventListener("submit", async function(e) {
  e.preventDefault();
  
  const title = document.getElementById("toiletTitle").value.trim();
  const description = document.getElementById("toiletDescription").value.trim();
  const rating = +document.getElementById("toiletRating").value;
  const category = document.getElementById("toiletCategory").value;
  const moderated = isModerator() && document.getElementById("moderationCheckbox").checked;
  const photoInput = document.getElementById("toiletPhoto");
  
  if (!title || !rating || !category) {
      alert("Пожалуйста, заполните обязательные поля.");
      return;
  }

  const markerData = { 
      id: Date.now(),
      lng: clickedLngLat.lng, 
      lat: clickedLngLat.lat, 
      title, 
      description, 
      rating, 
      category, 
      moderated,
      photo: null
  };

  if (photoInput.files[0]) {
      markerData.photo = await convertImageToBase64(photoInput.files[0]);
  }

  try {
      const result = await saveToBackend(markerData);
      
      if (result.status === 'success') {
          addMarker(markerData);
          backendMarkers.push(markerData);
          localStorage.setItem("backendMarkers", JSON.stringify(backendMarkers));
          
          clickedLngLat = null;
          addMode = false;
          e.target.reset();
          bootstrap.Modal.getInstance(document.getElementById('addModal')).hide();

          toiletCount++;
          localStorage.setItem("toiletCount", toiletCount);
          checkRewards();
      } else {
          throw new Error(result.message || 'Unknown error');
      }
  } catch (error) {
      console.error('Error saving to backend:', error);
      markerData.moderated = false;
      addMarker(markerData);
      backendMarkers.push(markerData);
      localStorage.setItem("backendMarkers", JSON.stringify(backendMarkers));
      
      clickedLngLat = null;
      addMode = false;
      e.target.reset();
      bootstrap.Modal.getInstance(document.getElementById('addModal')).hide();
      
      alert("Сервер недоступен. Точка сохранена локально.");
  }
});

function convertImageToBase64(file) {
  return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
      reader.readAsDataURL(file);
  });
}

function findNearby() {
  if (!navigator.geolocation) return alert("Геолокация не поддерживается.");
  navigator.geolocation.getCurrentPosition(pos => {
    const { latitude: lat, longitude: lng } = pos.coords;
    map.flyTo({ center: [lng, lat], zoom: 15 });
    
    if (map.getSource('user-location')) {
      map.getSource('user-location').setData({
        type: 'Feature',
        geometry: {
          type: 'Point',
          coordinates: [lng, lat]
        }
      });
    } else {
      map.addSource('user-location', {
        type: 'geojson',
        data: {
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [lng, lat]
          }
        }
      });
      
      map.addLayer({
        id: 'user-location-circle',
        type: 'circle',
        source: 'user-location',
        paint: {
          'circle-radius': 300,
          'circle-color': 'var(--water-blue)',
          'circle-opacity': 0.2,
          'circle-stroke-width': 2,
          'circle-stroke-color': 'var(--water-blue)'
        }
      });
    }
  });
}

// Функции для работы с чатом
const chatForm = document.getElementById("chatForm");
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const usernameInput = document.getElementById("usernameInput");

const storedMessages = JSON.parse(localStorage.getItem("chatMessages")) || [];
storedMessages.forEach(({ name, message }) => addChatMessage(name, message));

chatForm.addEventListener("submit", function(e) {
  e.preventDefault();
  const name = usernameInput.value.trim() || "Аноним";
  const message = chatInput.value.trim();
  if (message) {
    addChatMessage(name, message);
    saveChatMessage(name, message);
    chatInput.value = "";
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
});

function addChatMessage(name, message) {
  const msgEl = document.createElement("div");
  msgEl.className = "chat-message";
  msgEl.style.backgroundColor = stringToColor(name);
  msgEl.innerHTML = `<span>${name}:</span> ${message} `;
  chatMessages.appendChild(msgEl);
}

function saveChatMessage(name, message) {
  const saved = JSON.parse(localStorage.getItem("chatMessages")) || [];
  saved.push({ name, message });
  localStorage.setItem("chatMessages", JSON.stringify(saved));
}

function stringToColor(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) hash = str.charCodeAt(i) + ((hash << 5) - hash);
  const color = Math.floor(Math.abs(Math.sin(hash) * 16777215)).toString(16);
  return "#" + "000000".substring(0, 6 - color.length) + color;
}

// Система наград
function checkRewards() {
  const rewardText = document.getElementById("rewardText");
  const rewardModal = new bootstrap.Modal(document.getElementById("rewardModal"));
  if (toiletCount === 3) {
    rewardText.innerText = "🚽 БимбоТуалет!";
    rewardModal.show();
  } else if (toiletCount === 5) {
    rewardText.innerText = "🕺 ТУАЛЕТНЫЙ МАЧО!";
    rewardModal.show();
  } else if (toiletCount === 7) {
    rewardText.innerText = "👑 Король Унитазов!";
    rewardModal.show();
  } else if (toiletCount === 10) {
    rewardText.innerText = "🌈 Легенда Очка!";
    rewardModal.show();
  }
}

// Вспомогательные функции
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}