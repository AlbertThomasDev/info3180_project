<template>
  <div class="register-page">
    <div class="register-container">
      <h1 class="logo">Jam-Date</h1>
      <h2>Register</h2>
      <form id="reg_form" @submit.prevent="register_user">
        <input type="text" name="username" v-model="username" placeholder="Username" required />
        <input type="password" name="password" v-model="password" placeholder="Password" required />
        <input type="text" name="name" v-model="name" placeholder="Full Name" required />
        <input type="email" name="email" v-model="email" placeholder="Email" required />
        <input type="file" name="photo" @change="onFileChange" required />
        <button type="submit">Register</button>
      </form>

      <p v-if="message" :style="{ color: error ? 'red' : 'green' }">{{ message }}</p>
    </div>
  </div>
</template>

<script setup>
  
  
  const name = ref('');
  const username = ref('');
  const password = ref('');
  const email = ref('');
  const photo = ref(null);
  const message = ref('');
  const errors = ref([]);
  const csrf_token = ref('');
  const csrfStatus = ref('');
  
  import { ref, onMounted } from 'vue';
  
  function getCsrfToken() {
    fetch('/api/v1/csrf-token')
      .then((response) => {
        if (!response.ok) {
          csrfStatus.value = `Error: Server returned ${response.status}`;
          throw new Error(`Server error: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('CSRF token received:', data);
        csrf_token.value = data.csrf_token;
        csrfStatus.value = 'CSRF Token Received';
      })
      .catch(error => {
        // console.error('Error:', error);
        csrfStatus.value = `Error: ${error.message}`;
      });
  }
  
  onMounted(() => {
    getCsrfToken();
  });
  
  const onFileChange = (event) => {
    photo.value = event.target.files[0];
  };
  
  const register_user = async () => {
    // Clear previous messages/errors
    message.value = '';
    errors.value = [];
    
    // Prepare form data for submission
    let form_data = new FormData();
    form_data.append('name', name.value);
    form_data.append('username', username.value);
    form_data.append('password', password.value);
    form_data.append('email', email.value);
    form_data.append('photo', photo.value);
    
    try {
      message.value = 'Submitting registration...';
      console.log('CSRF Token used:', csrf_token.value);
      
      const response = await fetch('/api/register', {
        method: 'POST',
        body: form_data,
        headers: {
          'X-CSRFToken': csrf_token.value
        }
      });
      
      const data = await response.json();
      console.log('Registration response:', data);
      
      if (response.ok) {
        message.value = data.message || 'Registration successful!';
        errors.value = [];
        
        // Reset form fields after successful registration
        name.value = '';
        username.value = '';
        password.value = '';
        email.value = '';
        photo.value = null;
        
        //Redirect to login page
        setTimeout(() => window.location.href = '/login', 2000);
      } else {
        errors.value = data.errors || [data.message || 'Registration failed. Please try again.'];
      }
    } catch (error) {
      console.error('Error:', error);
      errors.value = ['An error occurred during registration. Please try again later.'];
    }
  };
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background-image: url('@/assets/Registration.jpeg'); 
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-container {
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

form input[type="file"] {
  padding: 10px;
  background-color: white;
}

button {
  padding: 12px;
  width: 100%;
  background-color:rgb(132, 209, 245);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s ease;
}

button:hover {
  background-color:rgb(132, 209, 245);
}

p {
  margin-top: 15px;
  color: red;
  font-weight: bold;
}
</style>






