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
  "moveTask",
]);


// ===============================
// DRAG & DROP PC
// ===============================

const startDrag = (event) => {

  event.dataTransfer.effectAllowed = "move";

  event.dataTransfer.setData(
    "taskId",
    props.task.id
  );

};


// ===============================
// ACTIONS
// ===============================

const editTask = () => {

  emit(
    "editTask",
    props.task
  );

};


const deleteTask = () => {

  emit(
    "deleteTask",
    props.task
  );

};


// ===============================
// DEPLACEMENT
// ===============================

const moveTask = (status) => {

  emit(
    "moveTask",
    {
      task: props.task,
      newStatus: status,
    }
  );

};

</script>


<template>

  <div
    class="task-card"
    draggable="true"
    @dragstart="startDrag"
  >

    <!-- ========================= -->
    <!-- HEADER -->
    <!-- ========================= -->

    <div class="card-header">

      <h3>
        {{ task.title }}
      </h3>


      <span
        class="badge"
        :class="task.priority"
      >

        PRIORITÉ :

        {{ task.priority }}

      </span>

    </div>


    <!-- ========================= -->
    <!-- ID -->
    <!-- ========================= -->

    <p class="task-id">

      ID : {{ task.id }}

    </p>


    <!-- ========================= -->
    <!-- DESCRIPTION -->
    <!-- ========================= -->

    <p class="description">

      {{ task.description || "Aucune description" }}

    </p>


    <!-- ========================= -->
    <!-- INFORMATIONS -->
    <!-- ========================= -->

    <div class="card-infos">

      <span>

        📅 DATE LIM :

        {{ task.due_date || "Pas de date" }}

      </span>


      <span>

        📂 PROJET :

        {{ task.project_name || "Sans projet" }}

      </span>


      <span>

        🏷️ CAT :

        {{ task.category_name || "Sans catégorie" }}

      </span>


      <span>

        ⏱️ DUR :

        {{ task.estimated_duration || 0 }} min

      </span>


      <span v-if="task.due_time">

        🕒 HEURE :

        {{ task.due_time }}

      </span>

    </div>


    <!-- ========================= -->
    <!-- DEPLACEMENT -->
    <!-- ========================= -->

    <div class="move-buttons">


      <!-- TODO -->

      <button
        v-if="task.status !== 'todo'"
        class="move-btn move-back"
        @click="moveTask('todo')"
      >

        ← À faire

      </button>


      <!-- IN PROGRESS -->

      <button
        v-if="task.status !== 'in_progress'"
        class="move-btn move-progress"
        @click="moveTask('in_progress')"
      >

        → En cours

      </button>


      <!-- DONE -->

      <button
        v-if="task.status !== 'done'"
        class="move-btn move-done"
        @click="moveTask('done')"
      >

        ✓ Terminée

      </button>


    </div>


    <!-- ========================= -->
    <!-- ACTIONS -->
    <!-- ========================= -->

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


/* =========================================
   CARTE
========================================= */

.task-card {

  width: 100%;

  box-sizing: border-box;

  background: #111827;

  border: 1px solid rgba(255,255,255,.08);

  border-radius: 18px;

  padding: 18px;

  display: flex;

  flex-direction: column;

  gap: 14px;

  cursor: grab;

  transition: .25s;

  box-shadow:
    0 6px 18px rgba(0,0,0,.25);

}


.task-card:hover {

  transform: translateY(-5px);

  border-color: #2563eb;

  box-shadow:
    0 10px 25px rgba(37,99,235,.25);

}


.task-card:active {

  cursor: grabbing;

}


/* =========================================
   HEADER
========================================= */

.card-header {

  display: flex;

  justify-content: space-between;

  align-items: flex-start;

  gap: 12px;

}


.card-header h3 {

  min-width: 0;

  font-size: 18px;

  font-weight: 700;

  color: white;

  margin: 0;

  overflow-wrap: anywhere;

}


/* =========================================
   PRIORITE
========================================= */

.badge {

  flex-shrink: 0;

  padding: 5px 10px;

  border-radius: 30px;

  font-size: 10px;

  font-weight: bold;

  text-transform: uppercase;

  color: white;

}


.badge.low {

  background: #22c55e;

}


.badge.medium {

  background: #f59e0b;

}


.badge.high {

  background: #ef4444;

}


.badge.urgent {

  background: #dc2626;

}


/* =========================================
   ID
========================================= */

.task-id {

  margin: 0;

  color: #facc15;

  font-size: 12px;

}


/* =========================================
   DESCRIPTION
========================================= */

.description {

  margin: 0;

  color: #94a3b8;

  font-size: 14px;

  line-height: 1.6;

  overflow-wrap: anywhere;

}


/* =========================================
   INFOS
========================================= */

.card-infos {

  display: flex;

  flex-direction: column;

  gap: 6px;

  font-size: 13px;

  color: #cbd5e1;

}


.card-infos span {

  overflow-wrap: anywhere;

}


/* =========================================
   BOUTONS DE DEPLACEMENT
========================================= */

.move-buttons {

  display: flex;

  flex-wrap: wrap;

  gap: 8px;

  padding-top: 4px;

}


.move-btn {

  flex: 1;

  min-width: 100px;

  padding: 9px 10px;

  border: none;

  border-radius: 10px;

  color: white;

  font-size: 12px;

  font-weight: 700;

  cursor: pointer;

  transition: .2s;

}


.move-btn:hover {

  transform: translateY(-2px);

}


.move-back {

  background: #475569;

}


.move-progress {

  background: #d97706;

}


.move-done {

  background: #16a34a;

}


/* =========================================
   ACTIONS
========================================= */

.actions {

  display: flex;

  justify-content: space-between;

  gap: 10px;

  margin-top: 8px;

}


.actions button {

  flex: 1;

  padding: 10px;

  border: none;

  border-radius: 12px;

  font-weight: 600;

  cursor: pointer;

  transition: .25s;

}


.edit {

  background: #2563eb;

  color: white;

}


.edit:hover {

  background: #1d4ed8;

}


.delete {

  background: #dc2626;

  color: white;

}


.delete:hover {

  background: #b91c1c;

}


.archive {

  background: #16a34a;

  color: white;

}


.archive:hover {

  background: #15803d;

}


/* =========================================
   MOBILE
========================================= */

@media (max-width: 768px) {

  .task-card {

    cursor: default;

    padding: 15px;

  }


  .task-card:hover {

    transform: none;

  }


  .card-header {

    flex-direction: column;

    gap: 8px;

  }


  .badge {

    align-self: flex-start;

  }


  .move-buttons {

    display: grid;

    grid-template-columns: 1fr 1fr;

  }


  .move-btn {

    min-width: 0;

    width: 100%;

    min-height: 42px;

  }


  .actions button {

    min-height: 42px;

  }

}


/* =========================================
   PETIT TELEPHONE
========================================= */

@media (max-width: 390px) {

  .task-card {

    padding: 13px;

  }


  .card-header h3 {

    font-size: 16px;

  }


  .card-infos {

    font-size: 12px;

  }


  .move-buttons {

    grid-template-columns: 1fr;

  }

}

</style>