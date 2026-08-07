<script setup>
const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits([
  "editTask",
  "deleteTask",
  "archiveTask",
]);

const startDrag = (event) => {
  event.dataTransfer.effectAllowed = "move";
  event.dataTransfer.setData(
    "taskId",
    props.task.id
  );
};

const editTask = () => {
  emit("editTask", props.task);
};

const deleteTask = () => {
  emit("deleteTask", props.task);
};
</script>

<template>
  <div
    class="task-card"
    draggable="true"
    @dragstart="startDrag"
  >
    <div class="card-header">

  <h3>
    {{ task.title }}
  </h3>


  <span
    class="badge"
    :class="task.priority"
  >
  PRIORTY:
    {{ task.priority }}
  </span>

</div>

<p style="color:yellow">
  ID : {{ task.id }}
</p>



<p class="description">
  {{ task.description || "Aucune description" }}
</p>


<div class="card-infos">

  <span>
    📅DATE_LIM:
    {{ task.due_date || "Pas de date" }}
  </span>


  <span>
    📂PROJET:
    {{ task.project_name || "Sans projet" }}
  </span>


  <span>
    🏷️CAT:
    {{ task.category_name || "Sans catégorie" }}
  </span>


  <span>
    ⏱️DR:
    {{ task.estimated_duration }} min
  </span>


<span v-if="task.due_time">
    🕒TIME:
    {{ task.due_time }}
</span>

</div>

    <div class="actions">

      <button
        class="edit"
        @click="editTask"
      >
        ✏ Modifier
      </button>

      <button
        v-if="task.status === 'done'"
        class="archive"
        @click="emit('archiveTask', task)"
      >
        📦 Archiver
      </button>

      <button
        v-else
        class="delete"
        @click="deleteTask"
      >
        🗑 Supprimer
      </button>

    </div>
  </div>
</template>

<style scoped>

.task-card{

background:#111827;

border:1px solid rgba(255,255,255,.08);

border-radius:18px;

padding:18px;

display:flex;

flex-direction:column;

gap:14px;

cursor:grab;

transition:.25s;

box-shadow:0 6px 18px rgba(0,0,0,.25);

}

.task-card:hover{

transform:translateY(-5px);

border-color:#2563eb;

box-shadow:0 10px 25px rgba(37,99,235,.25);

}

.task-card:active{

cursor:grabbing;

}

.card-header{

display:flex;

justify-content:space-between;

align-items:flex-start;

gap:12px;

}

.card-header h3{

font-size:18px;

font-weight:700;

color:white;

margin:0;

}

.description{

color:#94a3b8;

font-size:14px;

line-height:1.6;

}

.card-infos{

display:flex;

flex-direction:column;

gap:6px;

font-size:13px;

color:#cbd5e1;

}

.badge{

padding:5px 12px;

border-radius:30px;

font-size:11px;

font-weight:bold;

text-transform:uppercase;

color:white;

}

.badge.low{

background:#22c55e;

}

.badge.medium{

background:#f59e0b;

}

.badge.high{

background:#ef4444;

}

.actions{

display:flex;

justify-content:space-between;

margin-top:8px;

gap:10px;

}

.actions button{

flex:1;

padding:10px;

border:none;

border-radius:12px;

font-weight:600;

cursor:pointer;

transition:.25s;

}

.edit{

background:#2563eb;

color:white;

}

.edit:hover{

background:#1d4ed8;

}

.delete{

background:#dc2626;

color:white;

}

.delete:hover{

background:#b91c1c;

}
.archive{

    background:#16a34a;

    color:white;

}

.archive:hover{

    background:#15803d;

}

</style>