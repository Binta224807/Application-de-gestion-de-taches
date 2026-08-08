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
// GLISSER-DÉPOSER — ORDINATEUR
// ===============================

const startDrag = (event) => {

  event.dataTransfer.effectAllowed = "move";

  event.dataTransfer.setData(
    "taskId",
    props.task.id
  );

};


// ===============================
// MODIFIER
// ===============================

const editTask = () => {

  emit(
    "editTask",
    props.task
  );

};


// ===============================
// SUPPRIMER
// ===============================

const deleteTask = () => {

  emit(
    "deleteTask",
    props.task
  );

};


// ===============================
// ARCHIVER
// ===============================

const archiveTask = () => {

  emit(
    "archiveTask",
    props.task
  );

};


// ===============================
// DÉPLACER — MOBILE
// ===============================

const moveTask = (status) => {

  emit(
    "moveTask",
    {
      taskId: props.task.id,
      newStatus: status
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

        {{
          task.priority === "low"
            ? "Faible"
            : task.priority === "medium"
            ? "Moyenne"
            : task.priority === "high"
            ? "Élevée"
            : task.priority === "urgent"
            ? "Urgente"
            : task.priority
        }}

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

        📅
        {{ task.due_date || "Pas de date" }}

      </span>


      <span>

        📂
        {{ task.project_name || "Sans projet" }}

      </span>


      <span>

        🏷️
        {{ task.category_name || "Sans catégorie" }}

      </span>


      <span>

        ⏱️
        {{ task.estimated_duration || 0 }} min

      </span>


      <span
        v-if="task.due_time"
      >

        🕒
        {{ task.due_time }}

      </span>

    </div>


    <!-- ========================= -->
    <!-- DÉPLACEMENT MOBILE -->
    <!-- ========================= -->

    <div class="mobile-move-actions">

      <p class="move-title">
        Déplacer la tâche
      </p>


      <div class="move-buttons">

        <button
          v-if="task.status !== 'todo'"
          class="move-btn todo-btn"
          @click="moveTask('todo')"
        >

          ← À faire

        </button>


        <button
          v-if="task.status !== 'in_progress'"
          class="move-btn progress-btn"
          @click="moveTask('in_progress')"
        >

          → En cours

        </button>


        <button
          v-if="task.status !== 'done'"
          class="move-btn done-btn"
          @click="moveTask('done')"
        >

          ✓ Terminée

        </button>

      </div>

    </div>


    <!-- ========================= -->
    <!-- ACTIONS -->
    <!-- ========================= -->

    <div class="actions">

      <button
        class="edit"
        @click="editTask"
      >

        ✏️
        <span>Modifier</span>

      </button>


      <button
        v-if="task.status === 'done'"
        class="archive"
        @click="archiveTask"
      >

        📦
        <span>Archiver</span>

      </button>


      <button
        v-else
        class="delete"
        @click="deleteTask"
      >

        🗑️
        <span>Supprimer</span>

      </button>

    </div>

  </div>

</template>


<style scoped>


/* =========================================
   CARTE
========================================= */

.task-card {

  width:100%;

  box-sizing:border-box;

  background:#111827;

  border:1px solid rgba(255,255,255,.08);

  border-radius:18px;

  padding:18px;

  display:flex;

  flex-direction:column;

  gap:14px;

  cursor:grab;

  transition:.25s;

  box-shadow:
    0 6px 18px rgba(0,0,0,.25);

}


.task-card:hover {

  transform:translateY(-4px);

  border-color:#2563eb;

  box-shadow:
    0 10px 25px rgba(37,99,235,.25);

}


.task-card:active {

  cursor:grabbing;

}


/* =========================================
   HEADER
========================================= */

.card-header {

  display:flex;

  justify-content:space-between;

  align-items:flex-start;

  gap:12px;

}


.card-header h3 {

  font-size:18px;

  font-weight:700;

  color:white;

  margin:0;

  word-break:break-word;

}


/* =========================================
   PRIORITÉ
========================================= */

.badge {

  flex-shrink:0;

  padding:5px 10px;

  border-radius:30px;

  font-size:10px;

  font-weight:bold;

  text-transform:uppercase;

  color:white;

}


.badge.low {

  background:#22c55e;

}


.badge.medium {

  background:#f59e0b;

}


.badge.high {

  background:#ef4444;

}


.badge.urgent {

  background:#dc2626;

}


/* =========================================
   ID
========================================= */

.task-id {

  color:#facc15;

  font-size:12px;

  margin:0;

}


/* =========================================
   DESCRIPTION
========================================= */

.description {

  color:#94a3b8;

  font-size:14px;

  line-height:1.6;

  margin:0;

  overflow-wrap:anywhere;

}


/* =========================================
   INFORMATIONS
========================================= */

.card-infos {

  display:flex;

  flex-direction:column;

  gap:7px;

  font-size:13px;

  color:#cbd5e1;

}


.card-infos span {

  overflow-wrap:anywhere;

}


/* =========================================
   DÉPLACEMENT MOBILE
========================================= */

.mobile-move-actions {

  display:none;

  padding-top:8px;

  border-top:1px solid rgba(255,255,255,.08);

}


.move-title {

  color:#94a3b8;

  font-size:12px;

  margin:0 0 10px;

}


.move-buttons {

  display:flex;

  flex-wrap:wrap;

  gap:8px;

}


.move-btn {

  flex:1;

  min-width:110px;

  min-height:42px;

  border:none;

  border-radius:11px;

  color:white;

  font-weight:600;

  cursor:pointer;

  padding:9px 10px;

}


.todo-btn {

  background:#2563eb;

}


.progress-btn {

  background:#d97706;

}


.done-btn {

  background:#16a34a;

}


.move-btn:active {

  transform:scale(.97);

}


/* =========================================
   ACTIONS
========================================= */

.actions {

  display:flex;

  justify-content:space-between;

  gap:10px;

  margin-top:8px;

}


.actions button {

  flex:1;

  min-height:42px;

  padding:10px;

  border:none;

  border-radius:12px;

  font-weight:600;

  cursor:pointer;

  transition:.25s;

  color:white;

}


.edit {

  background:#2563eb;

}


.edit:hover {

  background:#1d4ed8;

}


.delete {

  background:#dc2626;

}


.delete:hover {

  background:#b91c1c;

}


.archive {

  background:#16a34a;

}


.archive:hover {

  background:#15803d;

}


/* =========================================
   MOBILE
========================================= */

@media (max-width:768px) {

  .task-card {

    padding:16px;

    border-radius:16px;

    cursor:default;

  }


  .task-card:hover {

    transform:none;

    box-shadow:
      0 6px 18px rgba(0,0,0,.25);

  }


  .mobile-move-actions {

    display:block;

  }


  .card-header {

    align-items:flex-start;

  }


  .card-header h3 {

    font-size:17px;

  }


  .badge {

    font-size:9px;

    padding:5px 8px;

  }


  .actions button {

    min-height:46px;

  }

}


/* =========================================
   PETIT TÉLÉPHONE
========================================= */

@media (max-width:480px) {

  .task-card {

    padding:14px;

  }


  .card-header {

    flex-direction:column;

    gap:8px;

  }


  .badge {

    align-self:flex-start;

  }


  .move-buttons {

    flex-direction:column;

  }


  .move-btn {

    width:100%;

    min-height:44px;

  }


  .actions {

    flex-direction:column;

  }


  .actions button {

    width:100%;

    min-height:46px;

  }

}

</style>