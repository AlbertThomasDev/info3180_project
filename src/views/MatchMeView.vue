<template>
    <div class="container">
      <button class="back-button" @click="goBack">← Back</button>
      <h1>Matched Profiles</h1>
  
      <div v-if="matches.length" class="profile-list">
        <div v-for="profile in matches" :key="profile.id" class="profile-card">
          <h3>Profile ID: {{ profile.id }}</h3>
          <p><strong>Description:</strong> {{ profile.description }}</p>
          <p><strong>Parish:</strong> {{ profile.parish }}</p>
          <p><strong>Birth Year:</strong> {{ profile.birth_year }}</p>
          <p><strong>Height:</strong> {{ profile.height }} m</p>
          <p><strong>Favourite Cuisine:</strong> {{ profile.fav_cuisine }}</p>
          <p><strong>Favourite Colour:</strong> {{ profile.fav_colour }}</p>
          <p><strong>School Subject:</strong> {{ profile.fav_school_subject }}</p>
        </div>
      </div>
  
      <div v-else-if="error">
        <p class="error">{{ error }}</p>
      </div>
  
      <div v-else>
        <p>Loading matches...</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name: 'MatchView',
    data() {
      return {
        matches: [],
        error: null,
      };
    },
    async created() {
      const profileId = sessionStorage.getItem('profile_id');
      if (!profileId) {
        this.error = 'No profile selected for matching.';
        return;
      }
  
      try {
        const response = await axios.get(`/api/profiles/matches/${profileId}`);
        this.matches = response.data;
      } catch (err) {
        this.error = err.response?.data?.error || 'Error fetching matched profiles';
      }
    },
    methods: {
      goBack() {
        window.history.length > 1 ? window.history.back() : (window.location.href = '/');
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    padding: 2rem;
  }
  .profile-list {
    display: grid;
    gap: 1.5rem;
  }
  .profile-card {
    background: #fff;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  .error {
    color: red;
    margin-top: 1rem;
  }
  </style>
  