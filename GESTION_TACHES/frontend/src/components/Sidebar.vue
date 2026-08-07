<template>

  
  <aside 
    class="sidebar"
    :class="{open: props.open}"
    @click="emit('close')"
  >
    <!-- LOGO -->

    <div class="brand">

  <h1>
    NOVA TASKS
  </h1>

  <p>
    Organisez votre quotidien
  </p>

  <span class="brand-signature">
    by Clever
  </span>

  </div>



    <!-- NAVIGATION -->

    <nav class="menu">


      <RouterLink
        to="/dashboard"
        class="menu-item"
      >
        <span class="icon">📊</span>
        <span>Tableau de bord</span>
      </RouterLink>


      <RouterLink
        to="/kanban"
        class="menu-item"
      >
        <span class="icon">📋</span>
        <span>Gestion tâches</span>
      </RouterLink>
      


      <RouterLink
        to="/calendar"
        class="menu-item"
      >
        <span class="icon">📅</span>
        <span>Calendrier</span>
      </RouterLink>



      <RouterLink
        to="/statistics"
        class="menu-item"
      >
        <span class="icon">📈</span>
        <span>Statistiques</span>
      </RouterLink>



      <RouterLink
        to="/archives"
        class="menu-item"
      >
        <span class="icon">📦</span>
        <span>Archives</span>
      </RouterLink>


    </nav>



    <!-- PROFIL -->

    <div class="profile">


      <div class="avatar">

        {{ initial }}

      </div>



      <div class="user-info">

        <p class="username">
          {{ username }}
        </p>


        <p class="status">

          <span></span>
          Connecté

        </p>


      </div>


    </div>


  </aside>


</template>



<script setup>
const props = defineProps({

open:{
    type:Boolean,
    default:false
}

});
import { computed } from "vue";


const username =
localStorage.getItem("username")
|| "Utilisateur";



const initial = computed(() => {

  return username
    .charAt(0)
    .toUpperCase();

});

const emit = defineEmits([
    "close"
]);
</script>



<style scoped>


.sidebar {

  width: 280px;

  height: 100vh;

  position: sticky;

  top: 0;


  background:

  linear-gradient(
    180deg,
    #111827,
    #1e1b4b,
    #020617
  );


  border-right: 1px solid rgba(148,163,184,.15);


  display:flex;

  flex-direction:column;


  padding:28px;


}



/* BRAND */


.brand h1 {

  color:white;

  font-size:26px;

  font-weight:900;

  letter-spacing:1px;


}


.brand p {

  margin-top:8px;

  color:#94a3b8;

  font-size:14px;

}



/* MENU */


.menu {

  margin-top:45px;

  display:flex;

  flex-direction:column;

  gap:12px;

  flex:1;

}



.menu-item {


  display:flex;

  align-items:center;

  gap:15px;


  padding:15px 18px;


  border-radius:18px;


  color:#cbd5e1;


  text-decoration:none;


  font-weight:600;


  transition:.3s;


}



.menu-item:hover {


  background:

  rgba(99,102,241,.18);


  color:white;


  transform:translateX(6px);


}



/* PAGE ACTIVE */


.router-link-active {


  background:

  linear-gradient(
    90deg,
    rgba(59,130,246,.45),
    rgba(139,92,246,.35)
  );


  color:white;


  box-shadow:

  0 10px 30px rgba(59,130,246,.15);


}



.icon {

  font-size:20px;

}



/* PROFIL */


.profile {


  display:flex;

  align-items:center;

  gap:14px;


  padding-top:20px;


  border-top:

  1px solid rgba(148,163,184,.15);


}



.avatar {


  width:48px;

  height:48px;


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

  font-size:18px;


}



.username {

  color:white;

  font-weight:700;

}



.status {


  display:flex;

  align-items:center;

  gap:6px;


  color:#22c55e;

  font-size:13px;


}



.status span {


  width:8px;

  height:8px;


  border-radius:50%;


  background:#22c55e;


}

@media (min-width:769px) and (max-width:900px){

  .sidebar{

  width:280px;

  position:fixed;

  left:-300px;

  top:0;

  z-index:1000;

  transition:.3s;

}

.sidebar.open{

  left:0;

}

.brand p,
.brand-signature,
.menu-item span,
.user-info{

  display:block;

}

.menu-item{

  justify-content:flex-start;

}



}

@media(max-width:768px){


.sidebar{

position:fixed;

left:-300px;

top:0;

z-index:1000;

transition:.3s;

}


.sidebar.open{

left:0;

}



}
.brand-signature {

  display:block;

  margin-top:6px;

  color:#2180ed;

  font-size:15px;

  font-weight:900;

  letter-spacing:1px;

}
</style>

