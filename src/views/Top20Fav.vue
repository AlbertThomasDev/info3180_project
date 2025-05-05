<template>
    <button class="back-button" @click="goBack">← Back</button>

    <div class="container">
      <h1>Top Favourited Users</h1>
  
      <div v-if="loading" class="text-center">Loading...</div>
      <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
  
      <div v-else class="row">
        <div class="col-md-4 mb-4" v-for="user in users" :key="user.id">
          <div class="card h-100">
            <img
              :src="getPhotoUrl(user.photo)"
              class="card-img-top"
              alt="User Photo"
              style="object-fit: cover; height: 200px;"
            />
            <div class="card-body">
              <h5 class="card-title">{{ user.name }}</h5>
              <p class="card-text">Favourited {{ user.favourites_count }} times</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
    import { ref, onMounted } from 'vue'
    import { useRouter } from 'vue-router'
    import axios from 'axios'
    
    const users = ref([])
    const loading = ref(true)
    const error = ref(null)
    const router = useRouter()
    
    const getPhotoUrl = (filename) => {
        return filename ? `/pic_uploads/${filename}` : '/default-profile.png'
    }
    
    const viewUserProfile = (userId) => {
        router.push(`/profiles/${userId}`)
    }
    
    onMounted(async () => {
        try {
        const response = await axios.get('/api/users/favourites/20')
        users.value = response.data
        } catch (err) {
        error.value = err.response?.data?.error || 'Failed to load top favourites'
        } finally {
        loading.value = false
        }
    })

    function goBack() {
        window.history.length > 1 ? window.history.back() : window.location.href = '/';
    }

  </script>
  
  <style scoped>
  .container {
    padding: 2rem;
  }
  </style>
  