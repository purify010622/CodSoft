import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";
import { getAnalytics } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyDSypBnBLnqXaMFA5q4Fb71rFVHdfDftrU",
  authDomain: "codsoft-d33d8.firebaseapp.com",
  projectId: "codsoft-d33d8",
  storageBucket: "codsoft-d33d8.firebasestorage.app",
  messagingSenderId: "26503093818",
  appId: "1:26503093818:web:9d9b305cb8657dc1cd5f03",
  measurementId: "G-TZ21C22Z6V"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
