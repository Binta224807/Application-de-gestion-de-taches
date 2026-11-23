
<template>
  <div class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">

    <div class="bg-slate-900 rounded-2xl p-6 w-[400px] shadow-xl">

      <h2 class="text-xl font-bold text-white mb-4">
        📦 Archiver la tâche
      </h2>

      <p class="text-gray-300 mb-5">
        {{ task?.title }}
      </p>


      <div class="space-y-3">

        <label
          class="flex items-center gap-3 text-white cursor-pointer"
        >
          <input
            type="radio"
            value="7_days"
            v-model="duration"
          />

          Archiver pendant 7 jours
        </label>


        <label
          class="flex items-center gap-3 text-white cursor-pointer"
        >
          <input
            type="radio"
            value="15_days"
            v-model="duration"
          />

          Archiver pendant 15 jours
        </label>


        <label
          class="flex items-center gap-3 text-red-400 cursor-pointer"
        >
          <input
            type="radio"
            value="delete"
            v-model="duration"
          />

          Supprimer définitivement
        </label>

      </div>


      <div class="flex justify-end gap-3 mt-6">

        <button
          @click="$emit('close')"
          class="px-4 py-2 rounded-lg bg-gray-700 text-white"
        >
          Annuler
        </button>


        <button
          @click="confirmArchive"
          class="px-4 py-2 rounded-lg bg-blue-600 text-white"
        >
          Confirmer
        </button>

      </div>

    </div>

  </div>
</template>



<script setup>

import { ref } from "vue"


const props = defineProps({

  task: {
    type: Object,
    required: true
  }

})


const emit = defineEmits([

  "confirmArchive",
  "close"

])


const duration = ref("7_days")



const confirmArchive = () => {

  emit(
    "confirmArchive",
    {
      task: props.task,
      duration: duration.value
    }
  )

}

</script>


<style scoped>


.overlay{

    position:fixed;

    inset:0;

    display:flex;

    justify-content:center;

    align-items:center;

    background:rgba(0,0,0,.65);

    backdrop-filter:blur(8px);

    z-index:10000;

}



.modal{

    width:420px;

    background:#0f172a;

    border-radius:24px;

    padding:30px;

    border:1px solid rgba(255,255,255,.08);

    box-shadow:
    0 30px 70px rgba(0,0,0,.5);

}



.header{

    display:flex;

    justify-content:space-between;

    align-items:flex-start;

}



.header h2{

    color:white;

    margin:0;

    font-size:24px;

}



.header p{

    color:#94a3b8;

    margin-top:8px;

}



.close{

    background:#1e293b;

    border:none;

    color:white;

    width:35px;

    height:35px;

    border-radius:10px;

    cursor:pointer;

}



.task-preview{

    margin:25px 0;

    padding:18px;

    border-radius:16px;

    background:#172033;

}



.task-preview h3{

    color:#60a5fa;

    margin:0 0 8px;

}



.task-preview p{

    color:#94a3b8;

}



.options{

    display:flex;

    flex-direction:column;

    gap:12px;

}



.options button{

    padding:14px;

    border:none;

    border-radius:14px;

    background:#1e293b;

    color:white;

    cursor:pointer;

    font-weight:600;

    transition:.25s;

}



.options button:hover{

    background:#2563eb;

    transform:translateY(-2px);

}



.options .danger:hover{

    background:#dc2626;

}



.cancel{

    margin-top:20px;

    width:100%;

    padding:13px;

    border:none;

    border-radius:14px;

    background:#334155;

    color:white;

    cursor:pointer;

}



</style>