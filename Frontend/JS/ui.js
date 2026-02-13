/* =========================
   NAVIGATION FUNCTIONS
   ========================= */

function goLogin() {
  window.location.href = "login.html";
}

function goSignup() {
  window.location.href = "signup.html";
}

function goPredict() {
  window.location.href = "disease_predict.html";
}

function goExplorer() {
  window.location.href = "disease_explorer.html";
}

function goAIDoctor() {
  window.location.href = "ai_doctor.html";
}

function goRecords() {
  window.location.href = "health_records.html";
}

function goEmergency() {
  window.location.href = "emergency.html"; 
}

/* =========================
   NAVBAR AUTH LOGIC
========================= */

function initNavbarAuth() {
  const navAuth = document.getElementById("navAuth");
  if (!navAuth) return;

  const user = JSON.parse(localStorage.getItem("healnova_user"));

  if (user) {
    navAuth.innerHTML = `
      <div class="account">
        <button class="account-btn" onclick="toggleAccountMenu(event)">
          👤 ${user.name}
        </button>
        <div class="account-menu">
          <button onclick="logout()">Logout</button>
        </div>
      </div>
    `;
  } else {
    navAuth.innerHTML = `
      <button class="login-btn" onclick="goLogin()">Login</button>
    `;
  }
}

/* TOGGLE LOGOUT MENU */
function toggleAccountMenu(e) {
  e.stopPropagation(); // 
  const account = document.querySelector(".account");
  if (account) {
    account.classList.toggle("show");
  }
}

/* CLOSE MENU WHEN CLICKING OUTSIDE */
document.addEventListener("click", () => {
  const account = document.querySelector(".account");
  if (account) {
    account.classList.remove("show");
  }
});

/* LOGOUT */
function logout() {
  localStorage.removeItem("healnova_user");
  window.location.href = "index.html";
}

/* =========================
   AUTO-SCROLL FEATURES (HOME)
   ========================= */

document.addEventListener("DOMContentLoaded", () => {
  const features = document.querySelector(".features");

  if (features) {
    let scrollAmount = 0;

    setInterval(() => {
      scrollAmount += 280;

      if (scrollAmount >= features.scrollWidth - features.clientWidth) {
        scrollAmount = 0;
      }

      features.scrollTo({
        left: scrollAmount,
        behavior: "smooth"
      });
    }, 4000);
  }
});

function toggleMenu() {
  document.getElementById("navMenu").classList.toggle("show");
}

function goHome() {
  window.location.href = "index.html";
}

/* =========================
   AI DOCTOR DAILY LIMIT
========================= */

const AI_LIMIT_PER_DAY = 5;

function canAskAIDoctor() {
  const user = JSON.parse(localStorage.getItem("healnova_user"));
  if (!user) return false;

  const today = new Date().toLocaleDateString();
  const key = `ai_limit_${user.email}`;

  let data = JSON.parse(localStorage.getItem(key));

  // First time today
  if (!data || data.date !== today) {
    data = { date: today, count: 0 };
  }

  if (data.count >= AI_LIMIT_PER_DAY) {
    return false;
  }

  data.count += 1;
  localStorage.setItem(key, JSON.stringify(data));
  return true;
}
