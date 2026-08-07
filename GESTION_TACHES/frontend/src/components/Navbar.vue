<template>

<header class="navbar">

  <button
    class="mobile-menu"
    @click="$emit('toggleMenu')"
    >
    ☰
    </button>
  <!-- RECHERCHE -->

  <div class="search-container">

    <div class="search-box">

      <span class="search-icon">
        🔍
      </span>

      <input

          
        
          v-model="search"
          @input="updateSearch(search)"
          type="text"
          placeholder="Rechercher..."
          class="
          w-full
          bg-slate-900
          border
          border-slate-700
          rounded-2xl
          px-5
          py-3
          text-white
          outline-none
          focus:border-indigo-500
          transition
          "

/>


    </div>

  </div>



  <!-- PROFIL -->

  <div class="right-section">


    <div class="profile">


      <div class="avatar">

        {{ usernameInitial }}

      </div>



      <div class="user-info">

        <p class="username">
          {{ username }}
        </p>


        <p class="status">

          <span></span>

          En ligne

        </p>


      </div>


    </div>



    <!-- DECONNEXION -->

    <button

      v-if="isAuthenticated"

      class="logout-btn"

      @click="logout"

    >

      Se déconnecter

    </button>



    <RouterLink

      v-else

      to="/login"

      class="login-btn"

    >

      Connexion

    </RouterLink>


  </div>


</header>


</template>



<script setup>

import { ref, computed } from "vue";
import { useSearch } from "../components/useSearch";
import { useRouter } from "vue-router";


const { updateSearch } = useSearch();
const router = useRouter();


const search = ref("");





const username =

localStorage.getItem("username")

|| "Utilisateur";



const isAuthenticated = computed(()=>{

return localStorage.getItem("access") || localStorage.getItem("access_token")!== null;

});




const usernameInitial = computed(()=>{

return username

.charAt(0)

.toUpperCase();

});





const logout = ()=>{


localStorage.removeItem(
"access"
);
localStorage.removeItem(
"refresh"
);

localStorage.removeItem(
"access_token"
);
localStorage.removeItem(
"refresh_token"
);

localStorage.removeItem(
"username"
);



router.push("/login");


};

defineEmits([
    "toggleMenu"
]);

</script>



<style scoped>


.navbar {


height:80px;


background:

linear-gradient(
90deg,
#020617,
#111827
);


border-bottom:

1px solid rgba(148,163,184,.15);



display:flex;


align-items:center;


justify-content:space-between;


padding:0 32px;


}



/* SEARCH */


.search-container {

flex:1;

max-width:600px;


}



.search-box {


display:flex;


align-items:center;


gap:12px;


background:

rgba(15,23,42,.8);



border:

1px solid rgba(148,163,184,.2);



padding:12px 18px;



border-radius:18px;



transition:.3s;


}



.search-box:focus-within {


border-color:#6366f1;


box-shadow:

0 0 20px rgba(99,102,241,.25);


}



.search-box input {


width:100%;


background:transparent;


border:none;


outline:none;


color:white;


font-size:15px;


}



.search-box input::placeholder {


color:#94a3b8;


}


.search-icon {


font-size:18px;


}



/* RIGHT */


.right-section {


display:flex;


align-items:center;


gap:25px;


}



.profile {


display:flex;


align-items:center;


gap:12px;


}



.avatar {


width:45px;


height:45px;


border-radius:50%;



display:flex;


align-items:center;


justify-content:center;



background:

linear-gradient(
135deg,
#2563eb,
#9333ea
);



color:white;


font-weight:900;


}



.username {


color:white;


font-weight:700;


margin:0;


}



.status {


display:flex;


align-items:center;


gap:6px;



font-size:12px;


color:#22c55e;


}



.status span {


width:8px;


height:8px;


border-radius:50%;


background:#22c55e;


}



/* BUTTONS */


.logout-btn,

.login-btn {


padding:10px 18px;


border-radius:14px;


font-weight:700;


border:none;


cursor:pointer;


text-decoration:none;


transition:.3s;


}



.logout-btn {


background:

linear-gradient(
135deg,
#ef4444,
#dc2626
);



color:white;


}



.logout-btn:hover {


transform:translateY(-2px);


box-shadow:

0 10px 25px rgba(239,68,68,.3);


}



.login-btn {


background:

linear-gradient(
135deg,
#2563eb,
#7c3aed
);



color:white;


}



@media(max-width:900px){


.navbar {


padding:0 15px;


}



.search-container {


max-width:300px;


}



.user-info {


display:none;


}


.logout-btn {


padding:8px 12px;


font-size:12px;


}


}

.mobile-menu{

display:none;

font-size:26px;

color:white;

background:none;

border:none;

cursor:pointer;

}


@media(max-width:768px){

.mobile-menu{

display:block;

}

}

</style>