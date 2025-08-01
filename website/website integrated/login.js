
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
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

// Handle login form submission
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const userCredential = await signInWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    const docRef = doc(db, "users", user.uid);
    const userSnap = await getDoc(docRef);

    if (!userSnap.exists()) {
      alert("User document not found.");
      return;
    }

    const userData = userSnap.data();

    // Check if profile is incomplete
    if (!userData.name || !userData.age || !userData.emergencyContact) {
      window.location.href = "complete-profile.html";
    } else {
      window.location.href = "profile.html";
    }

  } catch (error) {
  if (error.code === "unavailable" || error.message.includes("offline")) {
    alert("You're offline or Firestore isn't reachable. Please check your internet and Firebase setup.");
  } else {
    alert("Login failed: " + error.message);
  }
}
});
