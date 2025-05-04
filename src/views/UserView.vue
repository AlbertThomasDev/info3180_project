<template>
    <div class="action-buttons">
      <button @click="createProfile" class="btn-create-profile">Create Profile</button>
      <button @click="viewProfiles" class="btn-view-profiles">View Profile</button>
      <button @click="viewReport" class="btn-report">View Report</button>
      <button @click="logout" class="btn-logout">Log Out</button>
    </div>
    <div class="user-view">
        <img :src="getPhotoUrl(user.photo)" alt="User Photo" class="user-photo" v-if="user.photo" />
        <h1>{{ user.name }}'s Profile</h1>
        <!-- <p><strong>Email:</strong> {{ user.email }}</p> -->
        <p><strong>Joined:</strong> {{ new Date(user.date_joined).toLocaleDateString() }}</p>
    
    </div>


    
  </template>
  
<script setup>
    import axios from 'axios'
    import { onMounted, ref } from 'vue'
    import { useRouter, useRoute } from 'vue-router'
    

    const user = ref({})
    const router = useRouter()
    
    const route = useRoute()
    const userId = route.params.userId
    console.log(userId);


    const createProfile = () => {
        router.push('/profiles/new')
    }

    const getPhotoUrl = (filename) => {
        console.log(`pic_uploads/${filename}`)
        return `/pic_uploads/${filename}` 
    }

    // Fetch user data on component mount
    onMounted(async () => {
        try {
            const response = await axios.get(`/api/users/${userId}`)  // Fetching user data based on dynamic userId
            user.value = response.data
        } catch (err) {
            console.error('Failed to fetch user:', err)
        }
    })

    const viewProfiles = () => {
        router.push("/profiles/" + userId) // Navigate to profile details view
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