<template>

<div

  class="project-card"

>


  <!-- Couleur projet -->

  <div

    class="color-line"

    :style="{
      backgroundColor: project.color || '#6366F1'
    }"

  ></div>





  <div class="p-5">


    <!-- Header -->


    <div class="flex justify-between items-start gap-3">


      <div class="flex items-center gap-3">


        <div class="project-icon">

          {{ project.icon || "📁" }}

        </div>



        <div>


          <h3 class="project-title">

            {{ project.name }}

          </h3>



          <p class="text-slate-400 text-sm mt-1">

            {{ project.description || "Aucune description" }}

          </p>


        </div>


      </div>





      <span

        v-if="project.is_favorite"

        class="favorite"

      >

        ⭐

      </span>


    </div>







    <!-- Infos -->


    <div class="project-info">


      <span>

        📌 {{ project.tasks_count || 0 }} tâche(s)

      </span>


      <span>

        {{ formatDate(project.created_at) }}

      </span>


    </div>







    <!-- Bouton -->


    <button

      @click="$emit('open', project.id)"

      class="open-project"

    >

      Ouvrir le projet →

    </button>



  </div>


</div>


</template>





<script setup>


defineProps({

project:{

type:Object,

required:true

}

});



defineEmits([

"open"

]);





const formatDate=(date)=>{


if(!date)
return "";


return new Date(date)

.toLocaleDateString("fr-FR");


};


</script>







