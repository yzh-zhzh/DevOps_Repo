import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

import firebaseConfig from './firebaseConfig.js';

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// Load profile data when user is logged in
onAuthStateChanged(auth, async (user) => {
  if (!user) {
    alert("No logged in user, please login first.");
    window.location.href = "/";
    return;
  }

  try {
    const userDocRef = doc(db, "users", user.uid);
    const userDoc = await getDoc(userDocRef);

    if (userDoc.exists()) {
      const data = userDoc.data();
      document.getElementById("resident-name").textContent = data.name || "N/A";
      document.getElementById("room-number").textContent = data.roomNumber || "N/A";
      document.getElementById("age").textContent = data.age || "N/A";
      document.getElementById("emergency-contact").textContent = data.emergencyContact || "N/A";
    } else {
      alert("User profile not found in database!");
    }
  } catch (error) {
    console.error("Error fetching profile:", error);
    alert("Failed to fetch profile: " + error.message);
  }
});
