<template>

  <MainLayout v-if="showLayout">
    <RouterView />
  </MainLayout>

  <RouterView v-else />

</template>


<script setup>

import { computed } from "vue";
import { useRoute } from "vue-router";
import MainLayout from "./Layouts/MainLayout.vue";


const route = useRoute();


const showLayout = computed(() => {

  return ![
    "/login",
    "/register"
  ].includes(route.path);

});

</script>