<template>
    <button class="back-button" @click="goBack">← Back</button>
    <div class="profiles-container">
      <h1>All Profiles</h1>
      <div v-if="profiles.length">
        <div
          v-for="profile in profiles"
          :key="profile.user_id_fk"
          class="profile-card"
        >
            <!-- Display the user's photo -->
            <img
                v-if="user.photo"  
                :src="getPhotoUrl(user.photo)" 
                alt="User's Profile Photo"
                class="profile-photo"
            />
            <h2>Profile ID: {{ profile.id }}</h2>
            <p><strong>User ID:</strong> {{ profile.user_id_fk }}</p>
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
            <button @click="addToFavourites(profile.user_id_fk)">Add to Favourites</button>
        </div>
      </div>
      <div v-else>
        <p>Loading or no profiles found...</p>
      </div>
    </div>
  </template>
  
<script setup>
    import { onMounted, ref } from 'vue'
    import axios from 'axios'
    
    const profiles = ref([])
    const user = ref([])

    const currentUserId = sessionStorage.getItem('user_id')
    const userId = profiles.user_id_fk
    
    // Function to fetch the user data for a given user_id
    const fetchUser = async (user_id_fk) => {
        try {
            const response = await axios.get(`/api/users/${user_id_fk}`)  // Fetch user data using user_id_fk
            user.value = response.data  // Attach the user data to the 'user' object
        } catch (error) {
            console.error('Error fetching user data:', error)
        }
    }

    onMounted(async () => {
        try {
            const response = await axios.get('/api/profiles')  // Fetch profiles from the backend
            profiles.value = response.data;
            
            // After fetching profiles, fetch user data for each profile's user_id_fk
            for (let profile of profiles.value) {
                console.log("pr id:",profile.user_id_fk)
                await fetchUser(profile.user_id_fk);
            }
        } catch (error) {
            console.error('Error fetching profiles:', error);
        }
    });


    const getPhotoUrl = (filename) => {
        console.log(`pic_uploads/${filename}`)
        return `/pic_uploads/${filename}`
    }

    const getCsrfToken = async () => {
            try {
                const response = await axios.get('/api/v1/csrf-token');  // Fetch CSRF token
                return response.data.csrf_token;  // Return the token
            } catch (error) {
                console.error('Error fetching CSRF token:', error);
                return '';  // In case of failure, return an empty string or handle the error as needed
            }
    }
  
    const addToFavourites = async (favUserId) => {
        try {
            const csrfToken = await getCsrfToken();  // Fetch the CSRF token

            // Make sure csrfToken is available
            if (csrfToken) {
                // Send an empty object {} as the body in the request
                const response = await axios.post(`/api/profiles/${favUserId}/favourite`, {}, {
                    headers: {
                        'X-CSRFToken': csrfToken,  // Send CSRF token in the headers
                        'Content-Type': 'application/json',  // Explicitly setting content type
                    },
                });

                // Check the response from the backend
                if (response.data.message === 'Profile already in favourites') {
                    alert('This profile is already in your favourites.');
                } else {
                    alert('Added to favourites!');
                }
            } else {
                alert('Failed to retrieve CSRF token.');
            }
        } catch (error) {
            console.error('Error adding to favourites:', error);
            alert('Failed to add to favourites.');
        }
    };

    function goBack() {
        window.history.length > 1 ? window.history.back() : window.location.href = '/';
    }

</script>
  
<style>
    .profiles-container {
        padding: 20px;
    }
    
    .profile-card {
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 16px;
        background-color: #f9f9f9;
    }
    button {
        margin-top: 10px;
        padding: 8px 12px;
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
    }
    button:hover {
        background-color: #0056b3;
    }

    .profile-photo {
    width: 120px;
    height: 120px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
        }
</style>