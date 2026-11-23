<template>

<div class="project-detail">


  <!-- Retour -->

  <button
    @click="$router.back()"
    class="back-button"
  >

    ← Retour aux projets

  </button>





  <!-- Chargement -->

  <div
    v-if="loading"
    class="loading"
  >

    Chargement du projet...

  </div>





  <!-- Projet -->

  <div
    v-else-if="project"
    class="project-container"
  >



    <!-- Header -->

    <div class="flex justify-between items-start">


      <div>


        <div class="flex items-center gap-4">


          <div class="icon">

            {{ project.icon || "📁" }}

          </div>




          <div>


            <h1 class="title">

              {{ project.name }}

            </h1>



            <p class="description">

              {{ project.description || "Aucune description" }}

            </p>


          </div>


        </div>


      </div>




      <span
        v-if="project.is_favorite"
        class="favorite"
      >

        ⭐ Favori

      </span>



    </div>







    <!-- Informations -->


    <div class="stats">


      <div class="stat-card">

        <span>

          📌

        </span>

        <p>

          {{ tasks.length }}

        </p>

        <small>

          Tâches

        </small>

      </div>





      <div class="stat-card">

        <span>

          ✅

        </span>

        <p>

          {{ completed }}

        </p>

        <small>

          Terminées

        </small>

      </div>






      <div class="stat-card">

        <span>

          🚀

        </span>

        <p>

          {{ progress }}%

        </p>

        <small>

          Progression

        </small>

      </div>



    </div>








    <!-- Liste tâches -->


    <div class="tasks-box">


      <h2>

        Tâches du projet

      </h2>



      <div
        v-if="tasks.length"
        class="space-y-3 mt-5"
      >


        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-item"
        >


          <span>

            {{ task.title }}

          </span>



          <span class="status">

            {{ task.status }}

          </span>



        </div>


      </div>



      <p
        v-else
        class="empty"
      >

        Aucune tâche dans ce projet.

      </p>



    </div>




  </div>


</div>


</template>







<script setup>


import {
ref,
computed,
onMounted
} from "vue";


import {useRoute} from "vue-router";


import api from "../services/api";





const route = useRoute();




const project = ref(null);

const tasks = ref([]);

const loading = ref(true);







const loadProject = async()=>{


try{


const response = await api.get(

`projects/${route.params.id}/`

);



project.value=response.data;





if(project.value.tasks){

tasks.value=project.value.tasks;

}



}

catch(error){


console.error(error);


}

finally{


loading.value=false;


}


};








const completed = computed(()=>{


return tasks.value.filter(

task=>task.status==="done"

).length;


});







const progress = computed(()=>{


if(tasks.value.length===0)

return 0;



return Math.round(

(completed.value / tasks.value.length)

*100

);


});







onMounted(()=>{


loadProject();


});


</script>







