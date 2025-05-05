<template>
    <div class="action-buttons">
      <button @click="createProfile" class="btn-create-profile">Create Profile</button>
      <button @click="viewProfiles" class="btn-view-profiles">My Profiles</button>
      <button @click="viewAllProfiles" class="btn-view-profiles">All Profiles</button>
      <button @click="viewReport" class="btn-report">View Report</button>
      <button @click="logout" class="btn-logout">Log Out</button>
    </div>
    <div class="user-view">
        <img :src="getPhotoUrl(user.photo)" alt="User Photo" class="user-photo" v-if="user.photo" />
        <h1>{{ user.name }}'s Profile</h1>
        <!-- <p><strong>Email:</strong> {{ user.email }}</p> -->
        <p><strong>Joined:</strong> {{ new Date(user.date_joined).toLocaleDateString() }}</p>
    
    </div>
    
    <!-- Search Bar -->
    <div class="mb-4">
    <input
        v-model="searchQuery"
        type="text"
        class="form-control"
        placeholder="Search by name, birth year, sex, or race"
    />
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center my-5">
    <div class="spinner-border text-primary" role="status">
        <span class="sr-only">Loading...</span>
    </div>
    </div>

    <!-- Error Message -->
    <div v-else-if="error" class="alert alert-danger">
    {{ error }}
    </div>

    <!-- Profiles List -->
    <div v-else>
    <div class="row">
        <div
        class="col-md-4 mb-4"
        v-for="profile in filteredProfiles.slice(0, 4)"
        :key="profile.id"
        >
        <div class="card h-100">
            <img
            :src="getPhotoUrl(profile.user.photo)"
            class="card-img-top"
            alt="Profile Photo"
            style="object-fit: cover; height: 200px;"
            />
            <div class="card-body">
            <h5 class="card-title">{{ profile.user.name }}</h5>
            <p class="card-text">{{ profile.description?.slice(0, 100) }}...</p>
            <router-link
                :to="`/profiles/${profile.user_id_fk}`"
                class="btn btn-outline-primary btn-sm"
            >
                View Details
            </router-link>
            </div>
        </div>
        </div>
    </div>

    <div v-if="filteredProfiles.length === 0" class="text-muted">
        No profiles found.
    </div>
    </div>

</template>
  
<script setup>
    import axios from 'axios'
    import { onMounted, ref, computed } from 'vue'
    import { useRouter, useRoute } from 'vue-router'

    const user = ref({})
    const profiles = ref([])
    const searchQuery = ref('')
    const loading = ref(false)
    const error = ref('')
    const router = useRouter()
    const route = useRoute()
    const userId = route.params.userId

    const createProfile = () => {
            router.push('/profiles/new')
    }

    const viewProfiles = () => {
            router.push("/profiles/" + userId) // Navigate to profile details view
    }

    const viewAllProfiles = () => {
        router.push("/profiles") // Navigate to profile details view
    }

    // Method for logout
    const logout = async () => {
        try {
            // Get CSRF token from the backend
            const csrfResponse = await axios.get('/api/v1/csrf-token', {
                withCredentials: true,
            })
            const csrfToken = csrfResponse.data.csrf_token

            // Call logout with the token
            const response = await axios.post(
                '/api/auth/logout',
                {},
                {
                    headers: {
                        'X-CSRFToken': csrfToken,
                    },
                    withCredentials: true,
                }
            )

            console.log(response.data.message)

            // Clear local/session storage and redirect
            localStorage.removeItem('user_id')
            sessionStorage.removeItem('user_id')
            router.push('/login')
        } catch (error) {
            console.error('Logout failed:', error)
        }
    }

const getPhotoUrl = (filename) => {
    return `/pic_uploads/${filename}`
}

const fetchUser = async () => {
    try {
        const response = await axios.get(`/api/users/${userId}`)
        user.value = response.data
    } catch (err) {
        console.error('Failed to fetch user:', err)
    }
}

const fetchProfiles = async () => {
    try {
        loading.value = true
        const response = await axios.get('/api/search')
        profiles.value = response.data
    } catch (err) {
        console.error('Failed to fetch profiles:', err)
        error.value = 'Failed to load profiles.'
    } finally {
        loading.value = false
    }
}

const filteredProfiles = computed(() => {
    if (!searchQuery.value) return profiles.value
    const q = searchQuery.value.toLowerCase()
    return profiles.value.filter((p) =>
        (p.user?.name || '').toLowerCase().includes(q) ||
        (p.sex || '').toLowerCase().includes(q) ||
        (p.race || '').toLowerCase().includes(q) ||
        String(p.birth_year).includes(q)
    )
})

onMounted(() => {
    fetchUser()
    fetchProfiles()
})
</script>




<style scoped>
.user-photo {
  width: 150px;
  height: 150px;
  object-fit: cover;
  border-radius: 50%;
  margin-bottom: 1rem;
}

.action-buttons {
  margin-top: 20px;
}

.action-buttons button {
  padding: 10px 15px;
  margin: 5px;
  font-size: 16px;
  cursor: pointer;
  border: none;
  border-radius: 8px;
  background-color: #4CAF50;
  color: white;
  transition: background-color 0.3s ease;
}

/* .search-bar {
  margin: 20px 0;
  display: flex;
  justify-content: center;
}

.search-input {
  padding: 0.5rem;
  width: 100%;
  max-width: 400px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.search-input::placeholder {
  color: #aaa;
} */

.action-buttons button:hover {
  background-color: #45a049;
}

.btn-profile {
  background-color: #2196F3;
}

.btn-profile:hover {
  background-color: #0b7dda;
}

.btn-report {
  background-color: #ff9800;
}

.btn-report:hover {
  background-color: #e68900;
}

.btn-logout {
  background-color: #f44336;
}

.btn-logout:hover {
  background-color: #d32f2f;
}
</style>