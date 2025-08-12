import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";


import firebaseConfig from './firebaseConfig.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const name = document.getElementById("name").value;
  const age = document.getElementById("age").value;
  const emergencyContact = document.getElementById("emergencyContact").value;

  const user = auth.currentUser;
  if (!user) {
    alert("No logged in user, please login first.");
    window.location.href = "/";
    return;
  }

  try {
    const userDocRef = doc(db, "users", user.uid);
    await updateDoc(userDocRef, {
      name,
      age,
      emergencyContact
    });
    alert("Profile updated! Please log in again.");
    window.location.href = "/";  // Redirect to login page
  } catch (error) {
    alert("Failed to update profile: " + error.message);
  }
});
