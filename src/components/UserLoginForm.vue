<template>
  <div class="login-page">
    <div class="login-container">
      <h1 class="logo">Jam-Date</h1>
      <h2>Login</h2>
      <form @submit.prevent="login_user">
        <input type="text" v-model="username" placeholder="Username" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <button type="submit">Login</button>
      </form>
      <!-- <p v-if="message">{{ message }}</p> -->
    </div>
  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue';

  // Reactive variables
  const username = ref('');
  const password = ref('');
  const message = ref('');
  const errors = ref([]);
  const csrf_token = ref('');

  // Fetch CSRF token
  const getCsrfToken = async () => {
    try {
      const response = await fetch('/api/v1/csrf-token');
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      csrf_token.value = data.csrf_token;
      console.log('CSRF Token fetched:', csrf_token.value);
    } catch (err) {
      console.error('Failed to get CSRF token:', err);
      message.value = 'Unable to connect to the server.';
      errors.value = [err.message];
    }
  };

  // On component mount, fetch the CSRF token
  onMounted(() => {
    getCsrfToken();
  });

  // Login function
  const login_user = async () => {
    // Clear any previous messages
    message.value = '';
    errors.value = [];

    // Basic validation
    // if (!username.value || !password.value) {
    //   errors.value.push('Username and password are required.');
    //   return;
    // }

    // Prepare form data for the login request
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);

    try {
      // Send login request
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        body: formData,
        headers: {
          'X-CSRFToken': csrf_token.value,
        },
      });

      const data = await response.json();
      
      if (response.ok) {
        // Handle successful login
        message.value = 'Login successful!';
        // Optionally, redirect after login (e.g., to a dashboard)
        setTimeout(() => {window.location.href = '/user'; }, 2000);
      } else {
        // Handle login error
        errors.value = data.errors || [data.message || 'Login failed.'];
      }
    } catch (error) {
      console.error('Error during login:', error);
      errors.value = ['An error occurred during login. Please try again.'];
    }
  };
</script>



<style scoped>
.login-page {
  min-height: 100vh;
  background-image: url('@/assets/Login.jpg'); 
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  padding: 40px;
  border-radius: 12px;
  color: white;
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.logo {
  font-size: 32px;
  margin-bottom: 20px;
}

form input {
  display: block;
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border-radius: 6px;
  border: none;
  font-size: 1rem;
}

button {
  padding: 12px;
  width: 100%;
  background-color: rgb(132, 209, 245);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color: rgb(95, 189, 233);
}

p {
margin-top: 15px;
  color: red;
  font-weight: bold;
}
</style>





