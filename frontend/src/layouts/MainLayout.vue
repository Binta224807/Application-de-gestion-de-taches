<template>

<div class="app-layout">


    <Sidebar 
        :open="sidebarOpen"
        @close="closeSidebar"
    />



    <Transition name="overlay-fade">
        <div
            v-if="sidebarOpen"
            class="sidebar-overlay"
            @click="closeSidebar"
        />
    </Transition>

    <Starfield />

    <div class="ambient-glow glow-left"></div>
    <div class="ambient-glow glow-right"></div>

    <div class="main-content">


        <Navbar 
            @toggleMenu="toggleSidebar"
            @search="handleSearch"
        />


        <main class="page-container">

            <RouterView v-slot="{ Component, route }">

                <Transition
                    name="page"
                    mode="out-in"
                >

                    <component
                        :is="Component"
                        :key="route.path"
                    />

                </Transition>

            </RouterView>

        </main>


    </div>


</div>

</template>



<script setup>

import { ref, watch } from "vue";

import Sidebar from "../components/Sidebar.vue";
import Starfield from '../components/Starfield.vue';
import Navbar from "../components/Navbar.vue";


const sidebarOpen = ref(false);

watch(sidebarOpen, (open) => {
    document.body.style.overflow = open ? "hidden" : "";
});


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

  background: var(--bg);

}


.glow-left {

  width: 460px;

  height: 460px;

  top: -160px;

  left: 22%;

  background: #2563eb;

}


.glow-right {

  width: 420px;

  height: 420px;

  bottom: -180px;

  right: -6%;

  background: #7c3aed;

  animation-delay: -9s;

}


.main-content {

  position: relative;

  z-index: 1;

}


.sidebar-overlay {

  display: none;

}


@media (max-width: 900px) {

  .sidebar-overlay {

    display: block;

    position: fixed;

    inset: 0;

    z-index: 990;

    background: rgba(2, 6, 23, .62);

    backdrop-filter: blur(3px);

    -webkit-backdrop-filter: blur(3px);

  }

}


.overlay-fade-enter-active,

.overlay-fade-leave-active {

  transition: opacity .25s ease;

}


.overlay-fade-enter-from,

.overlay-fade-leave-to {

  opacity: 0;

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