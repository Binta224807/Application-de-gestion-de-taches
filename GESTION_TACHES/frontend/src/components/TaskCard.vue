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
// GLISSER-DÉPOSER
// ===============================

const startDrag = (event) => {

  event.dataTransfer.effectAllowed = "move";

  event.dataTransfer.setData(
    "taskId",
    String(props.task.id)
  );

};


// ===============================
// MODIFIER
// ===============================

const editTask = () => {

  emit("editTask", props.task);

};


// ===============================
// SUPPRIMER
// ===============================

const deleteTask = () => {

  emit("deleteTask", props.task);

};


// ===============================
// ARCHIVER
// ===============================

const archiveTask = () => {

  emit("archiveTask", props.task);

};


// ===============================
// DÉPLACER
// ===============================

const moveTask = (newStatus) => {

  // Sécurité : ne rien faire
  // si on clique sur le statut actuel

  if (props.task.status === newStatus) {
    return;
  }

  emit("moveTask", {
    task: props.task,
    newStatus: newStatus,
  });

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

      <span v-if="task.due_time">
        🕒
        {{ task.due_time }}
      </span>

    </div>


    <!-- ========================= -->
    <!-- ACTIONS -->
    <!-- ========================= -->

    <div class="actions">

      <!-- MODIFIER -->

      <button
        class="edit"
        @click="editTask"
      >
        ✏️
        <span>Mod</span>
      </button>


      <!-- SUPPRIMER -->
      <!-- Visible seulement si la tâche -->
      <!-- n'est PAS terminée -->

      <button
        v-if="task.status !== 'done'"
        class="delete"
        @click="deleteTask"
      >
        🗑️
        <span>Sup</span>
      </button>


      <!-- ARCHIVER -->
      <!-- Visible seulement si terminée -->

      <button
        v-if="task.status === 'done'"
        class="archive"
        @click="archiveTask"
      >
        📦
        <span>Arch</span>
      </button>


      <!-- ========================= -->
      <!-- DÉPLACEMENT -->
      <!-- ========================= -->


      <!-- À FAIRE → EN COURS -->

      <button
        v-if="task.status === 'todo'"
        class="progress"
        @click="moveTask('in_progress')"
      >
        →
        <span>En cours</span>
      </button>


      <!-- EN COURS → À FAIRE -->

      <button
        v-if="task.status === 'in_progress'"
        class="todo"
        @click="moveTask('todo')"
      >
        ←
        <span>À faire</span>
      </button>


      <!-- EN COURS → TERMINÉ -->

      <button
        v-if="task.status === 'in_progress'"
        class="done"
        @click="moveTask('done')"
      >
        ✓
        <span>Terminé</span>
      </button>


      <!-- TERMINÉ → EN COURS -->

      <button
        v-if="task.status === 'done'"
        class="progress"
        @click="moveTask('in_progress')"
      >
        ←
        <span>En cours</span>
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

  transform: translateY(-4px);

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

  font-size: 18px;

  font-weight: 700;

  color: white;

  margin: 0;

  word-break: break-word;

}


/* =========================================
   PRIORITÉ
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

  color: #facc15;

  font-size: 12px;

  margin: 0;

}


/* =========================================
   DESCRIPTION
========================================= */

.description {

  color: #94a3b8;

  font-size: 14px;

  line-height: 1.6;

  margin: 0;

  overflow-wrap: anywhere;

}


/* =========================================
   INFORMATIONS
========================================= */

.card-infos {

  display: flex;

  flex-direction: column;

  gap: 7px;

  font-size: 13px;

  color: #cbd5e1;

}


.card-infos span {

  overflow-wrap: anywhere;

}


/* =========================================
   BOUTONS
========================================= */

.actions {

  display: flex;

  flex-wrap: nowrap;

  width: 100%;

  gap: 6px;

  margin-top: 8px;

}


.actions button {

  flex: 1;

  min-width: 0;

  min-height: 36px;

  padding: 7px 5px;

  border: none;

  border-radius: 9px;

  font-size: 11px;

  font-weight: 600;

  cursor: pointer;

  transition: .2s;

  color: white;

  white-space: nowrap;

}


.actions button:hover {

  transform: translateY(-2px);

}


.edit {
  background: #2563eb;
}


.edit:hover {
  background: #1d4ed8;
}


.delete {
  background: #dc2626;
}


.delete:hover {
  background: #b91c1c;
}


.archive {
  background: #16a34a;
}


.archive:hover {
  background: #15803d;
}


.progress {
  background: #d97706;
}


.progress:hover {
  background: #b45309;
}


.todo {
  background: #2563eb;
}


.todo:hover {
  background: #1d4ed8;
}


.done {
  background: #16a34a;
}


.done:hover {
  background: #15803d;
}


/* =========================================
   MOBILE
========================================= */

@media (max-width: 768px) {

  .task-card {

    padding: 16px;

    border-radius: 16px;

  }


  .task-card:hover {

    transform: none;

  }


  .card-header h3 {

    font-size: 17px;

  }


  .badge {

    font-size: 9px;

    padding: 5px 8px;

  }


  .actions {

    gap: 5px;

  }


  .actions button {

    min-height: 40px;

    padding: 8px 4px;

    font-size: 10px;

  }

}


/* =========================================
   PETIT TÉLÉPHONE
========================================= */

@media (max-width: 480px) {

  .task-card {

    padding: 14px;

  }


  .card-header {

    flex-direction: column;

    gap: 8px;

  }


  .badge {

    align-self: flex-start;

  }


  .actions {

    display: grid;

    grid-template-columns: repeat(2, 1fr);

    gap: 6px;

  }


  .actions button {

    width: 100%;

    min-height: 40px;

    font-size: 11px;

  }

}

</style>