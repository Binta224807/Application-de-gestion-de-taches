<template>

<button

@click="logout"

class="rounded-xl bg-red-600 px-4 py-2 text-white hover:bg-red-700 transition"

>

Déconnexion

</button>

</template>



<script setup>


import { useRouter } from "vue-router";


const router = useRouter();



const logout = ()=>{


localStorage.removeItem(
"access_token"
);


localStorage.removeItem(
"refresh_token"
);



router.push("/login");


};


</script>