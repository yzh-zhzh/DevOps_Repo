import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

import firebaseConfig from './firebaseConfig.js';

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

document.querySelector("form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  try {
    // Create user with email & password
    const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    const user = userCredential.user;

    // Optional: create empty user doc in Firestore with user.uid as id
    const userDocRef = doc(db, "users", user.uid);
    await setDoc(userDocRef, {
      email: email,
      createdAt: new Date(),
      // You can leave other fields empty for now to be filled in complete-profile page
    });

    // Redirect to complete-profile page after successful registration
    window.location.href = "/";
  } catch (error) {
    alert("Registration failed: " + error.message);
  }
});
