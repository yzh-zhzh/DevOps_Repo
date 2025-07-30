// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBbPSfgU4hYMyPEM9S9L8z5xFx7XdMVWeo",
  authDomain: "fire-alarm-system-77832.firebaseapp.com",
  projectId: "fire-alarm-system-77832",
  storageBucket: "fire-alarm-system-77832.firebasestorage.app",
  messagingSenderId: "233304506178",
  appId: "1:233304506178:web:c479e2b9bf475ad17e12db",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

//inputs
const roomNumber = document.getElementById("Room Number").value;
const email = document.getElementById("Email").value;
const password = document.getElementById("Password").value;

//submit button
const submitButton = document.getElementById("submit");
submitButton.addEventListener("click", function (event) {
  event.preventDefault(); // Prevent the default form submission

  //inputs
  const roomNumber = document.getElementById("Room Number").value;
  const email = document.getElementById("Email").value;
  const password = document.getElementById("Password").value;
  createUserWithEmailAndPassword(getAuth(), email, password)
    .then((userCredential) => {
      // Signed in
      const user = userCredential.user;
      console.log("User registered successfully:", user);
      window.location.href = "index.html"; // Redirect to login page after successful registration
      // You can redirect or show a success message here
    })
    .catch((error) => {
      const errorCode = error.code;
      const errorMessage = error.message;
      console.error("Error registering user:", errorCode, errorMessage);
      alert("Error registering user: " + errorMessage);
      // Handle errors here (e.g., show an error message to the user)
    });
});
