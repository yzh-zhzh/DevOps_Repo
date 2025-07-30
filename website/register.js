
  // Import the functions you need from the SDKs you need
  import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
  // TODO: Add SDKs for Firebase products that you want to use
  // https://firebase.google.com/docs/web/setup#available-libraries

  // Your web app's Firebase configuration
  const firebaseConfig = {
    apiKey: "AIzaSyBbPSfgU4hYMyPEM9S9L8z5xFx7XdMVWeo",
    authDomain: "fire-alarm-system-77832.firebaseapp.com",
    projectId: "fire-alarm-system-77832",
    storageBucket: "fire-alarm-system-77832.firebasestorage.app",
    messagingSenderId: "233304506178",
    appId: "1:233304506178:web:c479e2b9bf475ad17e12db"
  };

  // Initialize Firebase
  const app = initializeApp(firebaseConfig);


  //inputs
  const roomNumber = document.getElementById("Room Number").value;
  const email = document.getElementById("Email").value; 
  const password = document.getElementById("Password").value;

    //submit button
    const submitButton = document.getElementById("submit");
    submitButton.addEventListener("click", function(event){

        event.preventDefault(); // Prevent the default form submission
    
        // Validate inputs
        if (roomNumber && email && password) {
            // Here you can add code to handle the registration logic, e.g., sending data to a server or Firebase
            console.log("Registration successful with:", {
            roomNumber,
            email,
            password
            });
            alert("Registration successful!");
        } else {
            alert("Please fill in all fields.");
        }
    })