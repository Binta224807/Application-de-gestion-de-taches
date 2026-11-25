<script setup>

import { computed } from "vue";
import { useRouter } from "vue-router";
import { formatDuration } from "../services/formatDuration.js";
import { User, Hourglass, CalendarDays } from "lucide-vue-next";

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits([
  "editTask",
  "deleteTask",
]);

const router = useRouter();

const priorityLabel = computed(() => {

  const labels = {
    low: "Faible",
    medium: "Moyenne",
    high: "Élevée",
    urgent: "Urgente",
  };

  return labels[props.task.priority] || props.task.priority;

});

const statusLabel = computed(() => {

  const labels = {
    todo: "À faire",
    in_progress: "En cours",
    review: "À vérifier",
    done: "Terminée",
  };

  return labels[props.task.status] || props.task.status;

});

const assignedName = computed(() => {

  const assignees = props.task.assigned_to || [];

  if (!assignees.length) {

    return "Non assigné";

  }

  const names = assignees
    .map((u) => u.username);

  if (names.length === 1) {

    return names[0];

  }

  return `${names[0]} +${names.length - 1}`;

});

const goToDetail = () => {

  router.push(`/tasks/${props.task.id}`);

};

const editTask = () => {

  emit("editTask", props.task);

};

const deleteTask = () => {

  emit("deleteTask", props.task);

};

</script>


<template>

  <div class="task-row" :class="'st-' + task.status" @click="goToDetail">

    <!-- COLONNE GAUCHE : TITRE + DESCRIPTION -->

    <div class="task-main">

      <h3 class="task-title">
        {{ task.title }}
      </h3>

      <p class="task-description">
        {{ task.description || "Aucune description" }}
      </p>

    </div>


    <!-- COLONNE CENTRALE : INFOS -->

    <div class="task-meta">

      <span
        class="badge status-badge"
        :class="task.status"
      >
        {{ statusLabel }}
      </span>

      <span
        class="badge priority-badge"
        :class="task.priority"
      >
        {{ priorityLabel }}
      </span>

      <span class="meta-item">
        <User :size="13" /> {{ assignedName }}
      </span>

      <span class="meta-item">
        <Hourglass :size="13" /> {{ formatDuration(task.estimated_duration) }}
      </span>

      <span
        v-if="task.due_date"
        class="meta-item"
      >
        <CalendarDays :size="13" /> {{ task.due_date }}
      </span>

    </div>


    <!-- COLONNE DROITE : ACTION -->

    <div class="task-actions">

      <button
        class="btn-detail"
        @click.stop="goToDetail"
      >
        Détails
      </button>

    </div>

  </div>

</template>


<style scoped>

.task-row {

  width: 100%;
  box-sizing: border-box;

  background: var(--surface);

  border: 1px solid var(--border);

  border-radius: 16px;

  padding: 18px 20px;

  display: grid;
  grid-template-columns: 1fr auto auto;
  align-items: center;
  gap: 20px;

  transition: .25s;

  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);

}


.task-row:hover {

  border-color: var(--accent-border);

  box-shadow: 0 8px 24px rgba(59, 130, 246, 0.15);

  transform: translateY(-2px);

}


.task-main {

  min-width: 0;

  overflow: hidden;

}


.task-title {

  font-size: 17px;
  font-weight: 700;
  color: var(--text-h);
  margin: 0 0 6px 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

}


.task-description {

  color: var(--text);
  font-size: 13px;
  margin: 0;

  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

}


.task-meta {

  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;

}


.badge {

  padding: 5px 10px;
  border-radius: 999px;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  color: white;

}


.priority-badge.low {
  background: #22c55e;
}

.priority-badge.medium {
  background: #f59e0b;
}

.priority-badge.high {
  background: #ef4444;
}

.priority-badge.urgent {
  background: #dc2626;
}


.status-badge.todo {
  background: var(--accent);
}

.status-badge.in_progress {
  background: #d97706;
}

.status-badge.review {
  background: #8b5cf6;
}

.status-badge.done {
  background: #16a34a;
}


.meta-item {

  color: var(--text-strong);
  font-size: 13px;
  padding: 4px 10px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;

  white-space: nowrap;

  display: inline-flex;
  align-items: center;
  gap: 6px;

}


.task-actions {

  display: flex;
  align-items: center;
  gap: 8px;

}


.btn-detail {

  background: var(--accent-strong);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: .2s;

  white-space: nowrap;

}


.btn-detail:hover {

  background: var(--accent);
  transform: translateY(-1px);

}


/* TABLETTE */

@media (max-width: 1024px) {

  .task-row {

    grid-template-columns: 1fr auto;
    gap: 16px;

  }

  .task-actions {

    grid-column: 2;
    grid-row: 1;

  }

  .task-meta {

    grid-column: 1 / -1;
    justify-content: flex-start;

  }

}


/* MOBILE : ligne compacte style app */

@media (max-width: 640px) {

  .task-row {

    position: relative;
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 10px 12px 10px 16px;
    border-radius: 10px;

  }


  .task-row::before {

    content: "";
    position: absolute;
    left: 0;
    top: 8px;
    bottom: 8px;
    width: 3px;
    border-radius: 3px;
    background: var(--accent);

  }


  .task-row.st-in_progress::before { background: #d97706; }
  .task-row.st-review::before { background: #8b5cf6; }
  .task-row.st-done::before { background: #16a34a; }


  .task-title {

    font-size: 14px;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

  }


  .task-description {

    display: none;

  }


  .task-meta {

    flex-wrap: nowrap;
    gap: 5px;
    overflow: hidden;

  }


  .badge {

    padding: 2px 7px;
    font-size: 9px;
    letter-spacing: .4px;
    flex-shrink: 0;

  }


  .meta-item {

    font-size: 10px;
    padding: 2px 6px;
    gap: 4px;
    flex-shrink: 0;

  }


  .meta-item svg {

    width: 11px;
    height: 11px;

  }


  .task-actions {

    display: none;

  }

}

</style>
