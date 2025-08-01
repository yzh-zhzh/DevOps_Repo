import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBbPSfgU4hYMyPEM9S9L8z5xFx7XdMVWeo",
  authDomain: "fire-alarm-system-77832.firebaseapp.com",
  projectId: "fire-alarm-system-77832",
  storageBucket: "fire-alarm-system-77832.firebasestorage.app",
  messagingSenderId: "233304506178",
  appId: "1:233304506178:web:c479e2b9bf475ad17e12db",
};


const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Wait for user to be authenticated
onAuthStateChanged(auth, async (user) => {
  if (!user) {
    window.location.href = "index.html"; // Not logged in
    return;
  }

  document.getElementById("email").textContent = user.email;

  try {
    const userDoc = await getDoc(doc(db, "users", user.uid));
    if (userDoc.exists()) {
      const data = userDoc.data();
      document.getElementById("roomNumber").textContent = data.roomNumber || "Not set";
      document.getElementById("name").textContent = data.name || "Not set";
      document.getElementById("age").textContent = data.age || "Not set";
      document.getElementById("emergencyContact").textContent = data.emergencyContact || "Not set";
    } else {
      alert("User data not found.");
    }
  } catch (error) {
    console.error("Error fetching profile data:", error);
    alert("Failed to load profile.");
  }
});
