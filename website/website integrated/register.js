import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// 🔁 Replace with your actual Firebase config
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

// 🔁 Get form
document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  // ✅ Replace with corrected IDs (no spaces)
  const room = document.getElementById("roomNumber").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // ✅ Store extra details in Firestore
    await setDoc(doc(db, "users", user.uid), {
      email,
      roomNumber: room
    });

    alert("Registration successful!");
    window.location.href = "index.html"; // ✅ Redirect to login page
  } catch (error) {
    alert("Registration failed: " + error.message);
    console.error(error);
  }
});
