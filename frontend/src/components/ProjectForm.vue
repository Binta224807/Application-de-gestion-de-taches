<template>

<div

  v-if="visible"

  class="project-form"


>


  <div class="flex items-center gap-3 mb-6">


    <div class="form-icon">

      📁

    </div>



    <div>

      <h2 class="text-xl font-bold text-white">

        Nouveau projet

      </h2>


      <p class="text-slate-400 text-sm">

        Organisez vos tâches par projet

      </p>


    </div>


  </div>






  <div class="space-y-5">



    <!-- Nom -->


    <div>

      <label>

        Nom du projet

      </label>


      <input

        v-model="form.name"

        type="text"

        placeholder="Ex: Application mobile"

        class="input"

      />


    </div>






    <!-- Description -->


    <div>

      <label>

        Description

      </label>


      <textarea

        v-model="form.description"

        rows="4"

        placeholder="Décrivez votre projet..."

        class="input resize-none"

      ></textarea>


    </div>







    <!-- Icône -->


    <div>


      <label>

        Icône

      </label>



      <input

        v-model="form.icon"

        type="text"

        placeholder="📁"

        class="input"

      />


    </div>







    <!-- Couleur -->


    <div>


      <label>

        Couleur du projet

      </label>


      <input

        v-model="form.color"

        type="color"

        class="color-picker"

      />


    </div>







    <!-- Bouton -->


    <button

      @click="submit"

      class="create-button"

    >

      🚀 Créer le projet

    </button>



  </div>


</div>


</template>







<script setup>


import { reactive } from "vue";



defineProps({

visible:{

type:Boolean,

default:false

}

});





const emit = defineEmits([

"create"

]);






const form = reactive({

name:"",

description:"",

icon:"📁",

color:"#6366F1"

});






const submit = ()=>{


if(!form.name.trim())
return;



emit(

"create",

{

...form

}

);



form.name="";

form.description="";

form.icon="📁";

form.color="#6366F1";


};



</script>








