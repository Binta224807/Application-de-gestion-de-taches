<template>

<div class="app-layout">


    <Sidebar 
        :open="sidebarOpen"
        @close="closeSidebar"
    />



    <div class="main-content">


        <Navbar 
            @toggleMenu="toggleSidebar"
            @search="handleSearch"
        />


        <main class="page-container">

            <RouterView />

        </main>


    </div>


</div>

</template>



<script setup>

import { ref } from "vue";

import Sidebar from "../components/Sidebar.vue";
import Navbar from "../components/Navbar.vue";


const sidebarOpen = ref(false);


const toggleSidebar = () => {

    sidebarOpen.value = !sidebarOpen.value;

};


const closeSidebar = () => {

    sidebarOpen.value = false;

};

const searchQuery = ref("");


const handleSearch = (value) => {

    searchQuery.value = value;

};

</script>



<style scoped>


.app-layout {

  min-height:100vh;

  display:flex;

  background:#020617;

}



/* CONTENU PRINCIPAL */


.main-content {

  flex:1;

  display:flex;

  flex-direction:column;

  min-width:0;

}



/* ZONE DES PAGES */


.page-container {

  flex:1;

  padding:32px;

  overflow:auto;

}



/* TABLETTE */


@media(max-width:1100px){


.page-container {

  padding:20px;

}


}



/* MOBILE */


@media(max-width:768px){


.app-layout {

  display:block;

}



.sidebar-layout {


  width:80px;


}



.page-container {

  padding:15px;

}



}



</style>