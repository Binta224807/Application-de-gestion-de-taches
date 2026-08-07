<template>

  <div
    class="bg-slate-900 rounded-3xl p-6 border border-slate-700 shadow-xl"
  >

    <h2 class="text-xl font-bold text-white mb-5">
      ⏰ Échéances
    </h2>



    <div
      v-if="deadlines.length"
      class="space-y-4"
    >


      <div

        v-for="task in deadlines"

        :key="task.id"

        class="flex justify-between items-center bg-slate-800 rounded-xl p-4"

      >


        <div>


          <h3 class="text-white font-medium">

            {{ task.title }}

          </h3>



          <p class="text-slate-400 text-sm">

            {{ task.due_date }}

          </p>


        </div>




        <span
          class="text-indigo-400 text-sm"
        >

          {{ task.priority }}

        </span>


      </div>


    </div>



    <p
      v-else
      class="text-slate-400 text-center py-5"
    >

      Aucune échéance.

    </p>


  </div>


</template>



<script setup>


defineProps({

deadlines:{

type:Array,

default:()=>[]

}

});


</script>