<template>
    <div class="container">
        <button class="back-button" @click="goBack">← Back</button>
        <div v-if="profiles.length" class="profile-grid">
            <div v-for="profile in profiles" :key="profile.id" class="profile-box">
            <h2 class="profile-title">Profile ID: {{ profile.id }}</h2>
            <p><strong>Description:</strong> {{ profile.description }}</p>
            <p><strong>Parish:</strong> {{ profile.parish }}</p>
            <p><strong>Biography:</strong> {{ profile.biography }}</p>
            <p><strong>Sex:</strong> {{ profile.sex }}</p>
            <p><strong>Race:</strong> {{ profile.race }}</p>
            <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
            <p><strong>Height:</strong> {{ profile.height }} m</p>
            <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
            <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
            <p><strong>Favourite School Subject:</strong> {{ profile.fav_school_subject }}</p>
            <p><strong>Political:</strong> {{ profile.political ? 'Yes' : 'No' }}</p>
            <p><strong>Religious:</strong> {{ profile.religious ? 'Yes' : 'No' }}</p>
            <p><strong>Family Oriented:</strong> {{ profile.family_oriented ? 'Yes' : 'No' }}</p>
            </div>
        </div>
  
      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
      </div>
  
      <div v-else class="loading-message">
        <p>Loading profiles...</p>
      </div>
    </div>
  </template>
  
<script>
    import axios from 'axios';
    const userId = sessionStorage.getItem('user_id');
    // const response = await axios.get(`/api/profiles/${userId}`);

    export default {
        name: 'ProfileDetailsView',
        data() {
        return {
            profiles: [],
            error: null,
        };
        },
        async created() {
        try {
            const response = await axios.get(`/api/profiles/${userId}`);
            this.profiles = response.data;
        } catch (err) {
            this.error = err.response?.data?.error || 'Error fetching profiles';
        }
        },
        methods: {
            goBack() {
                this.$router.back();
            },
        }
    };
</script>

<style scoped>
.container {
  padding: 2rem;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.profile-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.profile-box {
  background-color: white;
  padding: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  transition: box-shadow 0.3s ease;
}

.profile-box:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.profile-title {
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #2c3e50;
}

.error-message {
  color: red;
  text-align: center;
  margin-top: 2rem;
}

.loading-message {
  color: #555;
  text-align: center;
  margin-top: 2rem;
}
</style>
  
