<template>
    <button class="back-button" @click="goBack">← Back</button>
    <form @submit.prevent="handleSubmit" class="profile-form">
      <div>
        <label>Description:</label>
        <input v-model="form.description" type="text" maxlength="200" required />
      </div>
  
      <div>
        <label>Parish:</label>
        <input v-model="form.parish" type="text" required />
      </div>
  
      <div>
        <label>Biography:</label>
        <textarea v-model="form.biography" maxlength="1000" required></textarea>
      </div>
  
      <div>
        <label>Sex:</label>
        <select v-model="form.sex" required>
          <option disabled value="">Select</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
        </select>
      </div>
  
      <div>
        <label>Race:</label>
        <select v-model="form.race" required>
          <option disabled value="">Select</option>
          <option value="White">White</option>
          <option value="Black">Black</option>
          <option value="Hispanic">Hispanic</option>
          <option value="Asian">Asian</option>
          <option value="Other">Other</option>
        </select>
      </div>
  
      <div>
        <label>Birth Year:</label>
        <input v-model.number="form.birth_year" type="number" min="1900" max="2025" required />
      </div>
  
      <div>
        <label>Height (cm):</label>
        <input v-model.number="form.height" type="number" min="100" max="250" step="0.1" required />
      </div>
  
      <div>
        <label>Favorite Cuisine:</label>
        <input v-model="form.fav_cuisine" type="text" required />
      </div>
  
      <div>
        <label>Favorite Color:</label>
        <input v-model="form.fav_colour" type="text" required />
      </div>
  
      <div>
        <label>Favorite School Subject:</label>
        <input v-model="form.fav_school_subject" type="text" required />
      </div>
  
      <div>
        <label><input type="checkbox" v-model="form.political" /> Political</label>
      </div>
  
      <div>
        <label><input type="checkbox" v-model="form.religious" /> Religious</label>
      </div>
  
      <div>
        <label><input type="checkbox" v-model="form.family_oriented" /> Family Oriented</label>
      </div>
  
      <button type="submit">Save Profile</button>
    </form>
  </template>
  
<script setup>
    import { ref } from 'vue'
    import axios from 'axios'

    const form = ref({
        description: '',
        parish: '',
        biography: '',
        sex: '',
        race: '',
        birth_year: null,
        height: null,
        fav_cuisine: '',
        fav_colour: '',
        fav_school_subject: '',
        political: false,
        religious: false,
        family_oriented: false
    })
  
    
    const handleSubmit = async () => {
        try {
            const csrfResponse = await axios.get('/api/v1/csrf-token', {
                withCredentials: true, 
            });
            const csrfToken = csrfResponse.data.csrf_token;

            const response = await axios.post('/api/profiles', form.value, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                withCredentials: true, 
            });

            console.log('Profile saved:', response.data); 

            alert('Profile saved successfully');
            
            setTimeout(() => {
                const userId = sessionStorage.getItem('user_id');
                if (userId) {
                    window.location.href = `/users/${userId}`;
                } else {
                    alert('User ID not found in session.');
                }
            }, 1000);

        } catch (error) {
            if (error.response && error.response.status === 403) {
                alert(error.response.data.message)
                const userId = sessionStorage.getItem('user_id')
            if (userId) {
                window.location.href = `/users/${userId}`
            }
            } else {
                console.error('Error saving profile:', error)
                alert('An error occurred while saving the profile.')
            }
        }
    };
    
    function goBack() {
        window.history.length > 1 ? window.history.back() : window.location.href = '/';
    }
    
</script>
  
<style scoped>
    .profile-form {
        max-width: 600px;
        margin: auto;
        display: grid;
        gap: 1rem;
    }
    .profile-form {
        max-width: 600px;
        margin: 2rem auto;
        padding: 2rem;
        background-color: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

    .profile-form div {
        margin-bottom: 1.25rem;
    }

    .profile-form label {
        display: block;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: #333;
    }

    .profile-form input[type="text"],
    .profile-form input[type="number"],
    .profile-form select,
    .profile-form textarea {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid #ccc;
        border-radius: 8px;
        font-size: 1rem;
        box-sizing: border-box;
    }

    .profile-form textarea {
        resize: vertical;
        min-height: 100px;
    }

    .profile-form input[type="checkbox"] {
        margin-right: 0.5rem;
        transform: scale(1.1);
    }

    .profile-form button[type="submit"] {
        display: block;
        width: 100%;
        padding: 0.75rem;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .profile-form button[type="submit"]:hover {
        background-color: #0056b3;
    }

    

    
</style>
