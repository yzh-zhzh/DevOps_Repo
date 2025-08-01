import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getAuth,
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import {
  getFirestore,
  doc,
  getDoc
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

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

// Wait for the user to be logged in
onAuthStateChanged(auth, async user => {
  if (user) {
    const docRef = doc(db, "users", user.uid);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      const data = docSnap.data();
      document.getElementById("resident-name").textContent = data.name || "N/A";
      document.getElementById("room-number").textContent = data.roomNumber || "N/A";
      document.getElementById("age").textContent = data.age || "N/A";
      document.getElementById("emergency-contact").textContent = data.emergencyContact || "N/A";
    } else {
      alert("Profile data not found.");
    }
  } else {
    window.location.href = "index.html"; // redirect to login
  }
});
