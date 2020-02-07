// static/main.js

console.log("Sanity check!");

// new
// Get Stripe publishable key
fetch("http://127.0.0.1:8000/stripe/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  console.log('STRIPE INSTANCE CREATED', stripe)
  // new
  // Event handler
  document.querySelector("#submitBtn").addEventListener("click", () => {
    // Get Checkout Session ID
    fetch("http://127.0.0.1:8000/stripe/create-checkout-session/")
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log('DATA', data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  });
});
